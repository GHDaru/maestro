# 017 — Memória persistente de sessão para o agente

- **Id**: `memoria-persistente-de-sessao`
- **Fonte**: `Cline Memory Bank`
- **Observado em**: 2026-08-01
- **Veredito no momento**: observar
- **Destino**: —
- **Gatilho de reavaliação**: sessões de vários dias sobre a mesma intenção começarem a doer — perda de contexto medida, não sentida

## A ideia

Um banco de memória em arquivos que o agente lê no início e atualiza ao fim de cada sessão,
para atravessar o corte de contexto sem perder o que foi decidido.

## Por que atravessa (ou não)

O problema é real e tem nome aqui: corolário C12 — o que sobrevive à compactação é o que
está num artefato consumido; o resto é **apagado**, não degradado. A resposta do Maestro já
é essa: `spec.md`, `plan.md`, `tasks.md` e `qa-report.md` **são** a memória, e o
`check-conformance.sh` mede se ela sobreviveu. Uma segunda camada de memória seria função
duplicada (Princípio VI) — a menos que a dor apareça medida.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | risco de conflito com VI (duplicar a função dos artefatos) |
| 2 | Licença e redistribuição | sem licença declarada na varredura — **citar, nunca copiar** |
| 3 | Função já servida | **sim**: os quatro artefatos do ciclo, mais o portão de conformidade |
| 4 | Custo de contexto | carregar memória a cada sessão custa contexto justamente onde ele falta |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | leitura de terceiros; sem uso nosso |
| 7 | Dor real hoje | não medida — o ciclo cabe no fluxo atual |
