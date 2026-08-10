# 014 — Rastreabilidade pelas *issues* do repositório

- **Id**: `rastreabilidade-via-issues`
- **Fonte**: `CCPM`
- **Observado em**: 2026-08-01
- **Veredito no momento**: observar
- **Destino**: —
- **Gatilho de reavaliação**: projeto com mais de um desenvolvedor humano, usando *issues* como coordenação real

## A ideia

O rastro de "o que está sendo feito e por quem" mora nas *issues* da plataforma, e os
agentes as consomem e atualizam, em vez de manter um estado paralelo em arquivos.

## Por que atravessa (ou não)

A segunda ideia genuinamente nova do panorama. Hoje há **um** humano regendo, e a
rastreabilidade vive em `specs/NNN-*/` + `decisoes.jsonl`, que é auditável e não depende de
plataforma. Com mais de um humano, o estado passa a precisar de um lugar que os dois vejam —
e aí a dimensão 7 muda de resposta.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | atenção: acoplaria a rastreabilidade a uma plataforma (Princípio III) |
| 2 | Licença e redistribuição | sem licença declarada na varredura — **citar, nunca copiar** |
| 3 | Função já servida | sim, para um humano: `specs/` + índice de decisões |
| 4 | Custo de contexto | médio: chamadas de API por task |
| 5 | Reversibilidade | baixa: o histórico ficaria na plataforma |
| 6 | Maturidade e evidência | leitura de terceiros; sem uso nosso |
| 7 | Dor real hoje | **não**: um humano, um repositório |
