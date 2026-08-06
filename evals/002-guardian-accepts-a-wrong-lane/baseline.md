# Baseline — case 002

Date: pending
Target-commit: pending
First-red: pending
Verdict: not yet run

## Status

Never executed. Written in cycle 037 alongside the gate; running it needs a model in the
loop, which that cycle did not do. `check-evals.sh` fails on it by design until a run is
recorded here. Tracked as an open finding in `docs/records/decisoes.jsonl`.

## How to fill this in

```
Date: <YYYY-MM-DD>
Target-commit: <short sha of the last commit touching the target>
First-red: <YYYY-MM-DD — the run in which this case rejected an answer, and which assertion>
Verdict: <pass | fail> — <assertion-by-assertion result>
```

For `First-red` on this case, the cheapest deliberate weakening is a candidate verdict that
returns COMPLIANT because the lane block is present and complete. If the case does not
reject that, its assertions are too loose and need tightening before it counts.
