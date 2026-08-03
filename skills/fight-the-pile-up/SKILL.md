---
name: fight-the-pile-up
description: Editorial checklist that turns a dense document (a "pile-up" — many acronyms with no dictionary, everything on one page, no narrative) into clear text without changing the technical content. Use it when writing or reviewing any Maestro document (handbook, guide, README, ADR), when a text has unexplained acronyms or orphan jargon, or when someone says a document is "heavy", "dense" or "hard to follow".
---

# Fight the pile-up

## Iron Law

```
NO NAKED ACRONYM — EVERY ACRONYM EXPANDED ON FIRST OCCURRENCE AND IN THE GLOSSARY
```

**Violating the letter of this rule violates its spirit.** This is NOT an excuse:
- "everyone knows this acronym" — tomorrow's reader (or the new agent) does not;
- "I will expand it later" — later is where the pile-up is born.

"Pile-up" is the defect named by the Steward: a dense document, many acronyms with no
dictionary, everything stacked with no storytelling. This skill is the ruler for fixing the
**form** — never the technical fact.

## When to fire

Writing or reviewing a Maestro document; a text with an unexplained acronym or orphan
jargon; feedback of "heavy / dense / hard to follow".

## Checklist (every item is checkable)

1. **One subject per page or section.** If the section mixes two topics, split it.
2. **Acronym expanded on first occurrence** and present in the glossary. Example: "DoD
   (Definition of Done — what counts as finished)". Check: no new acronym appears naked.
3. **Zero orphan jargon** — every specialised term has a definition one click away
   (glossary) or inline. If you cannot link it, explain it in one sentence.
4. **An order that tells a story**: concrete before abstract, problem before rule. Start
   with the *why*, not with the taxonomy.
5. **Example beats dry definition.** Every rule earns a real example, preferably from one of
   our own cycles.
6. **Preserve the content.** Did you rewrite the technical fact? That is outside this skill —
   it is the author's or architect's decision, not the editor's.

## How to apply it

- Read the document once, marking every checklist item that fails.
- Fix form, order and glossary; do **not** invent or remove facts.
- If a term is missing from the glossary, add it there (single source) and link to it — do
  not redefine it locally.

## Example

> ❌ "DoR and DoD gate the cycle through RACI." (three naked acronyms, no story)
> ✅ "Before starting we check whether the spec is ready (DoR — Definition of Ready). At the
> end, whether it is done (DoD — Definition of Done). The person who approves each door is
> the owner (the *Accountable* in RACI)." (acronyms expanded, narrative order, role explained)

**Consumed by:** `didactics-editor` (applies it), `tech-writer` (integrates it in the pull
request).
