# ADRs — <project>

Architecture/Methodology Decision Records: **immutable** decisions (a later ADR may supersede
one; its merit is never rewritten). Shape: context → decision → consequences → sources.

<!-- This table is the CONTRACT that scripts/check-adr.sh reads. Three columns, in this order:

       | ADR | Title (linked to the file) | Status |

     - one row per ADR, and exactly one — two rows for the same ADR is worse than none,
       because one of them is wrong and the reader cannot tell which;
     - the first cell is the four-digit number, bare;
     - the title cell LINKS to the file (`NNNN-slug.md`, optionally `./` and an `#anchor`);
     - the status cell uses the closed vocabulary below, and must agree with the
       `- **Status**:` line inside the ADR itself.

     Closed vocabulary (either language; the gate maps synonyms):
       Accepted / Aceito · Proposed / Proposto · Rejected / Rejeitado ·  PT-DATA (vocabulary)
       Superseded by NNNN / Superado pelo NNNN                                  PT-DATA (vocabulary)

     A commented-out row, a struck-through row, or a mention in the prose below does NOT
     count as listed — an ADR must be findable in the rendered table, which is what a reader
     actually sees. That distinction is why this file has a gate at all (Maestro cycle 049). -->

| ADR | Título | Status |
|---|---|---|

<!-- The first row, once you have an ADR: three cells — the bare number, the title written
     as a markdown link to the file 0001-the-first-decision.md, and the status. Written in
     words rather than as a real link because this template ships with no ADR beside it, and
     a link to a file that does not exist is the defect the gate next door already checks. -->

> Machine-queryable index (append-only): `docs/records/decisoes.jsonl` — see the protocol in
> `docs/records/README.md`. This file is the human entry point; that one is the agent's.

## Numbering

Sequential, four digits, never reused. A superseded ADR keeps its number and its body: the
reversal is a **new** ADR that says what changed and why, and the status of the old one is
updated in both places — here and in its own header.
