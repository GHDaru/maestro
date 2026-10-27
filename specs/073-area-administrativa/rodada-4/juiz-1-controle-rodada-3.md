# Rodada 4 — Juiz 1: CONTROLE — terceira leitura (contexto fresco, 27/10/2026, sobre HEAD 4e421a4)

## Veredito

**Barra não atingida.** 13 das 16 peças chegam a 9 ou mais. Três ficam em 8: P1, P5 e P12. A barra exige as 16 em 9, então ela não passa.

Na segunda leitura eram 4 peças em 9 e 12 em 8. A correção 2 fechou quase tudo o que pedi. Fecharam em 9: P2, P3, P4, P6, P7, P8, P9, P10, P13, P14 e P16. As peças P11 e P15 já estavam em 9 e seguem.

**Funcionalidades ENTRA.**
- Os totais 16/5/11 = 32 conferem. Contei os grupos linha a linha em `confronto-decisao.md:51-122`, `:190-193` e `:204-208`.
- Todas as 16 têm tela. O cadastro de agentes ganhou a tabela "Agentes (perfis)" em `administracao-01-catalogo.html:276-382`.
- O ENTRA 4 está no alvo da regente: declarar o teto e avisar por mensagem endereçada a `nome · ref · projeto` e a `MAESTRO [7c8d05]`. Está em `administracao-03-orcamento.html:112-116` e `confronto-decisao.md:58` e `:133`.
- Recusar e suspender saíram do ENTRA e viraram DEPOIS com gatilho, em `confronto-decisao.md:172`.

**Plataformas.** As 25 colunas seguem na matriz (`plataformas.md:64-91`). Não reabri as fichas.

## Tabela

| Peça | Nota r2 | Nota r3 | Pedido da r2 | Fechado? | Evidência |
|---|---|---|---|---|---|
| P1 Plataformas | 8 | **8** | Separar orçamento e taxa em linhas, ou marcar por célula se o `sim` corta ou só avisa | **Não.** A linha segue fundida e a distinção continua em prosa. A correção 2 só mexeu em Langfuse (auditoria virou `parcial`) e nas células "não encontrado na documentação lida". | `plataformas.md:69` (linha fundida), `:93-98` (nota de coluna em prosa), `:132-138` (Langfuse), `:250-261` |
| P2 Inventário do Maestro | 8 | **9** | Refazer as citações de `claude-code.md` | **Sim.** `:61`, `:63`, `:79`, `:82` e `:84` batem com as linhas da ficha. | `inventario-maestro.md:53,55,92,95,112`; `claude-code.md:61,63,79,82,84` |
| P3 Confronto e decisão | 8 | **9** | Reescrever a lacuna "allow/ask executáveis"; resolver a circularidade suspender ↔ pausar; refazer citações | **Sim, os três.** A lacuna virou "bloco `permissions` não declarado no repositório". A circularidade foi nomeada e desfeita. As citações foram revalidadas. | `confronto-decisao.md:60`, `:172`, `:57`, `:94`, `:96`, `:104`, `:110` |
| P4 Lacunas declaradas | 8 | **9** | Registrar nas seções "Limites"/"Lacunas" o ponto de execução e o caminho de aprovação do derrubar | **Sim, nas duas peças.** Entram também o ledger parado no 064 e a área somente leitura. | `confronto-decisao.md:274-286`; `inventario-maestro.md:126-141` |
| P5 Mapa de contextos | 8 | **8** | Corrigir `:243` (relação 5 → 6) e "o único ponto" (`:89-90`) | **Sim, os dois pedidos.** Fica um achado novo, abaixo. | `mapa-de-contextos.md:246` (relação 6), `:91-93`, `:393-406`; **ausência** de "políticas" no mapa (grep sem resultado) |
| P6 mensageria-01 | 9 | **9** | — | Mantida. Roster correto e linha de desvio com projeto e ref. | `mensageria-01-caixa-de-entrada.html:60-86`, `:92` |
| P7 mensageria-02 | 8 | **9** | Justificar a leitura aberta do livro contra o default-deny, ou restringi-la por projeto | **Sim.** A leitura é restrita ao projeto e declarada. A ordem do livro é 8→12, e há linha com remetente diferente do destinatário. | `mensageria-02-livro-de-mensagens.html:124-125`, `:65-117`, `:93` |
| P8 mensageria-03 | 9 | **9** | — (resto da r2: "ref mudou" pedia confirmação, o mapa recusa) | **Sim.** A linha agora é "recusa e oferece a ref nova", igual ao mapa. | `mensageria-03-roteamento.html:74-79`, `:85-90`; `mapa-de-contextos.md:358` |
| P9 mensageria-04 | 8 | **9** | Linha de quem autoriza `registrar_peca` | **Sim.** Autoriza quem move a peça (sessão dona da fatia ou regente), e a ferramenta recusa sem a evidência. | `mensageria-04-protocolo.html:166-168` |
| P10 administracao-01 | 8 | **9** | Tirar da sessão dona o poder sobre "quem pode usar" e preço; espelhar uma regra de modelo nas políticas | **Sim.** Os dois campos ficam desabilitados e só o humano ou o regente por delegação os define. Há tabela do Modelo e uma regra de modelo nas políticas. | `administracao-01-catalogo.html:153-182`, `:201-207`, `:213-215`; `administracao-02-politicas.html:160-168` |
| P11 administracao-02 | 9 | **9** | — | Mantida. A precedência virou decisão de projeto em dois passos, e há coluna de escopo. | `administracao-02-politicas.html:116-122`, `:243-252` |
| P12 administracao-03 | 8 | **8** | Dizer qual ponto executa recusar/suspender, ou rebaixá-los a DEPOIS e deixar só "avisar" como ENTRA | **Parcial.** O rebaixamento foi feito na caixa de efeitos e no confronto. A tabela de tetos não acompanhou. | `administracao-03-orcamento.html:109-125` (ok) contra `:136`, `:146`, `:156`, `:166` (tabela) |
| P13 workflow-01 | 8 | **9** | Distinguir `claude stop` de `claude rm`; tirar "contexto não recuperável" ao lado de `--resume`; desenhar a passagem pelo pedido de decisão; manter o ponto de execução como dívida | **Sim, nos quatro.** Ressalva sobre a fonte, abaixo. | `workflow-01-sessao-de-agente.html:167-169`, `:175`, `:178` |
| P14 workflow-02 | 8 | **9** | Desabilitar "reiniciar a sessão" e apontá-lo para a confirmação do workflow-01 | **Sim.** O botão está `disabled`, o rótulo diz "abre a confirmação de workflow-01", e há nota explicativa. As citações `:79,82` batem. | `workflow-02-estado-do-agente-vivo.html:133`, `:135`, `:102`, `:120` |
| P15 workflow-03 | 9 | **9** | — (resto da r2: cancelar não mostrava o que se perde) | **Sim.** A confirmação lista o que se perde e o que fica. | `workflow-03-tarefa-aberta.html:130-131` |
| P16 workflow-04 | 8 | **9** | Reconciliar `:87` com `:169`; dar unidade ao percentual; declarar que comparar contra um piso pode estourar sem aviso | **Sim, os três.** O cartão mostra "— (nenhum teto declarado)", a unidade é tokens ou US$ e o aviso do piso está escrito. | `workflow-04-consumo-por-agente.html:87-88`, `:168-170` |

## O que fica aberto

**P1 — 8. É falta de desenho com um componente de decisão de produto.**
- Nenhum item do que pedi foi feito. A matriz continua com "limites de orçamento e de taxa" numa linha só (`plataformas.md:69`). O `sim` dessa linha segue sem dizer se corta ou só avisa. A nota em prosa (`:93-98`) explica a diferença, mas não marca nenhuma célula.
- Separar as linhas muda a "tabela fixa de 26" da spec, e isso é decisão do regente. A alternativa que não mexe nas 26 linhas é marcar, por plataforma, se o `sim` corta ou avisa. Isso é desenho puro.
- O confronto já desdobrou orçamento e taxa (`confronto-decisao.md:58-59`), então matriz e confronto divergem na estrutura.

**P5 — 8. É falta de desenho, e o achado é novo.**
- O ENTRA "políticas allow/deny/ask" não tem casa no mapa. O mapa diz que cada ENTRA pertence a um contexto (`mapa-de-contextos.md:38`). O § 6.5 lista "os quatro ENTRA da Administração": cadastro de agentes, catálogo, orçamento e auditoria (`:307-310`).
- A tela `administracao-02-politicas.html` se declara parte da Administração, mas a política não aparece em nenhum dos cinco contextos. Pelas minhas contas, Workflow tem 5, Administração 4 e Mensageria 6. São 15 de 16.
- Era um furo anterior que eu não vi na r2, quando li o mapa focado na execução do controle. Continua sendo a peça do controle, porque a declaração da política precisa de um dono no mapa.
- A correção é uma linha no § 6.5. Os três pedidos da r2 sobre essa peça foram atendidos.

**P12 — 8. É falta de desenho pequena. Um ponto toca decisão de produto.**
- A caixa "Efeito ao estourar" declara certo: avisar é o ENTRA, recusar e suspender são DEPOIS (`administracao-03-orcamento.html:109-125`).
- A tabela de tetos, logo abaixo, ainda oferece como opção de cada escopo "avisar · recusar · suspender" (linha de projeto, `:146`), "avisar · recusar" (agente, `:156`) e só "recusar" (modelo, `:166`). Nenhuma célula marca o DEPOIS.
- A linha do modelo oferece apenas um efeito que, por decisão da regente, ainda não existe. Hoje esse escopo não tem efeito algum. A tela contradiz a si mesma.
- Resta uma pergunta, que é de produto: qual processo calcula o cruzamento do limiar e emite a mensagem de aviso? A tela chama o aviso de "efeito de hoje" (`:112`), e o limiar vivo só vem "quando o teto executável existir" (`:218-219`). A dívida declarada trata o corte, não o emissor do aviso.

## Ressalvas dos 9 (não mudam a nota)

- **P13, fonte da reversibilidade.** A tela cita `claude-code.md:59` para "stop é religável e rm é irreversível". A linha 59 diz só que `stop` e `rm` "derrubam" e que `respawn` ressuscita. A assimetria é inferência. Além disso, a retomada citada é `claude --resume`, enquanto a ficha traz `claude attach` (`:61`). Recomendo trocar a citação por "a confirmar" ou corrigir a ficha.
- **P11, precedência.** A precedência é por escopo e depois `deny > ask > allow`. Pelo que sei do harness do Claude Code, o `deny` sempre vence, em qualquer escopo. Não verifiquei isso nesta leitura. Se estiver certo, um `allow` específico não sobrepõe um `deny` geral no bloco `permissions`. É um risco de execução, e a tela já declara a regra como decisão de projeto.
- **P9, leitura entre sessões.** `estado_atual` aceita o estado de "aquela sessão" para qualquer chamador (`mensageria-04-protocolo.html:93`). Isso fica mais aberto que a leitura do livro, que foi restrita ao projeto.
- **P6, autoridade do drenar.** "O ref de quem pede é o que autoriza" (`mensageria-01-caixa-de-entrada.html:92`) segue fraco, porque o ref muda a cada reinício. Já era ressalva na r2.
- **P10, dois lugares para o mesmo uso.** "Quem pode usar" do modelo no catálogo e a regra de modelo nas políticas dizem a mesma coisa em dois lugares. A tela não diz qual vale. Isso não impede a nota.

## Limites do que li

- **O arquivo `done-073-correcao-2.md` não existe.** Usei o histórico de `andamento.md:105-122`. Não li a seção da correção 2 em `qa-report.md`.
- **Não rodei nenhum script.** Nem o verificador `verifica-prototipo.py`, nem `check-conformance`. Também não abri o script nem as fixtures.
- **Telas lidas só em parte.** Nas quatro da Mensageria, li a partir da linha 48. Em `administracao-01-catalogo.html` e `administracao-02-politicas.html`, a partir da linha 50. Em `workflow-03-tarefa-aberta.html`, a partir da linha 48. As demais li inteiras.
- **`mapa-de-contextos.md`.** Li as linhas 36-47, 70-179 e 296-407, mais greps por termo. Que a política não aparece no mapa vem de grep sem resultado em "políticas", "política declarativa" e "allow/deny".
- **Sem conferência de código e de matriz.** Não conferi as citações `arquivo:linha` de código nem o conteúdo célula a célula da matriz contra as 25 fichas.
- **Outros documentos.** Do `README` do protótipo, só trechos por grep. Não li o glossário nem os pareceres dos outros dois juízes. As fichas além de `claude-code.md` ficaram fechadas.
- **Conhecimento do harness.** A ressalva sobre o `deny` do Claude Code vem de conhecimento próprio, não testado aqui.

DIAGNÓSTICO: **mudou.** Na r2 o fio principal eram as contradições entre telas, as citações defasadas e a falta do mecanismo de execução. Esses fios fecharam. Restam três pontos de natureza diferente: a matriz de plataformas que a correção não tocou (P1), um ENTRA do controle sem contexto no mapa (P5) e a tabela de tetos que não acompanhou o rebaixamento de recusar/suspender (P12). Nenhum deles é o mecanismo de execução.
