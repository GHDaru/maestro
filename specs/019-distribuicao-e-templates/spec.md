# Spec 019 — Distribuição em três camadas + templates faltantes

- **Status**: Aprovada · **Raia**: Plena · **Data**: 2026-08-01
- **Origem**: perguntas do Steward após o ciclo 018 — "já atualizou tudo? já criou os
  templates? precisamos de um padrão? podemos buscar padrões na comunidade? como fazer um
  instalador similar ao Spec Kit?"

## O quê e por quê

Duas frentes:

1. **Templates faltantes**: auditoria encontrou **ADR** (Registro de Decisão de
   Arquitetura) e **qa-report** sem template — dois artefatos usados em **todo** ciclo,
   reescritos à mão desde o 003. O `verificar-papeis.sh` não pegou porque olhava só os
   artefatos marcados "essencial" na tabela do modelo.
2. **Distribuição**: o instalador existia mas era só um script local. A comunidade
   consolidou padrões (skills CLI, plugin de marketplace) e o Spec Kit tem CLI próprio —
   era preciso decidir o que adotar, com evidência.

## Requisitos funcionais

- **FR1**: templates `adr-template.md` e `qa-report-template.md`, cada um carregando as
  regras que o método exige (ADR imutável e com consequências negativas explícitas;
  qa-report com resultado **real** por check).
- **FR2**: pesquisa dos padrões da comunidade (agente `curador-pesquisa`) com fontes.
- **FR3**: **camada B** — plugin do Claude Code: `scripts/empacotar-plugin.sh` gera
  `plugin/maestro/` das fontes canônicas; `.claude-plugin/marketplace.json` publica.
- **FR4**: **camada C** — compatibilidade com `npx skills add` **verificada** (layout
  `skills/<nome>/SKILL.md` com `name`+`description`).
- **FR5**: **fitness function** `empacotar-plugin.sh --verificar` — falha quando o pacote
  diverge das fontes.
- **FR6**: ADR 0012 com o comparativo e o racional de **não** construir CLI próprio.
- **FR7**: README e receita com os três caminhos, dizendo o que cada um **não** leva.

## Fora de escopo

- Publicar no marketplace comunitário da Anthropic (decisão do Steward, exige submissão).
- CLI próprio estilo Spec Kit — descartado com racional no ADR 0012.

## Critérios de aceite (DoD)

- [ ] QUANDO uma fonte (agente/skill/comando) mudar sem reempacotar, O SISTEMA DEVE falhar
      `empacotar-plugin.sh --verificar` com código ≠ 0 apontando o arquivo. *(provar falhando)*
- [ ] `ls .specify/templates/*.md | wc -l` = 10 (inclui ADR e qa-report).
- [ ] `plugin/maestro/` tem 13 agentes, 6 skills, 11 comandos e manifesto JSON válido.
- [ ] `marketplace.json` é JSON válido e aponta para o plugin.
- [ ] README documenta os três caminhos com o limite de cada um.

## Clarify (resolvido)

1. **CLI próprio?** Não — ~6.900 linhas no Spec Kit para entregar o que um script de 90
   linhas entrega. YAGNI, com o racional registrado no ADR.
2. **Duplicação do plugin?** Aceita e **verificada**: fonte canônica em `.claude/` e
   `skills/`; pacote gerado; check de sincronia bloqueia divergência.
