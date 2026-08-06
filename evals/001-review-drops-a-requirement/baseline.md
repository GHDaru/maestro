# Baseline — case 001

Date: pending
Target-commit: pending
First-red: pending
Verdict: not yet run

## Status

This case has never been executed. It was written in cycle 037 together with the gate, and
running it needs a model in the loop, which that cycle did not do.

Until `/eval 001-review-drops-a-requirement` runs and records a result here, this case is a
hope, and `check-evals.sh` fails on it by design. Recorded as an open finding in
`docs/records/decisoes.jsonl`.

## How to fill this in

Run the case in fresh context, then replace the fields above with what happened:

```
Date: <YYYY-MM-DD>
Target-commit: <short sha of the last commit touching the target>
First-red: <YYYY-MM-DD — the run in which this case rejected an answer, and which assertion>
Verdict: <pass | fail> — <assertion-by-assertion result>
```

`First-red` stays `pending` until the case has actually rejected something. If every run
passes, that is not a green case — it is an untested one. Weaken the answer deliberately
(drop the FR2 mention from a candidate verdict) and confirm the case catches it.
