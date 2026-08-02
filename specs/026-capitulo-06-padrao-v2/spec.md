# Spec 026 — Capítulo 06 (papéis e RACI) no padrão v2

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática (um capítulo por ciclo).

## O quê e por quê

O capítulo dos papéis explicava bem a teoria — RACI adaptado, o A indelegável, a armadilha
do funil — e provava nada. Justamente aqui a evidência é forte: a independência do
verificador é uma **linha de configuração** (o revisor não tem `Write`), o responsável final
humano deixa **21 gates registrados**, e a lacuna "papel prescrito sem executável" já
aconteceu de verdade e virou fitness function.

## Requisitos funcionais

- **FR1**: O capítulo DEVE cumprir as nove seções com datação (verificado por script).
- **FR2**: A seção ⭐ DEVE mostrar a independência do verificador como **estrutura
  verificável** (ferramentas negadas + fitness function), não como recomendação.
- **FR3**: QUANDO o capítulo afirma que o responsável final humano deixa rastro, O SISTEMA
  DEVE poder contar os gates registrados por comando.
- **FR4**: O capítulo DEVE contar o caso real do papel prescrito sem executável (ciclo 018)
  e a verificação que nasceu dele.

## Fora de escopo

- Alterar a matriz de papéis do modelo operacional · migrar 07–12 (um por ciclo).

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh`: 7 migrados, 6 pendentes, exit 0
- [x] O laço citado no capítulo reproduz exatamente `guardiao-processo`, `review`, `security`
- [x] `grep -c '"id": "gate-main'` devolve o 21 citado
- [x] Site sem link quebrado

## Clarify

1. Citar RACI por extenso? → **sim**, Princípio VIII: sigla nunca nasce nua.
