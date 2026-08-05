# Plan 036 — Pesquisa do upstream

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-03

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da pesquisa; requisitos em EARS |
| II. Orquestração humano-governada | ✅ a pesquisa **não decide**: entrega veredito para o gate do Steward |
| III. Reversibilidade / gates de risco | ✅ nada construído; a decisão de adotar é o gate |
| IV. Test-First / DoD verificável | ✅ critérios contáveis (fontes linkadas, gap medido por comando) |
| V. Economia de contexto / fronteira | ✅ pesquisa num documento; implementação seria outro ciclo |
| VI. Artefatos vivos | ✅ fichamento em `docs/research/` com data e ciclo |
| VII. Governança leve / YAGNI | ✅ a recomendação é **não construir sem dor real** |
| VIII. Comunicação inteligível | ✅ siglas por extenso; nomes das técnicas explicados |

## Como

1. **Medir o gap antes de pesquisar** — origem declarada das 34 specs, cobertura do toolkit
   a montante. Sem isso a pesquisa vira opinião sobre um problema suposto.
2. **Varrer quatro famílias**, não uma: frameworks agênticos com upstream (BMAD, Agent OS,
   Spec Kit), skills publicadas no padrão `SKILL.md`, relatos de campo sobre decomposição
   para agentes, e a literatura clássica de fatiamento e descoberta.
3. **Veredito por item** com o mesmo critério de sempre (consumidor + forcing function,
   corte por fronteira, menor cerimônia que resolve) — e licença checada antes de propor uso.
4. **Propor o mínimo**: um objeto, um verbo, um portão, um gate humano — e escrever o que
   **não** será feito, que é o que impede a proposta de virar pirâmide.

## Verificação (DoD)

```bash
ls specs/*/spec.md | wc -l                            # 34 — a base da medida
grep -c "https://" docs/research/upstream-decomposicao.md   # fontes linkadas
scripts/check-links.sh ; scripts/check-language.sh ; node publicar/build.mjs
```
