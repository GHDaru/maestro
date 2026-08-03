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
| [`check-language.sh`](./check-language.sh) | Portuguese residue in the installable surface (ADR 0014) | After touching agents, skills, scripts, templates or governance | Nothing — it only reports the leftovers |
| [`check-cycle.sh`](./check-cycle.sh) | Lane declared **and justified** by the three factors, the lane distribution, and every commit ahead of `main` citing its cycle | Before closing any cycle | Whether the lane is *right* — it demands the rationale and shows the skew |
| [`check-links.sh`](./check-links.sh) | Every relative link in the repository resolves — including outside the published pages | After any rename or move | Nothing — it only reports |
| [`check-retro.sh`](./check-retro.sh) | Open-finding debt: fails with ≥4 open, or one open for ≥6 cycles | Any time; it is the retrospective trigger | The retrospective itself — that stays human |
| [`check-chapters.sh`](./check-chapters.sh) | The editorial Iron Law as an executable: nine sections in order, dating, and the starred section with real evidence | When migrating or editing a book chapter | The merit of the text — only the skeleton |
| [`retro.sh`](./retro.sh) | Pre-computes the retrospective material (cycles, verdicts, pending gates, decisions, inventory) | In the end-of-cycle retrospective | The answers — the retrospective stays human |
| [`record-decision.sh`](./record-decision.sh) | Appends a decision to `docs/records/decisoes.jsonl` (append-only, validates the JSON) | When accepting an ADR or deciding a gate | The merit — it only records what the human decided |
| [`install-maestro.sh`](./install-maestro.sh) | Installs the complete method into another repository; `--block` prints the instruction for `CLAUDE.md` | When taking Maestro to a project | It never overwrites; `--dry-run` shows first |
| [`package-plugin.sh`](./package-plugin.sh) | Builds `plugin/maestro/` (Claude Code) from the sources; `--verify` proves they are in sync | After changing an agent, skill or command | Nothing — it repackages or reports the divergence |

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
