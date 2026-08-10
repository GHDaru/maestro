# 028 — Bootstrap do enforcement na instrução do projeto

- **Id**: `bootstrap-de-enforcement`
- **Fonte**: `obra/superpowers`
- **Observado em**: 2026-07-31
- **Veredito no momento**: absorver
- **Destino**: `CLAUDE.md`
- **Gatilho de reavaliação**: —

## A ideia

A primeira coisa que o agente lê manda ele consultar as skills antes de agir. Sem esse
parágrafo, as skills existem no disco e não existem no comportamento.

## Por que atravessa (ou não)

Absorvido como o "skills primeiro" do `CLAUDE.md`, e depois endurecido além da origem: a
instrução é **gerada do disco** (`--block`, ADR 0013), porque lista escrita à mão envelhece
em silêncio — foi a falha do ciclo 021. E o `check-install.sh` falha enquanto o
`CLAUDE.md`/`AGENTS.md` não apontar para o método: copiar arquivos não é instalar.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum |
| 2 | Licença e redistribuição | MIT na origem; parágrafo nosso, gerado |
| 3 | Função já servida | não à época |
| 4 | Custo de contexto | um parágrafo |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | com portão (`check-install.sh`) desde o ciclo 021 |
| 7 | Dor real hoje | sim: skill instalada e nunca consultada |
