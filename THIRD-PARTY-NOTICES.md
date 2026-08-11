# Third-party notices

Maestro is distributed under the MIT License, whose full text is in `LICENSE` — installed as
`docs/governance/MAESTRO-LICENSE` when the method is copied into another repository, and as
`LICENSE` inside the plugin package. Maestro also **redistributes** material from the
projects below: the Maestro installer copies it into other repositories, and
`plugin/maestro/` ships it as a plugin. MIT is permissive but has exactly one obligation, and
this file is how Maestro meets it — the copyright notice and the permission notice travel
with the copies.

> Paths here are written as plain names, not links, on purpose: this file is **installed
> under a different name and a different directory**, where a relative link to `LICENSE`
> would resolve to a file that does not exist there.

Provenance of each vendored piece — upstream version, commit and verbatim/adapted state —
is tracked in `.specify/UPSTREAM.md`. This file records the **attribution**; that one records
the **lineage**.

---

## github/spec-kit

- **Upstream**: <https://github.com/github/spec-kit> — installed via speckit **0.4.3**
- **Fork used for the `converge` command**: `GHDaru/spec-kit` @ `0117a7b` (2026-07-27)
- **Licence**: MIT
- **Copyright**: Copyright GitHub, Inc.

**What is redistributed**, and in what state (authoritative table in `.specify/UPSTREAM.md`):

| Path | State |
|---|---|
| `.specify/templates/spec-template.md` · `plan-template.md` · `tasks-template.md` | **Modified** by Maestro (cycles 009, 042, 045) |
| `.claude/commands/speckit.plan.md` | **Modified** by Maestro (cycles 044, 048) |
| `.claude/commands/speckit.converge.md` | **Modified** by Maestro (cycle 009), from the `GHDaru/spec-kit` fork |
| `.claude/commands/speckit.constitution.md` · `speckit.analyze.md` | **Modified** by Maestro (cycle 048) |
| `.claude/commands/speckit.*.md` (remaining) | Verbatim |
| `.specify/templates/checklist-template.md` · `constitution-template.md` · `agent-file-template.md` | Verbatim |
| `.specify/scripts/bash/` | Verbatim |

Modifications are marked as such above and dated in `.specify/UPSTREAM.md`; the upstream
authors are not responsible for them.

**MIT permission notice, reproduced in full as that licence requires:**

```
Copyright GitHub, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## obra/superpowers

- **Upstream**: <https://github.com/obra/superpowers>
- **Licence**: MIT
- **Copyright**: Copyright (c) 2025 Jesse Vincent

`skills/diagnose-before-fix/SKILL.md` — redistributed by **both** channels — declares
"systematic debugging (Superpowers, adapted)". The skill is a reimplementation: different
structure (six phases against four), Maestro's own wording, its own anti-pattern references.
But two short elements are close to the upstream's: the Iron Law framing
(*"NO FIX WITHOUT A ROOT-CAUSE INVESTIGATION FIRST"* against *"NO FIXES WITHOUT ROOT CAUSE
INVESTIGATION FIRST"*) and the *"violating the letter violates the spirit"* line.

That is the boundary between an idea (free to reimplement) and expression (not), and it is
not ours to settle: **attribution is given here because erring toward attribution costs a
paragraph and erring away from it costs the obligation.** Whether those two lines are a
derivative work is a question for a professional, not for this file or its gate.

---

## Ideas cited, not redistributed

These carry **no** licence obligation here because no material was copied — only a technique
was learned and reimplemented in Maestro's own words. They are listed so the lineage is not
orphaned (a technique absorbed without provenance cannot be re-evaluated if its source
changes):

| Idea | Source | Where it landed |
|---|---|---|
| EARS (*Easy Approach to Requirements Syntax*) | Kiro (AWS) — technique, documented publicly | `skills/verifiable-dod/SKILL.md`, `.specify/templates/spec-template.md` |

> An idea is not copyrightable; its **expression** is. Reimplementing a technique from
> understanding is free. Translating or closely paraphrasing someone else's text is a
> derivative work and would belong in the section above, not this one.

---

## Build-time only (not redistributed)

`publicar/` uses `markdown-it` and `markdown-it-anchor` (both MIT) to generate the published
site. They are development dependencies resolved from `publicar/package-lock.json`; they are
not copied by the installer and are not part of what Maestro ships.
