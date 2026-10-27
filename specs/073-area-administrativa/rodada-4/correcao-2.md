# Rodada 4 — correção 2, a última (consolidação da segunda rodada de juízes pela regente, 26/10/2026)

> Três juízes em contexto fresco sobre HEAD faca232 (correção 1 integrada): **barra não atingida**
> nos três, mas o **diagnóstico mudou** nos três — as lacunas de ausência da rodada 1 (gate do
> derrubar, precedência e escopo, identidade `nome · ref · projeto`, estados de entrega, DEPOIS com
> gatilho) foram fechadas; o que resta são **contradições criadas pelas próprias correções**,
> **citações `arquivo:linha` defasadas** e o **mecanismo de execução do controle**. Notas: juiz 1
> (controle) 4 peças em 9 e 12 em 8; juiz 2 (administração) 5 em 9 e 11 em 8; juiz 3
> (intercomunicabilidade) 6 em 9, 9 em 8 e 1 em 7. Nenhuma peça caiu. Pareceres:
> `juiz-1-controle-rodada-2.md`, `juiz-2-administracao-gerenciamento-rodada-2.md`,
> `juiz-3-intercomunicabilidade-rodada-2.md`.
>
> Pela regra das duas rodadas: diagnóstico mudou → **uma única correção 2**. Depois dela os três
> juízes voltam uma última vez. Se alguma peça ficar abaixo de 9, o laço **para** e o Darú decide
> com os três pareceres na mão (o que resta não é falta de desenho, é decisão de produto).

## Decisões da regente (fixas)

1. **Roster único de exemplo em todas as telas = roster real do 26/10**: Gerente `[31ee4d]`,
   Worker01 `[9a1b27]`, Worker02 `[31f7bf]`, Worker03 `[ad66d6]`, Worker04 `[4d000a]`, Worker05
   `[78d88f]`, Worker06 `[c85948]`, MAESTRO `[7c8d05]` (regente), todos `· 410_MAESTRO`; as sessões de
   outro projeto (Hindiana Office) usam refs próprios e nunca um ref do roster. **Nenhum ref
   pertence a dois nomes na mesma tela.** O verificador ganha a **regra 6**: dentro de uma tela,
   um ref `[xxxxxx]` só aparece colado a um único nome, e todo nome do roster vem com o ref do
   roster (lista no script); fixture e mutação. A ambiguidade de endereço continua **não
   verificada por script** e isso fica **declarado** no README e no mapa (§ 8).
2. **Mecanismo de execução do controle**: "recusar a chamada seguinte" e "suspender a sessão"
   **saem de ENTRA e viram DEPOIS com gatilho** ("existe um ponto de execução que corte gasto de
   modelo, não só uso de ferramenta: hook que lê o consumo medido — a desenhar na raia infra").
   O ENTRA 4 (limite de orçamento) fica com **declarar o teto + avisar**: o aviso é uma mensagem
   endereçada `nome · ref · projeto` à sessão dona **e** ao regente `MAESTRO [7c8d05]`, pela
   Mensageria (fecha P12 dos juízes 1 e 3). O ponto de execução do controle e o caminho de
   aprovação do derrubar entram nas seções "Limites"/"Lacunas declaradas" do confronto e do
   inventário, junto com "o ledger `tarefas.jsonl` parou no 064" e "a área é somente leitura
   nesta rodada" (P4 dos três).
3. **Derrubar e reiniciar**: a confirmação do `workflow-01` distingue `claude stop` (religável por
   `claude --resume`, contexto preservado) de `claude rm` (irreversível) e **desenha a passagem
   pelo pedido de decisão da Regência** (relação 5 do mapa); o botão "reiniciar a sessão" do
   alerta em `workflow-02` fica **desabilitado** e aponta para essa confirmação; "cancelar tarefa"
   mostra o que se perde. O ponto de execução permanece dívida declarada.
4. **Catálogo e políticas**: a **sessão dona não cadastra "quem pode usar" nem preço** — só humano
   ou regente por delegação (alinha com o orçamento); a tela ganha a **tabela do Modelo** com
   provedor, preço por milhão, quem pode usar, projeto (é dela que `workflow-04` e o orçamento
   dizem ler o preço); a tela de políticas ganha **coluna de escopo** na tabela de regras e uma
   **regra de modelo** de exemplo; precedência conciliada e marcada como **decisão de projeto**:
   "o mais específico decide qual regra se aplica; entre regras do mesmo escopo, `deny > ask >
   allow`"; o botão "propor regra (exemplo)" some (o formulário fica).
5. **Agentes como objeto**: agente = perfil (`.claude/agents/*.md`), sessão = instância com ref.
   O catálogo ganha a seção **"Agentes (perfis)"** lendo os perfis reais do repositório
   (`data-fonte`: `ls .claude/agents`), com papel, ferramentas e modelo padrão; "cadastro de
   agentes" passa de NÃO PRECISA a **ENTRA 16, como leitura do catálogo de perfis** (o cadastro é
   o arquivo versionado; a tela lista e liga ao roteamento). Em `workflow-04` a coluna "agente" é
   o **perfil sem ref**; as sessões agrupadas abaixo levam o ref.
6. **Orçamento**: a tabela de tetos ganha **coluna "limiar de alerta"** com valor de exemplo;
   precedência entre tetos: "**o menor teto aplicável vence**" (projeto, agente, modelo);
   cabeçalhos e `data-fonte` das três telas da Administração sem "e de taxa" e com os juízes
   certos; `workflow-04` reconcilia o cartão "teto vigente" com a seção "teto": o cartão mostra
   o teto da Administração com unidade (tokens ou US$) ou "— (nenhum teto declarado)", e declara
   que comparar contra um piso pode estourar sem aviso.
7. **Mensageria**: livro em ordem coerente com o título (mais antiga primeiro, ordem 8→12);
   coluna **tarefa** derivada da tag `[[TASK id]]` e coluna **custo** "— (ledger parado no 064)";
   leitura do livro **restrita ao projeto** (coerente com o default-deny) e declarada; `registrar_peca`
   ganha linha "quem autoriza"; "ref mudou no reinício" = **recusa + oferta do ref novo** (alinha
   com o mapa `§ 7.1`); Windmill sai da tela de roteamento (a referência é Claude Code
   `SendMessage`/`ListAgents` e Kiro × Claude Code na colisão); correção factual: A2A tem **5**
   `sim` na matriz, não 1; na coluna "nome pretendido" fica o nome nu digitado, os refs ficam na
   coluna ao lado; linha de exemplo do desvio com remetente diferente do destinatário.
8. **Citações defasadas**: toda citação a `claude-code.md` revalidada contra o HEAD (`:47→:61`,
   `:49→:63`, `:65→:79`, `:68→:82`, `:71→:84`) em `inventario-maestro.md`, `confronto-decisao.md`
   e `workflow-02`; o README do protótipo ganha a regra "citação de ficha é revalidada no mesmo
   commit que muda a ficha". Mapa: `:243` relação 5 → 6; `:89-90` "o único ponto" → "o ponto
   executável no repositório, além do `permissions` do harness". Confronto: lacuna da linha 52
   reescrita ("bloco `permissions` não declarado no repositório"); "mensagem desviada" sai de
   `alertas` (já tem tela) e o DEPOIS passa a ser "notificação ativa"; títulos "(6)" conferidos
   com as linhas. Matriz: `:155` e `:227-228` reescritos como "não encontrado na documentação
   lida"; `sim` de auditoria do Langfuse rebaixado a `parcial` (mesmo critério do custo).

## Tarefas por dono (uma rodada; commit "ciclo 073: correção 2 da rodada 4 — <fatia>")

| Dono | Fatia |
|---|---|
| **Worker02** | regra 6 do verificador (roster + ref único por nome, fixture, mutação); confronto (decisões 2, 5, 8: ENTRA 16, recusar/suspender → DEPOIS, lacunas consolidadas em "Limites", citações, títulos, "mensagem desviada"); mapa (`:243`, `:89-90`, § 8 "ambiguidade não verificada") |
| **Worker03** | as 4 telas da Mensageria (decisões 1 e 7) |
| **Worker04** | as 3 telas da Administração (decisões 4, 5, 6; aviso do teto como mensagem endereçada, decisão 2) |
| **Worker05** | as 4 telas do Workflow (decisões 1, 3, 5, 6) + inventário (citações, "Limites": ponto de execução, derrubar, ledger, somente leitura) |
| **Worker06** | matriz (`:155`, `:227-228`, Langfuse auditoria → parcial, revalidação das linhas citadas das fichas) + segurança documental + conformance 073 nos dois modos |
| **Worker01** | README (roster, regra 6, ENTRA 16, regra da citação revalidada, "ambiguidade não verificada"), glossário ("agente (perfil)" × "sessão") |
| **Gerente** | integra, verificador 11 telas / 0 achados com **seis** regras, `[[DONE 073-correcao-2]]` a `MAESTRO [5d2fba]` (ref novo desde 26/10 20:40) com HEAD e tokens |

## Depois

Os três juízes voltam uma última vez, com os mesmos mandatos, comparando com a rodada 2. Peça
abaixo de 9 na terceira leitura **não gera correção 3**: o laço para e a regente leva os três
pareceres ao Darú com a lista do que é decisão de produto.
