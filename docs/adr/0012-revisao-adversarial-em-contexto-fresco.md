# ADR 0012 — Cauda Maestro: revisão adversarial em contexto fresco como gate de merge

- **Status**: Aceito · **Data**: 2026-08-11 · **Origem**: prática comprovada no programa `ghdaru`
  (Épico 1, Épico R, spec 029/030/031/032 e o fechamento do Nível 2 APH) · **Decisor**: Steward

## Contexto

O Maestro já tinha o gate humano (Princípio II) e o Test-First (Princípio IV). Mas dois furos
apareceram repetidamente na prática do laboratório `ghdaru`:

1. **O autor é o pior revisor de si mesmo.** Quem escreveu a fatia carrega o contexto que a
   justifica — e é cego às mesmas suposições que o levaram ao bug. Uma revisão feita **na mesma
   conversa** herda esse contexto e tende a **concordar**: vê o código pela lente de quem o
   escreveu, não de quem vai quebrá-lo.
2. **"Verde local ≠ certo global".** Testes passando provam o que foi codificado, não o que foi
   esquecido — nem se a mudança abre um furo de **segurança** (vazamento entre tenants, autorização
   que passa a depender do modelo, mutador que escapa da governança). O CI não pega isso.

O programa `ghdaru` convergiu, sem planejar, num ritual que fechou os dois furos: **antes de todo
merge, dois revisores independentes rodam em contexto FRESCO** (subagentes, sem o histórico da
implementação), um de **correção** e um de **segurança**, cada um instruído a **refutar**, não a
aprovar. Achados classificados (BLOCKER/IMPORTANT/MINOR/NIT); só se aplicam os que sobrevivem;
depois CI verde e squash-merge. Repetido em dezenas de rounds, o padrão pegou bugs reais
(PNGs duplicados que a legenda mentia, `deriveCost` inexistente, matriz de maturidade
superdeclarada, título cru de proposta) e **confirmou** fatias sólidas com um "SECURITY-NEUTRAL"
fundamentado — em ambos os casos, evidência que o autor sozinho não produziria.

## Decisão

Formaliza-se a **Cauda Maestro**: o fecho ritual de toda fatia de risco não-trivial.

1. **Dois revisores em contexto fresco, adversariais.** Antes do merge, disparam-se subagentes de
   contexto limpo (sem o histórico da implementação): **(a) revisão de correção** e **(b) revisão de
   segurança**. Cada um recebe só o diff + o repositório e a instrução de **formar juízo próprio,
   tentando refutar** — não de chancelar. "Trust no prior narrative."
2. **Achados classificados e verificados.** BLOCKER / IMPORTANT / MINOR / NIT, cada um com
   `arquivo:linha` e **cenário concreto de falha** (não opinião). Só entram no código os achados que
   sobrevivem à verificação; NITs de doc/overclaim contam.
3. **A cauda é: revisão → aplicar o que sobrevive → CI verde → squash-merge.** Uma fatia não está
   "pronta" enquanto a cauda não fecha. O gate humano (Princípio II) decide o merge; a revisão fresca
   o **instrui**.
4. **Escala com o risco (Princípio III).** Fatia trivial/reversível: uma revisão, voto único. Fatia
   que toca segurança, governança ou fronteira: as duas revisões, e quando o espaço de falha é largo,
   múltiplos refutadores com lentes distintas (correção, segurança, "reproduz?").
5. **Painel de especialistas para planejamento.** A mesma técnica — vozes independentes em contexto
   fresco — vira instrumento de **decisão de roadmap**: antes de abrir um épico grande, N especialistas
   (protocolo, arquitetura/status, UX) dão parecer paralelo; a síntese humana vira o plano. É a Cauda
   aplicada **à montante** (antes de construir), não só a jusante (antes de mergear).

## Alternativas consideradas

- **Revisão na mesma conversa** — barata, mas herda o contexto do autor e concorda; foi o furo.
- **Só CI + Test-First** — pega regressão, não pega o esquecido nem o furo de segurança/UX/jornada.
- **Revisão humana obrigatória por par** — cara e nem sempre disponível; a revisão fresca por
  subagente **não a substitui**, mas eleva o piso antes de o humano olhar (o humano revisa o
  parecer, não o diff cru).

## Consequências

- ✅ **Cegueira do autor quebrada por construção**: o revisor fresco não sabe por que o código é
  "obviamente certo" — e é isso que o faz achar o bug.
- ✅ **Segurança vira gate, não afterthought**: toda fatia de risco tem um parecer de segurança
  datado e fundamentado (inclusive o "neutro", que é evidência positiva).
- ✅ **Custo de token, não de calendário**: os revisores rodam em paralelo, em minutos; a cauda não
  atrasa o humano, o informa.
- ⚠️ **Custo de tokens/contexto real** — por isso escala com o risco (Princípio III), não é ritual
  universal: fatia trivial não paga dois revisores.
- ⚠️ **Risco de "teatro de revisão"** — revisor fresco mal-instruído chancela. Mitigação: a instrução
  é **refutar** e trazer cenário concreto; parecer sem cenário não conta.

## Verificação

O padrão só vale se deixar rastro: cada fatia de risco fecha com o **parecer registrado** (achados
classificados + verdito de segurança) antes do merge. A ausência do parecer numa fatia de fronteira/
segurança é, ela mesma, um achado da retro.
