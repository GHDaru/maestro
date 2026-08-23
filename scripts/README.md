# Maestro scripts

Scripts of the **repeated ritual** — they take the mechanical step away from the
Orchestrator's attention (the bottleneck) without taking away the **decision**. Each one was
born from real pain in a retrospective, never from speculation.

| Script | What it does | When to use it | What it does NOT decide |
|---|---|---|---|
| [`promote-main.sh`](./promote-main.sh) | `dev → main` plus push with exponential backoff | After the **human merge gate** | **Whether** to promote — it asks for confirmation and aborts on a dirty tree |
| [`new-cycle.sh`](./new-cycle.sh) | Creates `specs/NNN-slug/` with the four skeleton artifacts | When opening a new cycle | The content — only the skeleton; you fill it in |
| [`check-agents.sh`](./check-agents.sh) | Runs the subagent invariants (count, front matter, read-only) | Before calling an agent cycle done | Nothing — it only reports; exit ≠ 0 when something breaks |
| [`check-roles.sh`](./check-roles.sh) | Role prescribed in the model × agent that exists; essential artifact × template; constitution principles × Constitution Check rows | Before closing a cycle that touches roles | Nothing — it only reports |
| [`check-install.sh`](./check-install.sh) | Is the method installed **for real** here? layers, the instruction the AI reads, every skill visible | In this repository and in every project that receives the method | Nothing — it only reports; exit ≠ 0 when the AI was not instructed |
| `check-language.sh` ¹ | Portuguese residue in the installable surface (ADR 0014) | After touching agents, skills, scripts, templates or governance | Nothing — it only reports the leftovers |
| `check-cycle.sh` ¹ | Lane declared **and justified** by the three factors, the lane distribution, and every commit ahead of `main` citing its cycle | Before closing any cycle | Whether the lane is *right* — it demands the rationale and shows the skew |
| [`check-links.sh`](./check-links.sh) | Every relative link in the repository resolves — including outside the published pages | After any rename or move | Nothing — it only reports |
| [`check-retro.sh`](./check-retro.sh) | Open-finding debt: fails with ≥4 open, or one open for ≥6 cycles | Any time; it is the retrospective trigger | The retrospective itself — that stays human |
| `check-chapters.sh` ¹ | The editorial Iron Law as an executable: nine sections in order, dating, and the starred section with real evidence | When migrating or editing a book chapter | The merit of the text — only the skeleton |
| [`check-conformance.sh`](./check-conformance.sh) | Are you following Maestro? Declared artifacts and the closing tail **with evidence**. `--ticked-only` is the blocking half: a ticked box must have its evidence | Before closing a cycle; `--ticked-only` runs in CI | Quality — only whether the method survived into the artifacts |
| `check-boundary.sh` ¹ | What belongs in this repository and what does not, plus every publication channel | After adding a page, a material or a channel | Where a new thing *should* live — it reports the ones out of place |
| [`check-ecosystem.sh`](./check-ecosystem.sh) | The third-party catalogue: the idea as the unit, moment separate from state, and absorbing requires a real destination | After judging or absorbing an outside idea | The judgement — it demands the evidence for it |
| [`check-evals.sh`](./check-evals.sh) | The baseline for non-deterministic output exists and is readable | After touching an agent that judges | Whether the output is *good* — it checks the baseline exists |
| `check-licensing.sh` ¹ | Our licence, the third-party attributions, and that both travel through **every** redistribution channel | After adding a dependency or a channel | The choice of licence |
| `check-flags.sh` ¹ | The flags and subcommands a parser accepts × the ones the documentation promises, both directions | After adding a flag or a subcommand anywhere | Whether the flag is a good idea |
| [`retro.sh`](./retro.sh) | Pre-computes the retrospective material (cycles, verdicts, pending gates, decisions, inventory) | In the end-of-cycle retrospective | The answers — the retrospective stays human |
| [`record-decision.sh`](./record-decision.sh) | Appends a decision to `docs/records/decisoes.jsonl` (append-only, validates the JSON) | When accepting an ADR or deciding a gate | The merit — it only records what the human decided |
| `install-maestro.sh` ¹ | Installs the complete method into another repository; `--block` prints the instruction for `CLAUDE.md` | When taking Maestro to a project | It never overwrites; `--dry-run` shows first |
| [`check-adr.sh`](./check-adr.sh) | Decision index × ADRs on disk: every ADR listed, every listing real, and the status in the index agreeing with the status in the ADR | After writing or superseding an ADR | The merit of the decision — it only reports the divergence |
| `check-version.sh` ¹ | One version, in every place that states one: the newest released heading in the CHANGELOG against the front page, the roadmap header and the packaged plugin | When cutting a version | Whether the number is the RIGHT one — semantic versioning is a human judgement |
| `check-installed.sh` ¹ | Installs into an empty directory and exercises the result: every shipped gate runs green there, and every method path a shipped file names exists there | After touching the installer, a command, a skill or any installable file | Nothing — it only reports the incoherence |
| `package-plugin.sh` ¹ | Builds `plugin/maestro/` (Claude Code) from the sources; `--verify` proves they are in sync | After changing an agent, skill or command | Nothing — it repackages or reports the divergence |

¹ **Does not travel with the installation.** These belong to the Maestro repository itself —
they guard the book, the internal boundary, the licence, the plugin and the installer, none
of which a project that installed the method has. Written as plain names, not links, because
this file **is** installed: a link here would resolve to nothing there (cycle 048).

## Principle (II + III)

The script performs the **mechanical** part; the **gate stays human**. `promote-main.sh` does
**not** promote by itself: it shows the commits, asks for confirmation (or an explicit
`--yes`) and aborts when the tree is dirty or `dev` is not ahead of `main`. Automating the
*execution* of the ritual saves attention; automating the *decision* would violate
Principle II.

## Quick start

```bash
scripts/new-cycle.sh 007 vendor-spec-kit   # opens the next cycle
scripts/check-agents.sh                    # agent fitness functions
scripts/check-install.sh                   # is the method really installed here?
scripts/promote-main.sh                    # promotes after the "yes" (it asks first)
```
