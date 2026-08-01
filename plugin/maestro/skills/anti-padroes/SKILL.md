---
name: anti-padroes
description: Catálogo do que NÃO fazer ao operar humano+agentes — os erros recorrentes observados nas nossas retros e no ecossistema. Use quando estiver desenhando um fluxo/prompt/orquestração, revisando o trabalho de um agente, ou quando algo "funciona mas cheira mal" e você precisa nomear o anti-padrão antes de corrigir.
---

# Anti-padrões (o catálogo do "não faça")

## Iron Law

```
NOMEIE O ANTI-PADRÃO ANTES DE CORRIGI-LO
```

**Violar a letra desta regra é violar o espírito dela.** Corrigir sem nomear conserta o
sintoma uma vez; nomear ("isso é o 4") liga ao catálogo, encurta a conversa e alimenta a
retro — que decide se vira regra.

Regra positiva diz o caminho; anti-padrão marca o precipício. Este catálogo é **vivo**:
todo anti-padrão novo entra pela retro (erro recorrente observado), nunca por especulação.

## De contexto

1. **Despejo de contexto** — colar o codebase/documento inteiro no prompt. Fatie pelo
   papel/task (Princípio V); reporte a economia quando possível (handbook cap. 04).
2. **Contexto tribal** — intenção que só existe na cabeça de quem opera. Se não está na
   spec, o agente não sabe — e outro humano também não.
3. **Reset preguiçoso** — nem sempre `/clear` resolve; resetar demais perde aprendizado,
   resetar de menos acumula lixo. O gatilho é o papel mudar, não o turno.

## De orquestração

4. **Multi-agente para problema de agente único** — orquestração tem custo (handoffs,
   reconciliação). Use a **menor autonomia que resolve** (handbook cap. 05).
5. **Retry cego** — repetir o mesmo prompt esperando resultado diferente. Se falhou 2x,
   o problema é o prompt/contexto/task — mude algo antes de tentar de novo.
6. **Autor-revisor** — o agente que escreveu aprovando o próprio trabalho. Revisão é em
   **contexto fresco**, sempre (regra operacional 2).

## De qualidade

7. **"Parece que funciona"** — entregar sem avaliação executável. Prove, não declare:
   teste verde, build limpo, evidência anexada (DoD).
8. **Caminho feliz apenas** — sem teste de falha, sem tratamento de erro. Mínimo: 1 feliz
   + 1 falha por caso de uso.
9. **Meta numérica gameável** — "cobertura ≥ X%" convida a teste inútil. Critério é
   comportamento verificável, não percentual.

## De processo

10. **Mudança silenciosa de escopo** — o agente "aproveita para" refatorar. Diff pequeno
    e focado; problema maior vira registro, não desvio.
11. **Cerimônia de papel** — processo que não muda decisão nenhuma (daily de um, backlog
    infinito). Se um gate nunca reprova nada, ele é teatro — poda (YAGNI).
12. **Corrigir a mesma coisa duas vezes** — correção recorrente que não virou regra
    versionada. A retro existe para isso; repetir correção é falha de processo, não do
    agente.

## De verificação

13. **Check que mede o proxy, não o fato** — o comando passa, mas prova outra coisa.
    Sintomas: casa com o *texto* em vez do artefato (`grep -l companion` acha a palavra
    escrita na página, não o widget injetado); conta *linhas* em vez de itens
    (`grep -c "https://"` reporta 5 onde há 6 fontes); confirma que a *seção existe* em
    vez de que ela *está atualizada* ("avaliação heurística presente" ≠ "revisitada com
    data nova"). **Antídoto**: prove o check **falhando** antes de confiar nele — se você
    não viu o check acusar, não sabe o que ele mede (ver skill `dod-verificavel`).

## De processo (continuação)

14. **Achado que morre em "candidato"** — registrar "candidato a regra" no relatório e não
    executar a retrospectiva. O ciclo `retro → regra versionada` só existe se for
    **rodado**; anotação sem cerimônia é dívida silenciosa.
15. **Artefato de planejamento que congela** — roadmap/mapa que para de ser atualizado
    enquanto os ciclos avançam. Vira ficção: descreve um projeto que não é mais o seu
    (Princípio VI — artefato vivo ou morto, não há meio-termo).

## Como usar

- **Desenhando**: percorra o catálogo como checklist negativo (nenhum item presente?).
- **Revisando**: nomeie o anti-padrão pelo número — "isso é o 4" encurta a conversa.
- **Na retro**: erro recorrente novo → nova entrada aqui (com o ciclo de origem).

**Fontes:** retros dos ciclos 001–008 · catálogo "workflow slop" do
[maestro-02/sharpdeveye](https://github.com/GHDaru/maestro-02) (adaptado — ver Apêndice A
do handbook) · princípios I–VII.
