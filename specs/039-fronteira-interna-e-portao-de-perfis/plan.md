# Plano 039 — Fronteira interna e portão para os perfis de agente

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-06

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-driven | Spec antes; FR2–FR5 viraram as quatro condições do portão novo. |
| II. Orquestração governada | A reversão é decisão humana registrada; o portão não julga papel — compara documento com disco. |
| III. Reversibilidade / gates | FR4 existe **para** este princípio: a coluna de tools é a promessa de que quem julga não escreve. Sem portão, um agente ganha `Edit` e o índice segue dizendo "read-only ✅". |
| IV. Test-first / DoD verificável | Portão escrito antes e visto acusar nas quatro condições, incluindo a de tools. |
| V. Economia de contexto / fronteira | Duas mudanças pequenas, sem reestruturação de `docs/` — os três incômodos menores ficaram fora com razão escrita. |
| VI. Artefatos vivos | O ponto do ciclo: `docs/agents/README.md` passa de documento que ninguém consome (C9) para entrada de um portão. E o ADR revertido deixa de afirmar o que não vale. |
| VII. Governança leve / YAGNI | Nenhum artefato novo: o vínculo estrutural (links markdown) já existia no índice; só passou a ser lido por máquina. |
| VIII. Comunicação inteligível | ADR, DoD, FR por extenso na primeira ocorrência de cada artefato. |

## Como

**Parte A — a reversão.** ADR é imutável, então o 0017 mantém o corpo e ganha status
"Superado pelo ADR 0018", com a razão na mesma linha. O 0018 registra a medição que mudou
a decisão — inclusive a correção do próprio número (o acoplamento bruto de 40% caiu para
20% quando descontada a burocracia que toda entrega toca).

`boundary.json` muda de vocabulário: `repos` → `domains`, `mirrored` → `shared`, e os nomes
`maestro`/`maestro-guia` viram rótulos de domínio. `check-boundary.sh` acompanha — inclusive
as mensagens, que falavam em "o dia da divisão". **A terceira invariante muda de razão, não
de valor**: já não protege contra perder páginas na mudança; protege contra o site publicar
um documento voltado a máquina que ninguém declarou público.

**Parte B — o portão dos perfis.** O vínculo é **estrutural**: o índice já liga papel →
arquivo por link markdown (`../../.claude/agents/<slug>.md`). O portão lê o link, não o
rótulo em prosa — rótulo lido como prosa seria checar a palavra, não o fato (anti-padrão 13).

Quatro comparações, nos dois sentidos:

| # | Condição | O que impede |
|---|---|---|
| 1 | agente no disco ausente do índice | agente invisível para quem lê |
| 2 | índice apontando para arquivo inexistente | perfil de agente que não existe |
| 3 | *tool* no disco fora da linha do índice | **o caso caro**: agente ganha `Edit` e o índice segue dizendo read-only |
| 4 | total declarado em prosa ≠ contagem no disco | leitor aprender o tamanho errado |

## Verificação (DoD)

```bash
scripts/check-roles.sh       # 4 condições novas + as 3 antigas
scripts/check-boundary.sh    # domínios internos, 3 invariantes
scripts/check-retro.sh       # dívida coerente depois das correções de registro
scripts/check-links.sh · check-language.sh · check-install.sh · node publicar/build.mjs
```

Prova de que o portão acusa: quatro injeções deliberadas (remover `security` do índice;
apontar para `fantasma`; dar `Edit` ao `review` no disco; declarar 12 em vez de 13), cada
uma com a saída no `qa-report.md`.
