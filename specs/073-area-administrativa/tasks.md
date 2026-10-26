# Tasks 073 — Área administrativa do Maestro (rodada 1: pesquisa de plataformas)

## Rodada 3 — wireframes das 13 ENTRA sobre o mapa de contextos (25/10, mandato do regente)

`[[TASK id=073-rodada-3 kind=implement cycle=073 attempt=1]]`

> Rodada 2 ACEITA; os 12 termos RATIFICADOS com a condição de que a entrada do glossário resolva as
> cinco colisões de nome do mapa. Entrega em `specs/073-area-administrativa/prototipo/`.

- [x] T3-glossario — Worker01: os 12 termos em `docs/governance/glossary.md` (inglês, coluna
      "Cycle 073"), resolvendo as cinco colisões (sessão de agente × agente; fila de decisões ×
      fila outbox; livro de mensagens × livro de ponto; caixa de entrada como objeto da
      Mensageria; portão do chamado reaproveitado pela Regência via camada anticorrupção).
      **Entregue: `ebe7eb9`, integrado em `853a1d5` — acréscimo puro (+12/−0), grafia batendo com
      o `data-rotulo` das telas, colisões com `arquivo:linha` do mapa §7 (:292–296) + regra
      operativa "fila e portão nunca nus"; MCP/A2A expandidos (Princípio VIII). Prova medida:
      allowlist 74→86; com a lista embutida vazia, as 4 telas da Mensageria com ZERO achado de
      rótulo — a 1ª coluna cobre todos os data-rotulo reais.**
- [x] T3-telas-administracao — Worker04: contexto Administração — catálogo de
      skills/ferramentas/modelos (ENTRA), políticas allow/deny/ask (ENTRA), limites de orçamento
      (ENTRA); cadastro de agentes e papéis aparece como registro existente (NÃO PRECISA), sem
      funcionalidade nova.
      **Entregue: `5ce4a5f`, integrado em `00c1ae9` — 3 wireframes estáticos; agentes/papéis como
      coluna de contexto somente-leitura (NÃO PRECISA honrado); auto-checagem própria com 9 regras
      E mutação 9/9 (mesmo falso-positivo de substring que o smoke test do Gerente achou — "Mod" ⊂
      "motor" — corrigido antes de entregar); interpretações declaradas (moldura × domínio; F2–F7
      e F10–F12 n/a). Fitness do Gerente (v3): 23 achados (18 citação-sem-atributo + 5 rótulo de
      domínio sem data-rotulo) — correção attempt=2 entregue (`7147f50`, integrada em `01b55f6`):
      `data-referencia` na migalha/rodapé + `data-rotulo` nos th e no h1 (→OPA); fit073 e mut073
      re-rodados PASS; **verde nas 3 telas**.**
- [x] T3-telas-workflow — Worker05: contexto Workflow de sessões — sessão de agente
      (subir/derrubar), estado do agente vivo, tarefa aberta, consumo por agente; última atividade
      como coluna existente (NÃO PRECISA).
      **Entregue: `365f59d` + `fc183ce` (evidência no qa-report), attempt=2 por redespacho — o
      attempt=1 ficou 24h sem avanço (branch parada em `e51b3f5`, sessão idle) e o regente mandou
      redespachar com o contrato completo; W05 respondeu dentro da rodada, partindo de `c3137e2`
      (ff ok). 4 wireframes estáticos no contrato de marcação (data-fonte por bloco — retirou o
      data-fonte do `<body>` que isentaria a tela inteira; data-rotulo com termo ratificado;
      data-exemplo com "(exemplo)"; `—` sempre com motivo; F1/F7/F8/F9 valem, F2–F6 e F10–F12 n/a
      declaradas; Princípio VIII). "Última atividade" declarada NÃO PRECISA nas próprias telas.
      Self-check: 11 telas, 0 achados, exit 0. Divergência de nome de arquivo (slug sem prefixo ×
      mensageria-NN/administracao-) declarada — decisão de uniformidade é do regente, rodada 4.
      Tokens (piso): ≈2,56M.**
- [x] T3-telas-mensageria — Worker03 (prioridade): contexto Mensageria — caixa de entrada, livro
      de mensagens, roteamento por nome/ref com a colisão de nomes VISÍVEL, protocolo de
      intercomunicação (A2A/MCP).
      **Entregue: `5f6dcf8`, integrado em `566bca5` — 4 wireframes estáticos (caixa de entrada,
      livro de mensagens append-only com desvio marcado, roteamento que RECUSA nome ambíguo e
      mostra a colisão + tabela das cinco colisões do §7, protocolo com o que a sessão expõe/consome
      e A2A como "—" com motivo). Self-check do W03: 4 arquivos, 0 falas. Fitness do Gerente (v3):
      22 achados, TODOS da classe citação-sem-atributo — correção attempt=2 entregue (`ccf574c`,
      integrada em `1354240`): `data-referencia` nas citações, só atributos (35/35); **verde nas
      4 telas**.**
- [x] T3-readme-navegacao — Worker01: `prototipo/README.md` (telas × ENTRA × contexto dono ×
      juízes) e o lugar de cada tela na navegação do painel existente (Regência e Chamados ficam
      como estão).
      **Entregue: `e40f4bf` + `ff83e38` ("em entrega" unificado), integrado em `99fd85d` — tabela
      única tela × ENTRA nº × nome ubíquo × contexto × grupo × juízes × estado; os 13 ENTRA cabem
      em 11 telas (21 é objeto das 4 da Mensageria; 26 visível dentro do roteamento); Workflow
      declarado "em entrega" sem nome de arquivo inventado; Regência e Chamados intactos
      (`data-v` verificado em `painel/index.html:955`); grupo novo "Área administrativa" marcado
      como rodada 4, NÃO decidido, NÃO implementado; colisão na navegação explícita (caixa de
      entrada ≠ fila de decisões); divergência 4/5 (Administração no despacho × CONTROLE na
      matriz) declarada com as duas colunas; sem link markdown (nada novo para o check-links).
      Gate re-executado após o merge: 7 telas, 0 achados.**
      **Complemento pós-integração do W05 (`e756232`): as 4 linhas do Workflow pelos nomes reais
      (`workflow-01..04`, renomeados pela regente em `af81499`), estado "neste ramo" (`365f59d`);
      retrato atualizado para 11 telas (4+3+4), datado 26/10; bloco de medição com o topo `af81499`
      medido por ele (11 telas, 0 achados — não aceito de palavra); 4 correções de coerência
      declaradas (frases que ficariam falsas); CHANGELOG intocado de propósito. Tokens (piso):
      fatia 785.878 / sessão 33.118.017.**
- [x] T3-fitness — Gerente: script que percorre os HTML e falha se houver elemento interativo sem
      `data-fonte`, rótulo fora do glossário (glossary.md + os 12) ou número sem a marca "exemplo";
      saída colada no qa-report.
      **Entregue: `fa4ee3e` — `prototipo/verifica-prototipo.py` (4 regras: data-fonte, glossário com
      word-boundary, marca "exemplo" em todo nó de texto, colisões fila/portão sem qualificador);
      smoke-testado em telas sintéticas (5 achados na ruim, 0 na boa; o smoke test achou e corrigiu
      o falso-negativo RACI⊂"operacional"). A rodada verde sobre as telas reais e a saída colada no
      qa-report acontecem no T3-fechamento; a mutação do W02 quebra este script de propósito.**
- [ ] T3-revisao — Worker02: revisão em contexto fresco das telas contra o mapa e as colisões;
      mutação — quebrar o script da fitness function e vê-lo acusar.
- [ ] T3-seguranca — Worker06: segurança documental e conformance 073 nos dois modos.
- [ ] T3-fechamento — Gerente: andamento, `[[DONE 073-rodada-3]]` ao regente (e commitado) com a
      lista de telas, o resultado do script e os tokens. **Rodada 4 só com o "segue".**

## Rodada 2 — confronto com o Maestro e decisão do que entra (25/10, mandato do regente)

`[[TASK id=073-rodada-2 kind=implement cycle=073 attempt=1]]`

- [x] T2-preambulo — Worker06: normalização da força do `não`/`—` entre as gerações de ficha (regra
      na legenda; nenhuma célula `—`→`sim`), correções da amostragem do crítico (Maestri 5 `—` em
      CONTROLE; INTERCOMUNICAÇÃO 14%; Temporal "agentes vivos"/"tarefa aberta" `sim`→`parcial`) e
      seção "Consideradas e não incluídas". **Entregue: `0c74d30`, integrado; verificado por script
      (PASS — 172/223/13/242; grupos 30/76/45/21) e conferido célula a célula nas duas correções
      do crítico.**
- [x] T2-inventario — Worker05: inventário do Maestro — as 26 funcionalidades com tem/parcial/não
      tem e evidência (arquivo:linha, script, comando) em `confronto/inventario-maestro.md`.
      **Entregue: `bdc75cb`, integrado em `8e9ab43` — tem 8 · parcial 16 · não tem 2 (pausar/retomar);
      força da notação espelhando a matriz (só os 2 "não tem" são "não encontrado" — piso, não prova);
      6 citações amostradas pelo Gerente conferem exatamente.**
- [x] T2-confronto — Worker03: matriz 26 × {melhor referência, estado no Maestro, lacuna, decisão
      ENTRA/NÃO PRECISA/DEPOIS}; cada ENTRA com nome na linguagem ubíqua e os três critérios da
      rodada 4; nada entra sem fonte (plataforma citada OU requisito do método).
      **Entregue: `eb40d89` (ff) — ENTRA 13 · NÃO PRECISA 8 · DEPOIS 5, contagem conferida por
      script pelo Gerente; INTERCOMUNICAÇÃO 6 ENTRA de 6; 12 termos propostos, 8 reusados do
      glossário; nenhum ENTRA sobre célula `—`.**
- [x] T2-mapa — Worker02 (se livre) ou Worker03: mapa de contextos delimitados em
      `confronto/mapa-de-contextos.md`, com diagrama.
      **Entregue: `e90e8b9` (W02) — cinco contextos com raiz e invariantes, diagrama Mermaid, sete
      relacionamentos tipados com motivo, core domain = Chamados e Gates (leitura alternativa
      declarada), linguagem ubíqua por contexto com os 12 propostos marcados, cinco colisões de
      nome; divergências declaradas (painel é projeção, sexto contexto recusado por YAGNI).**
- [x] T2-fechamento — Gerente: revisão fresca do confronto (quem não escreveu), conformance 073
      nos dois modos, andamento, `[[DONE 073-rodada-2]]` ao regente. **Rodada 3 só com o "segue".**
      **Entregue: revisão fresca do W05 (6/6; 1 bloqueante de Princípio VIII corrigido pelo Gerente
      e verificado por script — PASS, incluindo um ABAC que a revisão não viu); conformance 073
      verde exit 0 nos dois modos; andamento e CHANGELOG atualizados; DONE emitido ao regente
      (fallback commitado em `done-073-rodada-2.md`).**

## Verification first
- [x] T0 — define the DoD checks — critérios de aceite FR1–FR4 na `spec.md` (ficha por plataforma
  com fonte, matriz consolidada, nenhuma célula sem fonte vira "sim", `andamento.md` a cada DONE);
  comandos verificáveis na `plan.md` §Verification.

## Implementation
- [x] T1-W03 — gateways e consoles de LLM: LiteLLM, Portkey, OpenAI Platform, Helicone (4 fichas;
  LiteLLM rodou local com chave descartável, capturas em `pesquisa/img/`).
- [x] T1-W05 — observabilidade e orquestração de agentes: 9 fichas (7 do despacho + Arize Phoenix
  e Comet Opik no mesmo nicho).
- [x] T1-W06 — controle de processos e governança: 12 fichas (10 do despacho + AWS Bedrock
  AgentCore e Windmill na mesma raia); pausou para a reverificação R1/R2 do ciclo 072 e retomou.
- [x] T1-consolidacao — `pesquisa/plataformas.md`: matriz 25 plataformas × 26 funcionalidades,
  fechada por acréscimo pelo Worker06 (as 13 colunas que faltavam depois das 12 dele).
- [x] T1-revisao — verificação em contexto fresco pelo Worker03 (não consolidou): amostragem
  dirigida de 7 células + recontagem independente + passagem de segurança sobre `pesquisa/`
  (commit `b920fce`); achado bloqueante — leitura subnotificava 4 `sim` — corrigido pelo
  Gerente e reconferido por script contra a matriz.
- [x] T1-fechamento — Gerente: preenche plan/qa-report, marca o rabo com a evidência, roda
  check-conformance 073 e emite o DONE da rodada 1 ao regente (a rodada 2 espera o "segue").

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [ ] TAIL:mutation — n/a: rodada documental — nenhum gate executável criado ou alterado (não há código neste ciclo); o verificável é a contagem e a amostragem, cobertas no TAIL:review
- [ ] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
