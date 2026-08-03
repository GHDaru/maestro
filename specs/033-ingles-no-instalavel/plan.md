# Plan 033 — Inglês no método instalável

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-02

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da execução; requisitos em EARS |
| II. Orquestração humano-governada | ✅ o escopo foi decisão do Steward, feita antes de qualquer renome |
| III. Reversibilidade / gates de risco | ✅ renome versionado (`git mv`), tudo reversível por revert; gate humano ao final |
| IV. Test-First / DoD verificável | ✅ `check-language.sh` escrito e **provado falhando** antes de valer |
| V. Economia de contexto / fronteira | ✅ a fronteira é o que o instalador copia — a mesma lista do script |
| VI. Artefatos vivos | ✅ referências atualizadas no mesmo PR; portão de links do livro verde |
| VII. Governança leve / YAGNI | ✅ nenhuma ferramenta de i18n; um script de 50 linhas |
| VIII. Comunicação inteligível | ✅ IA, ADR, DoD e EARS por extenso na primeira ocorrência |

## Como

1. **Definir a fronteira pela lista do instalador**, não por intuição: o que
   `install-maestro.sh` copia é o que precisa estar em inglês. A fronteira do check é a
   mesma — assim os dois não divergem.
2. **Renomear com `git mv`** (histórico preservado) e só então traduzir o conteúdo.
3. **Varredura mecânica de referências** em `docs/`, `publicar/`, `.github/`, `CLAUDE.md`,
   `README.md`, `companion/` — deixando `specs/` intocado (registro histórico).
4. **Escrever o `check-language.sh` medindo resíduo**, não "é inglês" — e declarar esse
   limite no cabeçalho do próprio script (anti-padrão 13: saiba o que seu check mede).
5. **Exceção visível**: linha que precisa de português declara `PT-DATA` nela mesma; nada
   de allowlist escondida em outro arquivo.
6. **Reempacotar o plugin** e rodar o portão de links do livro, que é quem acusa renome mal
   propagado.

## Verificação (DoD)

```bash
scripts/check-language.sh            # 13 caminhos, exit 0 (nasceu vermelho nos READMEs)
scripts/check-agents.sh              # 13 agentes com nomes novos
scripts/check-roles.sh               # papéis × agentes; princípios × Constitution Check
scripts/check-install.sh             # método instalado e coerente
scripts/package-plugin.sh --verify   # plugin sincronizado
node publicar/build.mjs              # 35 páginas, links OK
scripts/install-maestro.sh --block   # bloco em inglês com as 6 skills
```
