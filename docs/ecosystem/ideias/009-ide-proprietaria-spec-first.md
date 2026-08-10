# 009 — Adotar a IDE agêntica spec-first como ferramenta

- **Id**: `ide-proprietaria-spec-first`
- **Fonte**: `Kiro (AWS)`
- **Observado em**: 2026-07-30
- **Veredito no momento**: descartar
- **Destino**: —
- **Gatilho de reavaliação**: —

## A ideia

Adotar a ferramenta inteira: uma IDE que gera `requirements.md` / `design.md` / `tasks.md` a
partir de um prompt, com *steering* e *hooks*.

## Por que atravessa (ou não)

A estrutura espelha o nosso spec/plan/tasks, e a melhor parte dela — EARS — atravessou
sozinha ([001](001-ears.md)). A ferramenta não: é proprietária, presa a uma IDE e ao
ecossistema de uma nuvem. Reversibilidade é princípio aqui, e *lock-in* de IDE é o oposto.
**A dimensão 5 reprova sozinha**, sem precisar das outras.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | sim: Princípio III (reversibilidade) e ferramenta única (ADR 0005) |
| 2 | Licença e redistribuição | proprietária — **citável, não copiável** |
| 3 | Função já servida | sim: o Spec Kit é o motor |
| 4 | Custo de contexto | irrelevante diante do conflito |
| 5 | Reversibilidade | **baixa** — *lock-in* de IDE e de nuvem |
| 6 | Maturidade e evidência | madura, e isso não muda o veredito |
| 7 | Dor real hoje | não |
