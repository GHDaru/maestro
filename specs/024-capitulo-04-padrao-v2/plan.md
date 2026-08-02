# Plan 024 — Capítulo 04 no padrão v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição, requisitos em EARS |
| II. Orquestração humano-governada | ✅ gate de merge humano ao final |
| III. Reversibilidade / gates de risco | ✅ documento; `git revert` desfaz |
| IV. Test-First / DoD verificável | ✅ esqueleto cobrado por `verificar-capitulos.sh` |
| V. Economia de contexto / fronteira | ✅ é o tema — e o capítulo mede em vez de afirmar |
| VI. Artefatos vivos | ✅ datação; números reproduzíveis por comando |
| VII. Governança leve / YAGNI | ✅ nenhuma ferramenta nova |
| VIII. Comunicação inteligível | ✅ IA, DoD e siglas por extenso na primeira ocorrência |

## Como

1. Medir antes de escrever: `wc -l .claude/agents/*.md`, `grep "^tools:"`, varredura de
   menções a cada agente nos registros dos ciclos.
2. Reorganizar a teoria correta do capítulo antigo (uma restrição, quatro respostas;
   ótimo local; contexto que sustenta) nas nove seções.
3. Trocar a seção "economia medida" (que era recomendação) por evidência real: os arquivos
   dos agentes e a fitness function que impede o somente-leitura de escrever.

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh          # 5 migrados, exit 0
wc -l .claude/agents/*.md | tail -1     # 267 total, citado no capítulo
grep -H "^tools:" .claude/agents/review.md   # sem Write/Edit, citado no capítulo
node publicar/build.mjs
```
