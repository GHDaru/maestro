# NNN — <the idea, in one sentence>

<!-- Evaluation card for something from OUTSIDE the project. Copy this file into
     docs/ecosystem/ideias/ and fill it in. Read by scripts/check-ecosystem.sh.

     THE UNIT IS THE IDEA, NOT THE TOOL. You almost never adopt someone's whole tool; you
     absorb an idea and leave the rest. "Superpowers: absorb + observe" is not actionable.
     "Root cause before fix: absorb, into skills/diagnose-before-fix/SKILL.md" is — and it
     is falsifiable, which is the point.

     THIS CARD IS IMMUTABLE. It records what you saw and judged ON A DATE. When the verdict
     changes later, append a line to estado.jsonl — never rewrite this file. Mixing the
     moment with the state forces a choice between rewriting history and lying about today. -->

- **Id**: `<slug>`                                   <!-- matches estado.jsonl -->
- **Source**: `<owner/repo>`                         <!-- must exist in the sources file, with its licence -->
- **Observed**: <YYYY-MM-DD>                         <!-- the date OF THE OBSERVATION, not today -->
- **Verdict at the time**: <adopt|absorb|observe|discard>
- **Destination**: `<path/to/file>`                  <!-- required for adopt/absorb; a FILE, not a folder -->
- **Re-evaluation trigger**: <observable condition>   <!-- required for observe -->

## The idea

<!-- What it is, in the source's own terms. Two or three sentences. If you cannot state it
     without naming the tool, you have not found the idea yet. -->

## Why it crosses the line (or does not)

<!-- The reasoning. Name which dimension decided — usually one did, alone. If the tool is
     rejected but the idea survives (or the reverse), say so and link the sibling card. -->

## Dimensions

<!-- All seven, always, in this order. A partial evaluation depends on who wrote it.
     Two of them REJECT ON THEIR OWN: an incompatible licence and an irreconcilable
     conflict with a principle are not offset by maturity or popularity. There is no
     aggregate score, on purpose: an average hides which dimension decided. -->

| # | Dimension | Reading |
|---|---|---|
| 1 | Conflict with a principle | <which principle, and is it irreconcilable?> |
| 2 | Licence and redistribution | <copyable, or citable only? no licence = all rights reserved> |
| 3 | Function already served | <does it duplicate something we have? Principle VI> |
| 4 | Context cost | <what it costs to carry> |
| 5 | Reversibility | <what leaving costs later — lock-in> |
| 6 | Maturity and evidence | <what WE observed, at which version — not third-party stars> |
| 7 | Real pain today | <does the pain it solves exist here, now? YAGNI> |

<!-- Vocabulary, closed:
     adopt    the tool comes in, as a dependency of the method   -> destination must exist
     absorb   the IDEA comes in, reimplemented in our artifact   -> destination must exist
     observe  not now; may change                                -> trigger must be written
     discard  does not come in — principle, licence, or already served

     `observe` with no trigger is forgetting with ceremony, and the gate refuses it. When no
     future condition could change the decision, the honest verdict is `discard`.

     The gate reads BOTH spellings of every field and of the closed vocabulary: Maestro's own
     catalogue is written in Portuguese, because it is published in the book, while the
     installable surface is English (ADR 0014). Write yours in either. -->
