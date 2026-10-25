# QA report 073 — Área administrativa do Maestro (rodada 1: pesquisa de plataformas)

- **Date**: 2026-10-24 (fichas) · 2026-10-25 (consolidação e fechamento) · **Lane**: plena ·
  **Verdict**: pending (fecha com a revisão em contexto fresco)

## Fitness functions (DoD)
| Check | Expected | Result |
|---|---|---|
| `scripts/check-cycle.sh 073` | lane justificada | **ok** — "lane 'full' with rationale" (justificativa dos três fatores no spec, commit `b186214`) |
| Colunas da matriz (`pesquisa/plataformas.md`) | 2 + 25 = 27 | **27** (medido por script sobre o arquivo, Worker06) |
| Linhas de funcionalidade | 26 | **26**, na ordem da tabela fixa da spec |
| Linhas com contagem de células ≠ 27 | 0 | **0** |
| Células da matriz | 25 × 26 = 650 | **650** |
| Fichas com tabela fixa completa | 25 × 26 = 650 | **650** — 629 com veredito explícito + 21 células em branco (convertidas em `—` na matriz) |
| `scripts/check-conformance.sh 073` | verde nos dois modos | (preenchido no fechamento da rodada) |

## Closing tail — the evidence
<!-- One entry per non-n/a TAIL token. What was OBSERVED, never the intention restated. -->
- TAIL:review — (preenchido no fechamento: revisão em contexto fresco pelo Worker03, que não consolidou)
- TAIL:security — (preenchido no fechamento: varredura de segredos/credenciais/dados pessoais sobre pesquisa/)
- TAIL:mutation — n/a: rodada documental — nenhum gate executável foi criado ou alterado neste ciclo (não há código); o veredito verificável da rodada é a contagem e a amostragem contra as fichas, cobertas no TAIL:review
- TAIL:gate — (do regente: o "segue" para a rodada 2 — confronto com o Maestro e decisão do que entra)

## Requirement coverage
- FR1: **presente** — 25 fichas em `pesquisa/`, cada uma com URL, data da visita, o que foi aberto
  de verdade (docs, repositório, demo, execução local) e a tabela fixa de 26 funcionalidades.
- FR2: **presente** — `pesquisa/plataformas.md` consolida as 25 plataformas (27 colunas de
  cabeçalho, 26 linhas de dados, 650 células), fechada por acréscimo.
- FR3: **presente** — toda célula se apoia na ficha da coluna; célula sem fonte ficou `—` (as 21
  em branco do Worker03 foram convertidas na matriz); nenhuma célula sem fonte virou "sim"
  (amostragem dirigida no fechamento).
- FR4: **presente** — `andamento.md` atualizado a cada DONE (quatro linhas da rodada 1 em
  **entregue** + histórico datado).

## Pending gate
- dev -> main promotion awaits human approval.

## Evidência da consolidação (073-T1-consolidacao, 25/10)

Worker06, contexto próprio. `pesquisa/plataformas.md` foi fechada **por acréscimo**, como a seção
"Como acrescentar uma plataforma" previu: as 13 colunas que faltavam (4 do Worker03 + 9 do
Worker05) entraram depois das 12 do Worker06. Nenhuma linha das fichas alheias foi reescrita.

### Contagem conferida

| O que | Esperado | Medido | Como foi medido |
|---|---|---|---|
| Colunas da matriz | 2 + 25 = 27 | **27** | cabeçalho da tabela, contado por script sobre o arquivo |
| Linhas de funcionalidade | 26 | **26** | 26 linhas de dados; **0** com contagem de células diferente de 27 |
| Células da matriz | 25 × 26 = 650 | **650** | 26 linhas × 25 colunas de plataforma |
| Linhas das 13 fichas novas | 13 × 26 = 338 | **338** | contagem própria por arquivo: **317 com veredito explícito + 21 células em branco** |
| Fichas consolidadas | 25 | **25** | 12 + 4 + 9, todas com 26 linhas |

Medição própria das 13 fichas novas (uma linha por arquivo): `helicone.md` **17**,
`openai-platform.md` **22**, `portkey.md` **20**, `litellm.md` **24** — as quatro do Worker03 somam
83 = 4×26 − 21 células em branco — e **26** para cada uma das nove do Worker05. Total com veredito:
**317**; 317 + 21 = **338** = 13 × 26.

### Células sorteadas e conferidas contra a ficha

| Célula na matriz | Ficha (caminho:linha) | O que a ficha diz |
|---|---|---|
| Langfuse × auditoria = `sim` | `pesquisa/langfuse.md:47` | "auditoria → sim — *audit logs* listados entre os controles" |
| Portkey × mensagem entre agentes = `não` | `pesquisa/portkey.md:68` | "mensagem entre agentes → não — nada sobre mensagem entre agentes (nem o termo A2A aparece)" |
| LiteLLM × colisão de nomes = `—` | `pesquisa/litellm.md:119` | célula **em branco**: "colisão de nomes → (vazio) — `a2a_agent_permissions` fixa o roteamento por `agent_id`, mas nenhuma página aberta trata colisão" |
| LiteLLM × protocolos (A2A; MCP) = `sim` | `pesquisa/litellm.md:115` | "Protocolos (A2A; MCP) → sim — `agent-card.json`, `protocolVersion` 0.3/1.0, e MCP" |

As quatro conferem — inclusive a única conversão deliberada: célula **em branco** na ficha virou
`—` na matriz, porque é o que a legenda manda e porque branco não é "sim" (FR3).

### Achado declarado (não corrigido por conta própria)

As 13 fichas novas **não usam `—`**: o Worker03 deixa a célula em branco (21 células) e o Worker05
escreve `não` para "nada achei". Nas colunas do Worker05, `não` significa amiúde **"não
encontrei"**, não "a fonte afirma que não existe" — é mais fraco que o `não` da legenda. O FR3 não
é violado (nenhuma célula sem fonte virou "sim"), mas a **força** do veredito difere entre as duas
gerações de ficha. Normalizar é decisão do dono da rodada; a nota está repetida em
`plataformas.md`, para quem ler a matriz sem ler este relatório.

### Decisão do Gerente (25/10) — notação ratificada, normalização deferida

O tratamento do consolidador está **ratificado**: célula em branco vira `—` (é o que a legenda
manda), `não` é transcrito como a ficha escreveu, e a divergência fica declarada na legenda da
matriz. O FR3 está preservado — nenhuma célula sem fonte virou "sim" — e a nota avisa o leitor
sobre a força do veredito. **Normalizar** (reclassificar o `não` do Worker05 entre "ausência
afirmada pela fonte" e "não encontrei", célula a célula, relendo as 9 fichas) fica como
**tarefa de preâmbulo da rodada 2**: é no confronto com o Maestro que a força do veredito passa
a decidir, e reclassificar agora seria gastar ficha antes de saber se a rodada 2 precisa da
distinção.
