# QA-report 012 — Apêndice C: panorama exploratório

- **Data**: 2026-08-01 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| Build com o Apêndice C | 23 páginas, links OK | ✅ |
| `grep -c "Triagem"` | ≥ 8 | **9** ✅ |
| `grep -c "https://"` (fontes) | ≥ 8 | **12** ✅ |
| Já julgados não repetidos | remete a ficha/A/B | ✅ (cabeçalho do apêndice) |

## Cobertura

- 9 itens triados em 4 famílias; 2 achados genuinamente novos com gatilho claro
  (**PRP** — 1º ciclo regendo código de produto; **CCPM** — multi-dev com Issues);
  2 descartes fundamentados (multi-CLI, swarm — anti-padrão 4); marketplaces definidos
  como fonte de garimpo por dor, nunca importação em bloco.
- Funil de avaliação formalizado: exploratório → gatilho → hands-on → absorção por gate.

## Gate

- Sem absorção a decidir (triagens = observar/gatilho). Publicado via `promover-main.sh`.
