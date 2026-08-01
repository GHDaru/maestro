# QA-report 018 — Instalação visível + UX e jornadas

- **Data**: 2026-08-01 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `verificar-papeis.sh` **com agente removido** | exit ≠ 0 nomeando o papel | **exit 1**, "'UX-agent' é prescrito mas NÃO tem agente" ✅ |
| `verificar-papeis.sh` no estado atual | exit 0 | ✅ 8 papéis + 2 templates |
| `verificar-agentes.sh` | 13 agentes, invariante read-only | ✅ |
| `ls skills/*/SKILL.md` | 6 | ✅ |
| `grep instalar-maestro.sh README.md` | ≥1 | 2 ✅ |
| BPMN com "Ramo de interface" | presente | ✅ (imagem re-renderizada) |
| `pytest` · build do site | verdes | 11 testes · 35 páginas ✅ |

## Os dois achados, com naturezas diferentes

1. **Invisibilidade** (não era ausência): o instalador existia desde o ciclo 013, mas fora
   do ponto de entrada. Para quem chega — humano ou IA — **existir e não estar no README é
   o mesmo que não existir**.
2. **Divergência norma × executável**: o modelo operacional prescrevia UX-agent,
   `ux-design.md` e journey doc havia **catorze ciclos**, sem nada que os entregasse. Nenhum
   `qa-report` pegou porque **ninguém verificava a cobertura da norma** — os checks olhavam
   sempre para dentro do ciclo, nunca para a distância entre o que o modelo manda e o que o
   toolkit tem.

## A fitness function que faltava

`verificar-papeis.sh` fecha essa classe inteira: papel prescrito sem agente, artefato
essencial sem template. Provado falhando antes de ser aceito (segunda lei da
`dod-verificavel`, ciclo 017 — aplicada pela primeira vez desde que virou regra).

**Efeito colateral bem-vindo**: ao subir para 13 agentes, o `verificar-agentes.sh` falhou
sozinho (esperava 12) — a fitness function anterior funcionando como projetada.

## Gate

- Auditoria do Steward; promovido via `promover-main.sh`.
