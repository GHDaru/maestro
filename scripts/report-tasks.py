#!/usr/bin/env python3
"""report-tasks.py — answers "how much am I spending?" from the task ledger.

Why this exists. The ledger (docs/records/tarefas.jsonl) holds only events, written when they
happened. Every entity (task, attempt, verdict) and every number is derived HERE, at read time,
so the ledger never has to be rewritten and a new metric never needs a migration.

What it reports (definitions: specs/064-*/data-model.md):
  * tokens and cost per kind, per cycle and per model (per model from `tokens_by_model`);
  * first-pass approval: tasks approved whose only attempt is 1 / tasks with a verdict;
  * rework cost: tokens and cost of attempts with attempt >= 2;
  * cache rate: cache_read / (tokens_in + cache_read + cache_write);
  * orphans: a `start` with no paired `stop` (same task_id and session, and same attempt when
    both carry one; a stop closes the most recent open start). Never completed by inference.

Usage:  scripts/report-tasks.py [--ledger PATH] [--cycle NNN] [--json]
        MAESTRO_TASK_LEDGER=<path> overrides the default ledger.
Exit:   0 when the ledger could be read · 2 usage or unreadable ledger

Limits, declared.
  * A line that is not a JSON object, or whose fields have the wrong type, is counted as invalid
    and skipped — never fatal. Unknown fields are ignored.
  * Cost is whatever the ledger recorded: this script does not price tokens.
  * A `stop` with no token or cost field is NOT 0: it is "not measured", counted apart, and
    shown as null in --json.
  * A verdict counts only when its `by` is the id of a task of kind audit or review in this same
    ledger (Principle II: whoever executes, or manages, does not grade) AND its `session` is the
    session of a `start` of that task (whoever judged is whoever ran the audit). Others are
    counted as "verdicts from non-judges" and ignored. The verdict of a task is the LAST one that
    counts. The session check assumes distinct session ids per executor: nested sessions can
    repeat an id (measured in cycle 064), and then it cannot tell them apart. The label itself is
    not authenticated either: a session with no open task can open an audit task and judge.
  * A verdict on a task that never had a `start` has unknown attempts: listed apart, not counted.
  * A verdict whose target ends in "-cycle" (e.g. "064-cycle") is the verdict on a whole cycle,
    not on a task: reported apart as "Cycle verdicts" (last valid one per cycle, with history),
    never as "no start" and never in the first-pass rate. Same judge rule as above. Task ids
    ending in "-cycle" are therefore reserved.
  * --cycle scopes a verdict by the cycle of its TARGET task (verdict events carry no cycle);
    when the target has no event with a cycle, by the cycle of the judge.
"""
import argparse
import json
import os
import sys

DEFAULT_LEDGER = os.path.join("docs", "records", "tarefas.jsonl")
APPROVED = {"approved", "approved_with_notes"}
JUDGE_KINDS = {"audit", "review"}
CYCLE_SUFFIX = "-cycle"
MEASURES = ("tokens_in", "tokens_out", "tokens_cache_read", "tokens_cache_write", "cost_usd")


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def num(value):
    return value if is_number(value) else 0


def tokens_of(rec):
    return sum(num(rec.get(k)) for k in
               ("tokens_in", "tokens_out", "tokens_cache_read", "tokens_cache_write"))


def measured(rec):
    """A stop that carries no token or cost field is work nobody measured — not work that cost 0."""
    return any(is_number(rec.get(k)) for k in MEASURES)


def well_typed(rec):
    """False for a line whose field types would break the arithmetic or a set/dict lookup."""
    for field in ("event", "task_id"):
        if not isinstance(rec.get(field), str) or not rec[field]:
            return False
    for field in ("kind", "session", "by", "verdict", "outcome"):
        if rec.get(field) is not None and not isinstance(rec[field], str):
            return False
    if rec.get("attempt") is not None and type(rec["attempt"]) is not int:
        return False
    cyc = rec.get("cycle")
    if cyc is not None and not (isinstance(cyc, str) or type(cyc) is int):
        return False
    return not (rec["event"] == "verdict" and not rec.get("verdict"))


def load(path):
    events, invalid = [], 0
    with open(path, encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            if not raw.strip():
                continue
            try:
                rec = json.loads(raw)
            except json.JSONDecodeError:
                invalid += 1
                continue
            if isinstance(rec, dict) and well_typed(rec):
                if rec.get("cycle") is not None:
                    rec["cycle"] = str(rec["cycle"])
                events.append(rec)
            else:
                invalid += 1
    return events, invalid


def bucket(rows, key, tokens, cost, is_measured=True):
    row = rows.setdefault(str(key), {"tokens": 0, "cost_usd": 0.0, "attempts": 0, "unmeasured": 0})
    if not is_measured:  # counted apart: adding it as 0 would pass a gap off as a cheap attempt
        row["unmeasured"] += 1
        return
    row["tokens"] += tokens
    if cost is None or row["cost_usd"] is None:  # the grouping carries no cost data: null, never 0
        row["cost_usd"] = None
    else:
        row["cost_usd"] = round(row["cost_usd"] + cost, 6)
    row["attempts"] += 1


def seal(rows):
    """A row made only of unmeasured attempts has no number to show: null, not 0."""
    for row in rows.values():
        if row["attempts"] == 0 and row["unmeasured"]:
            row["tokens"], row["cost_usd"] = None, None


def analyse(events, invalid, cycle=None):
    # The whole book first: a verdict has no cycle of its own, and who may judge is decided by
    # the kind of the task named in `by`, wherever that task's events are.
    kinds, task_cycle, start_sessions = {}, {}, {}
    for ev in events:
        if ev.get("kind") and ev["event"] != "verdict":
            kinds.setdefault(ev["task_id"], ev["kind"])
        if ev["event"] == "start" and ev.get("session"):
            start_sessions.setdefault(ev["task_id"], set()).add(ev["session"])
        if ev.get("cycle") is not None:
            task_cycle.setdefault(ev["task_id"], ev["cycle"])

    def cycle_of_verdict(ev):
        """"064" for a verdict on "064-cycle"; None for a verdict on an ordinary task."""
        tid = ev["task_id"]
        if ev["event"] == "verdict" and tid.endswith(CYCLE_SUFFIX) and len(tid) > len(CYCLE_SUFFIX):
            return tid[:-len(CYCLE_SUFFIX)]
        return None

    def in_scope(ev):
        if cycle is None:
            return True
        if cycle_of_verdict(ev) is not None:
            return cycle_of_verdict(ev) == cycle
        if ev["event"] == "verdict":
            return (task_cycle.get(ev["task_id"]) or task_cycle.get(ev.get("by"))) == cycle
        return str(ev.get("cycle", "")) == cycle

    def is_judge(ev):
        by = ev.get("by")
        return (kinds.get(by) in JUDGE_KINDS and by != ev["task_id"]
                and ev.get("session") in start_sessions.get(by, ()))

    events = [e for e in events if in_scope(e)]
    by_kind, by_cycle, by_model = {}, {}, {}
    rework = {"tokens": 0, "cost_usd": 0.0, "attempts": 0, "unmeasured_attempts": 0}
    cache = {"read": 0, "denominator": 0}
    open_starts, not_measured = [], []
    attempts, started, verdicts, non_judge = {}, set(), {}, 0
    cycle_verdicts = {}

    for ev in events:
        kind = ev["event"]
        tid = ev["task_id"]
        att = ev.get("attempt")
        if kind == "start":
            open_starts.append(ev)
            started.add(tid)
            attempts.setdefault(tid, set()).add(att if att is not None else 1)
        elif kind == "stop":
            for i in range(len(open_starts) - 1, -1, -1):
                st = open_starts[i]
                if (st["task_id"] == tid and st.get("session") == ev.get("session")
                        and (att is None or st.get("attempt") is None or att == st.get("attempt"))):
                    del open_starts[i]
                    break
            attempts.setdefault(tid, set()).add(att if att is not None else 1)
            has_data = measured(ev)
            tok, cost = tokens_of(ev), float(num(ev.get("cost_usd")))
            bucket(by_kind, ev.get("kind", "unknown"), tok, cost, has_data)
            bucket(by_cycle, ev.get("cycle", "unknown"), tok, cost, has_data)
            if not has_data:
                not_measured.append({"task_id": tid, "attempt": att})
            models = ev.get("tokens_by_model")
            if isinstance(models, dict):
                for name, m in models.items():
                    if isinstance(m, dict):
                        mt = sum(num(m.get(k)) for k in
                                 ("input", "output", "cacheRead", "cacheWrite"))
                        bucket(by_model, name, mt, None)  # cost is per attempt, not per model
            if att is not None and att >= 2:
                if has_data:
                    rework["tokens"] += tok
                    rework["cost_usd"] = round(rework["cost_usd"] + cost, 6)
                    rework["attempts"] += 1
                else:
                    rework["unmeasured_attempts"] += 1
            cache["read"] += num(ev.get("tokens_cache_read"))
            cache["denominator"] += (num(ev.get("tokens_in")) + num(ev.get("tokens_cache_read"))
                                     + num(ev.get("tokens_cache_write")))
        elif kind == "verdict":
            if not is_judge(ev):  # Principle II: whoever delivered, or manages, does not grade
                non_judge += 1
            elif cycle_of_verdict(ev) is not None:
                cycle_verdicts.setdefault(cycle_of_verdict(ev), []).append(
                    {"verdict": ev["verdict"], "by": ev["by"], "ts": ev.get("ts")})
            else:
                verdicts[tid] = ev["verdict"]  # last one wins

    for rows in (by_kind, by_cycle, by_model):
        seal(rows)
    if rework["attempts"] == 0 and rework["unmeasured_attempts"]:
        rework["tokens"], rework["cost_usd"] = None, None

    orphans = [{k: st.get(k) for k in ("task_id", "attempt", "session", "ts")}
               for st in open_starts]
    no_start = sorted(t for t in verdicts if t not in started)  # attempts unknown: not counted
    judged = [t for t in verdicts if t in started]
    first_pass = [t for t in judged if verdicts[t] in APPROVED and attempts[t] <= {1}]
    return {
        "events": len(events),
        "invalid_lines": invalid,
        "by_kind": by_kind,
        "by_cycle": by_cycle,
        "by_model": by_model,
        "first_pass_approval": {
            "approved_first_pass": len(first_pass),
            "tasks_with_verdict": len(judged),
            "rate": round(len(first_pass) / len(judged), 4) if judged else None,
            "verdicts_without_start": no_start,
            "verdicts_from_non_judges": non_judge,
        },
        "cycle_verdicts": {c: {"current": h[-1]["verdict"], "by": h[-1]["by"], "history": h}
                           for c, h in sorted(cycle_verdicts.items())},
        "rework": rework,
        "not_measured": not_measured,
        "cache_rate": round(cache["read"] / cache["denominator"], 4) if cache["denominator"] else None,
        "orphans": orphans,
    }


def table(title, rows, note=None):
    print(f"── {title} ──")
    if not rows:
        print("  (none)")
        return
    width = max(len(k) for k in rows)
    print(f"  {'name':<{width}}  {'attempts':>8}  {'tokens':>12}  {'cost_usd':>12}")
    for key in sorted(rows):
        r = rows[key]
        if r["tokens"] is None:
            tokens, cost, extra = "not measured", "not measured", ""
        else:
            tokens = f"{r['tokens']:,}"
            cost = "-" if r["cost_usd"] is None else f"{r['cost_usd']:.4f}"
            extra = f"  (+{r['unmeasured']} not measured)" if r["unmeasured"] else ""
        print(f"  {key:<{width}}  {r['attempts']:>8}  {tokens:>12}  {cost:>12}{extra}")
    if note and any(r["cost_usd"] is None and r["tokens"] is not None for r in rows.values()):
        print(f"  note: {note}")


def show(rep):
    print(f"events: {rep['events']}   invalid lines: {rep['invalid_lines']}")
    table("By kind", rep["by_kind"])
    table("By cycle", rep["by_cycle"])
    table("By model", rep["by_model"],
          "'-' = no cost data: the ledger records cost per attempt, not per model, "
          "so a per-model cost would be invented")
    fp = rep["first_pass_approval"]
    rate = "n/a" if fp["rate"] is None else f"{fp['rate']:.0%}"
    print(f"── First-pass approval ──\n  {fp['approved_first_pass']}/{fp['tasks_with_verdict']} ({rate})")
    print(f"  verdicts from non-judges: {fp['verdicts_from_non_judges']}, ignored "
          "(only a task of kind audit or review in this ledger may grade)")
    if fp["verdicts_without_start"]:
        print("  verdicts on tasks with no start (attempts unknown, not counted): "
              + ", ".join(fp["verdicts_without_start"]))
    print("── Cycle verdicts ──")
    if not rep["cycle_verdicts"]:
        print("  (none)")
    for cyc, cv in rep["cycle_verdicts"].items():
        trail = " → ".join(f"{h['verdict']} by {h['by']}" for h in cv["history"])
        history = f"  (history: {trail})" if len(cv["history"]) > 1 else ""
        print(f"  {cyc}: {cv['current']} by {cv['by']}{history}")
    rw = rep["rework"]
    spent = ("not measured" if rw["tokens"] is None
             else f"{rw['tokens']:,} tokens, ${rw['cost_usd']:.4f}")
    print(f"── Rework (attempt >= 2) ──\n  {rw['attempts']} measured attempt(s): {spent}")
    if rw["unmeasured_attempts"]:
        print(f"  + {rw['unmeasured_attempts']} attempt(s) not measured (no tokens or cost recorded)")
    if rep["not_measured"]:
        names = ", ".join(f"{n['task_id']}#{n['attempt']}" for n in rep["not_measured"])
        print(f"── Not measured (stop without tokens or cost) ──\n  {len(rep['not_measured'])}: {names}")
    cr = "n/a" if rep["cache_rate"] is None else f"{rep['cache_rate']:.1%}"
    print(f"── Cache rate ──\n  {cr}")
    print(f"── Orphans (start without stop) ──\n  {len(rep['orphans'])}")
    for o in rep["orphans"]:
        print(f"  {o['task_id']} attempt={o['attempt']} session={o['session']} since {o['ts']}")


def main(argv):
    ap = argparse.ArgumentParser(description="Report spending from the task ledger.")
    ap.add_argument("--ledger", default=os.environ.get("MAESTRO_TASK_LEDGER", DEFAULT_LEDGER))
    ap.add_argument("--cycle", help="only events of this cycle (e.g. 064)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv[1:])
    try:
        events, invalid = load(args.ledger)
    except OSError as exc:
        print(f"error: cannot read ledger ({exc})", file=sys.stderr)
        return 2
    rep = analyse(events, invalid, args.cycle)
    if args.json:
        json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        show(rep)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
