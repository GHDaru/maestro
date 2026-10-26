# [[DONE id=073-rodada-3 outcome=delivered]] — fallback commitado (o mesmo texto foi ao regente por SendMessage)

> Fecho da rodada 3 do ciclo 073 (área administrativa). Rodada 4 (três juízes) só com o "segue"
> do regente.

## As 11 telas (13 ENTRA cabem em 11)

`specs/073-area-administrativa/prototipo/` — wireframes estáticos, sem servidor, sem JavaScript
de dados, no contrato de marcação (data-fonte por bloco, data-rotulo com termo do glossário,
data-exemplo com "(exemplo)", `—` sempre com motivo, citação sob data-fonte/data-referencia):

- **Mensageria** (W03, `5f6dcf8` + correção `ccf574c`): `mensageria-01-caixa-de-entrada.html` ·
  `mensageria-02-livro-de-mensagens.html` · `mensageria-03-roteamento.html` (colisão de nomes
  VISÍVEL, recusa de nome ambíguo) · `mensageria-04-protocolo.html` (A2A "—" com motivo).
- **Administração** (W04, `5ce4a5f` + correção `7147f50`): `administracao-catalogo.html` ·
  `administracao-politicas.html` (allow/deny/ask) · `administracao-orcamento.html`.
- **Workflow de sessões** (W05, `365f59d`+`fc183ce`, renomeadas `workflow-01..04` pela regente
  em `af81499`; correção `09c02f0`): `workflow-01-sessao-de-agente.html` (subir/derrubar;
  derrubar desabilitado aguardando gate humano) · `workflow-02-estado-do-agente-vivo.html` ·
  `workflow-03-tarefa-aberta.html` · `workflow-04-consumo-por-agente.html`.

Acompanham: `prototipo/README.md` (W01: tabela tela × ENTRA × contexto × juízes, 13 em 11,
navegação proposta marcada rodada 4 NÃO decidida) e o glossário com os **12 termos ratificados**
(W01 `ebe7eb9`, +12/−0, colisões resolvidas por `arquivo:linha` do mapa §7).

## O gate executável e sua prova

- **`prototipo/verifica-prototipo.py`** (Gerente, `fa4ee3e`→v3 `da85def`; regra 4 ampliada pelo
  W02 `9cf0118`): 4 regras — data-fonte em todo interativo, rótulo no glossário (word boundary),
  número com marca "exemplo", fila/portão nunca nus (agora em **todo texto visível e atributo**,
  com isenção declarada para tabela de colisão de nomes).
- **Saída final, colada**:

```text
python specs/073-area-administrativa/prototipo/verifica-prototipo.py
-- verifica-prototipo: 11 screen(s), 0 finding(s)   [exit 0]
```

- **Mutação** (W02, contexto fresco): regra 3 cega → sumiu `number without the "exemplo" mark:
  "42"`; regra 4 cega → sumiu `"fila" unqualified (decisões or outbox?): "Fila"`; com a regra
  ampliada, 12 telas · 10 achados → 4 (sumiram os 4 reais + 2 do fixture, um deles novo, visível
  só com a regra ampliada). Script restaurado byte a byte (SHA-256 conferido, git diff vazio).
  Descoberta que motivou a extensão: **nenhuma tela real exercitava a regra 4** — o fixture
  `prototipo/fixtures/tela-ruim.html` é o único oráculo dela.

## Revisão fresca e correção final

- **Revisão (W02 `d1e9cc7`)**: nenhuma violação estrutural nas 11 telas; **9 achados** de
  disciplina de nome/citação que o gate então não via (R1–R9, cada um com arquivo:linha).
- **Correção por dono de tela** (mandato da regente): R1/R1b/R2/R3 → W03 `938d38b`; R4
  (`tasks.jsonl` inexistente → `docs/records/tarefas.jsonl`) /R7/R9-workflow → W05 `09c02f0`;
  R5/R2b/R6 → W04 `9fbbad3`. **Placar: 8 corrigidos, R8 e R9-mensageria/administração declarados
  dívida da rodada 4** (renome de arquivo e base única de citação são decisão da regente).
  Resalva do W03 registrada: o mapa §7 (`:292`) escreve "fila (outbox)" com parênteses; as telas
  seguem a grafia da regente "fila outbox" — alinhar a §7 é edição de doc da rodada 4.

## Segurança e conformance

- **Segurança documental (W06 `bc36487`)**: 0 achados — nenhum segredo (falsos positivos
  `sk-l`⊂"task-ledger", `senha`⊂"desenhados" confirmados por `grep -o`), nenhum dado pessoal,
  todo valor que parece real marcado `(exemplo)`+`data-exemplo`, só URL de documentação pública.
- **Conformance 073**: verde nos dois modos (normal e `TICKED_ONLY=1`), exit 0 — saídas coladas
  no qa-report § fechamento.

## Incidente declarado

Um marcador de conflito órfão (`<<<<<<< HEAD`) entrou no qa-report na resolução do merge
`00c1ae9` (Gerente, 25/10) e propagou por todos os commits seguintes (inclusive o `af81499` da
regente) até ser achado e removido na resolução do merge do W04 (`6f71db7`; um segundo, do merge
do W03, removido em `858baa4`). Nenhum gate o viu — nenhum fitness function lê o qa-report.
Lição para a retrospectiva: conferência de marcadores é passo declarado pós-resolução.

## Tokens (pisos — soma de `message.usage` desde a 1ª ocorrência do `[[TASK]]`; `tarefas.jsonl`
parou no ciclo 064, os pisos vêm dos transcripts)

W01 glossário 14,7M · W01 README 2,24M + complemento 785.878 · W03 telas 57,2M · W03 correção
61,36M (sessão) · W03 correção final 8,97M · W04 telas 18,26M · W04 correção 4,1M · W04 correção
final 5,70M · W05 telas 2,56M · W05 correção 0,45M · W06 segurança 12,67M · W02 revisão 9,78M ·
W02 regra 4 0,63M. (W06 reverificação do 072: ~5,32M, contabilizada no ciclo 072.)

## Limites cumpridos

Sem push, sem merge na dev/main, sem promote-main.sh, sem código de produto, sem segredo, siglas
expandidas (Princípio VIII). Rodada 4 (três juízes, nota 0–10, passa com os três ≥ 9) **somente
com o "segue" do regente**.
