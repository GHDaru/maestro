# Spec 036 — Pesquisa: o upstream (decompor projeto grande em objetos)

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-03
- **Origem**: pedido do Steward — "na metodologia é muito importante saber o que fazer …
  no upstream temos fragilidades. Faça uma pesquisa sobre skills que ajudem a decompor um
  projeto maior em objetos e avalie a possibilidade de gerarmos skills, scripts, etc."

> **Raia**: plena. **Ambiguidade** alta (a pergunta é aberta: nem o objeto certo era
> conhecido); **raio** amplo (a resposta muda o método a montante da spec, e o método é o
> produto); **irreversibilidade** baixa (é pesquisa, e nada foi construído).

## O quê e por quê

O Maestro é forte do `spec.md` para a frente e não tem **nada** a montante: nenhum agente,
skill, template ou portão ajuda a ir de uma intenção grande até o conjunto de ciclos.
Medida do próprio repositório: **20 das 34 specs nasceram de pedido pontual**, não de um
corte planejado — funcionou porque o dono do escopo está na sala, e é exatamente o que não
escala para um produto com terceiros.

## Requisitos funcionais

- **FR1**: A pesquisa DEVE fichar as fontes com **link primário** e veredito explícito
  (adotar · absorver · observar · descartar), no padrão de `docs/research/`.
- **FR2**: A pesquisa DEVE medir o gap no **próprio repositório**, não afirmá-lo.
- **FR3**: QUANDO uma fonte tiver licença incompatível com a nossa distribuição, O SISTEMA
  DEVE declará-lo antes de qualquer proposta de uso.
- **FR4**: A proposta DEVE caber em **um objeto, um verbo e um portão** — pirâmide de
  PRD/épico/história fica explicitamente fora.
- **FR5**: A proposta DEVE declarar seus riscos, inclusive o de que o gap não se pague neste
  repositório.

## Fora de escopo

- **Implementar** a skill, o template, o script ou o gate: isso é ciclo próprio, e só
  acontece com dor real (regra de nascimento das skills).
- Adotar qualquer framework de terceiros por inteiro.

## Critérios de aceite (DoD)

- [x] Fichamento com ≥12 fontes primárias linkadas e veredito por família
- [x] Gap medido por comando (34 specs, 20 de origem pontual, zero cobertura upstream)
- [x] Licença do `Product-Manager-Skills` (CC BY-NC-SA) declarada e tratada
- [x] Proposta em um objeto (`outcome`), um verbo (skill `slice-outcome`) e um portão
      (`check-outcomes.sh`), com o que **não** faremos
- [x] Recomendação com **gatilho**: construir só quando houver intenção grande real

## Clarify

1. Adotar já ou esperar dor? → **recomendação com gatilho** (seção 6 da pesquisa): a decisão
   é do Steward no gate.
2. Copiar as 70 skills de produto encontradas? → **não**: licença CC BY-NC-SA é incompatível
   com a nossa distribuição MIT; entram como fonte citada.
