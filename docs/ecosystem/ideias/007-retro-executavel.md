# 007 — Retrospectiva como comando, não como reunião

- **Id**: `retro-executavel`
- **Fonte**: `GHDaru/maestro-02`
- **Observado em**: 2026-07-31
- **Veredito no momento**: absorver
- **Destino**: `scripts/retro.sh`
- **Gatilho de reavaliação**: —

## A ideia

`/reflect`: a retrospectiva vira um comando que lê o estado do repositório e responde, em
vez de uma cerimônia de calendário.

## Por que atravessa (ou não)

Bate direto com a rejeição de cerimônia por data (modelo operacional §10). Absorvida, e a
evolução foi além da origem: a retro passou a ser disparada por **dívida** — quatro achados
abertos, ou um aberto há seis ciclos (`check-retro.sh`), e não por cadência. Um achado do
ciclo 041 mostrou que a ferramenta mentia desde o ciclo 011, o que é o argumento mais forte
a favor dela: uma reunião não teria sido auditável.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum; substitui cerimônia por gatilho (Princípio VII) |
| 2 | Licença e redistribuição | material próprio (MIT) |
| 3 | Função já servida | não |
| 4 | Custo de contexto | um script |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | roda desde o ciclo 008; corrigida no 041 depois de mentir por 29 ciclos |
| 7 | Dor real hoje | sim: retro que não acontece porque ninguém marca |
