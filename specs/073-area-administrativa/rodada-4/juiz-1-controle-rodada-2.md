# Rodada 4 — Juiz 1: CONTROLE — segunda rodada (contexto fresco, 26/10/2026, sobre HEAD faca232)

## Veredito

**Barra não atingida.** Só 4 das 16 peças chegam a 9 (P6, P8, P11, P15). As outras 12 ficam em 8, nenhuma abaixo disso. Na rodada 1 a nota máxima era 8 e a mínima 5.

**Funcionalidades ENTRA.** As 15 têm tela (`confronto-decisao.md:177`). Duas entraram na correção: auditoria administrativa e custo estimado por agente. A auditoria aparece como seção "Histórico de mudanças" nas três telas da Administração. O custo estimado aparece como coluna em `workflow-04-consumo-por-agente.html:101`. O ENTRA 1 (derrubar) tem gate desenhado, o que antes não tinha. O ENTRA 4 (orçamento) tem efeito ao estourar, escopo e unidade; a taxa foi rebaixada a DEPOIS com gatilho (`confronto-decisao.md:51` e `:162`).

**Plataformas.** As 25 colunas continuam na matriz e todas têm ficha (`plataformas.md:64-91`). Não reabri as 25 fichas.

**O que travou o 9.** Quase tudo que pedi na rodada 1 foi fechado no papel. O que falta é de outra natureza:
- Nenhuma peça mostra o mecanismo que faria o controle valer.
- Há contradições entre telas.
- Há citações `arquivo:linha` que não batem com o HEAD (linhas citadas de `claude-code.md`).

### Defeito transversal: linhas citadas de `claude-code.md` desatualizadas

A correção exigia `arquivo:linha` revalidados. O `inventario-maestro.md:17` afirma que foram. Para as citações de `claude-code.md`, isso não vale mais no HEAD, porque a correção da matriz inseriu linhas na ficha depois da revalidação.

| Citado | Aponta hoje para | Linha real |
|---|---|---|
| `:47` (retomar) | texto de `crossSessionInbound` | `claude-code.md:61` |
| `:49` (permissions) | texto de `crossSessionInbound` | `claude-code.md:63` |
| `:65` e `:68` (mensagem, roteamento) | linhas de "cadastro de agentes" e "chaves e segredos" | `claude-code.md:79` e `:82` |
| `:71` (colisão) | outra linha | `claude-code.md:84` |

O conteúdo citado existe na ficha, só em outra linha. As citações com número errado estão em `inventario-maestro.md:48,50,87,90`, `confronto-decisao.md:49,86,88,96,102,160` e `workflow-02-estado-do-agente-vivo.html:102,120`.

## Tabela

| Peça | Nota r1 | Nota r2 | Lacuna da r1 | Fechada? | Evidência |
|---|---|---|---|---|---|
| P1 Inventário de plataformas | 7 | 8 | Matriz não separa limite que corta de alerta que só avisa; "pausar" quase todo "—" | **Parcial.** Nota de coluna e leitura "não encontrado na documentação lida" entraram. A linha segue fundida (orçamento e taxa) e a distinção é prosa, não célula. Não conferi célula a célula se cada `sim` de limite corta | `plataformas.md:93-98`, `:69`, `:249-250` |
| P2 Inventário do Maestro | 8 | 8 | Dizia que allow/ask não são executáveis, lendo só o `settings.json` | **Fechada no conteúdo.** Allow/ask existem no harness e o repositório não declara o bloco; confirmei que `.claude/settings.json` não tem `permissions`. **Falha na própria exigência de revalidar linhas** (ver defeito transversal) | `inventario-maestro.md:50`, `:131`; `claude-code.md:63` (a citação diz `:49`) |
| P3 Confronto e decisão | 7 | 8 | Pausar/retomar por "o mercado quase não tem"; taxa cortada em silêncio; teto cria a necessidade de suspender | **Fechada em 3 de 4.** Justificativa agora é "sem fonte"; retomar reconhecido no Claude Code; taxa desdobrada em DEPOIS com gatilho; totais 15+6+11=32 fecham. **Restam:** a linha 52 ainda põe como lacuna "`allow`/`ask` executáveis", contra a tela de políticas e o inventário; e a tela de orçamento desenha o efeito "suspender" enquanto pausar/retomar é DEPOIS com gatilho no próprio teto (circular) | `confronto-decisao.md:48-51`, `:52`, `:159-162`, `:177-185`; `administracao-03-orcamento.html:113` |
| P4 Lacunas declaradas | 7 | 8 | Não declarava ponto de execução nem caminho de aprovação humana do derrubar | **Parcial.** A declaração existe, mas na tela e no mapa, não nas seções "Limites"/"Lacunas declaradas". O README declara que a regra executável de endereço ambíguo não foi despachada | `workflow-01-sessao-de-agente.html:177`; `mapa-de-contextos.md:85-90`; `prototipo/README.md:139-141`; ausente em `inventario-maestro.md:119-133` e `plataformas.md:239-258` |
| P5 Mapa de contextos | 6 | 8 | Faltava dono do ponto de execução; relação Workflow → Regência; orçamento no contexto errado | **Fechada no essencial.** Hooks e `settings.json` como ponto de execução fora do corte; relação 5 nova; orçamento na Administração (§2, §6.3, §6.5, §7.1). **Restam:** `:243` ainda chama "núcleo compartilhado" de relação 5 (agora é a 6); `:89-90` diz que o hook é "o único ponto" executável, contra o inventário (allow/ask rodam no harness) | `mapa-de-contextos.md:80-90`, `:108`, `:114`, `:161-168`, `:243`, `:300` |
| P6 mensageria-01 | 8 | 9 | "Drenar outbox" não dizia quem pode | **Fechada.** Sessão dona ou regente por delegação; a tela nunca drena a caixa de outra sessão sem pedido explícito. Ressalva: "o ref de quem pede autoriza" é fraco (ref é endereço mutável), mas está declarado | `mensageria-01-caixa-de-entrada.html:87-89`, `:73`, `:80` |
| P7 mensageria-02 | 8 | 8 | Faltava dizer quem vê ou filtra outras sessões | **Fechada, mas a resposta cria conflito.** "Qualquer sessão lê as linhas" (todas, de todos os projetos) contradiz o default-deny que a tela de políticas declara. Escrita bem fechada: só a sessão dona acrescenta | `mensageria-02-livro-de-mensagens.html:111-112`; `administracao-02-politicas.html:239-241` |
| P8 mensageria-03 | 8 | 9 | Faltava confirmação humana antes de entregar à sessão errada | **Fechada.** Confirmação com nome, refs, projeto e vivo/morto; vai à fila de decisões; quem autoriza declarado. Resta ajuste: a linha "ref mudou no reinício" diz "pede confirmação", enquanto o mapa diz que o endereço morto é recusado | `mensageria-03-roteamento.html:84-87`, `:60-77`; `mapa-de-contextos.md:353` |
| P9 mensageria-04 | 8 | 8 | "Registrar status" e "Chamar estado_atual" sem dizer quem autoriza | **Fechada para 2 de 3.** Leitura livre; escrita pela sessão dona. A terceira ferramenta, `registrar_peca` (muda estado de peça no portão), aparece na tabela sem linha de quem autoriza e sem botão | `mensageria-04-protocolo.html:165-166`, `:100-101` |
| P10 administracao-01-catalogo | 8 | 8 | Modelo era só linha de registro, sem ligação com a política | **Fechada na ligação**: formulário, unicidade de nomes, ligação com roteamento e política, auditoria. **Abre buraco novo:** "a sessão dona cadastra o que é dela", incluindo "quem pode usar" e preço do modelo, o que lhe permite autorizar o próprio uso. A tela de orçamento diz que a sessão dona nunca reabre o próprio teto. A tela de políticas não tem regra de modelo para espelhar a ligação | `administracao-01-catalogo.html:153-185`, `:204-210`; `administracao-03-orcamento.html:116`, `:171`; `administracao-02-politicas.html:119-154` |
| P11 administracao-02-politicas | 6 | 9 | Sem precedência, padrão, escopo, caminho do ask e referências com Claude Code e Kiro | **Fechada.** deny > ask > allow; default-deny; escopo agente/papel/projeto; fluxo do ask até o ruling; ligação com `permissions`; Claude Code e Kiro com ask = sim; envio de mensagem sob allow/deny/ask. Ressalvas menores: o default-deny está afirmado sem dizer como se configura (o `defaultMode` padrão do Claude Code pergunta, não nega); falta o caso "pedido sem ruling" | `administracao-02-politicas.html:74-84`, `:196-209`, `:227-292` |
| P12 administracao-03-orcamento | 6 | 8 | Limite só declarado; efeito ao estourar; taxa "—"; relógio sem idade; 40 % mal lido | **Fechada no papel.** Efeitos avisar/recusar/suspender, quem autoriza, tetos por projeto/agente/modelo, unidade, 40 % relido como cota do regente, taxa DEPOIS, idade do relógio declarada como "—" com motivo. **Falta o mecanismo:** nenhuma linha diz qual ponto executa "recusar a chamada seguinte" ou "suspender a sessão". O mapa nomeia hooks, mas um hook barra uso de ferramenta, não gasto de modelo, e a ficha do Claude Code diz que não há teto de orçamento por sessão no CLI | `administracao-03-orcamento.html:79`, `:85-90`, `:108-118`, `:121-159`, `:97-98`; `claude-code.md:62` |
| P13 workflow-01 | 5 | 8 | Derrubar sem gate; botões contraditórios; sem o que se perde nem reversibilidade; subir em sessão viva; Gerente desprotegido | **Fechada em 5 de 6.** Confirmação com tarefa aberta, worktree, o que fica salvo e como religar; todos os botões de linha desabilitados; "reiniciar" com aviso de ref novo; Gerente marcado "protegida"; quem autoriza. **Restam:** (a) o ponto de execução está declarado como não desenhado (`:177`); (b) a reversibilidade não distingue `claude stop` de `claude rm` (a ficha diz que `stop` deixa a sessão religável), e a tela afirma que o contexto "não é recuperável" ao lado de "`claude --resume` reabre a sessão"; (c) o caminho derrubar → pedido de decisão do mapa não está desenhado na tela | `workflow-01-sessao-de-agente.html:103-113`, `:154-159`, `:162-178`; `mapa-de-contextos.md:161-168`; `claude-code.md:59` |
| P14 workflow-02 | 7 | 8 | "Bloqueado" e "esperando" sem ação | **Fechada.** Bloqueado abre o pedido de decisão, esperando abre a caixa de entrada, caída leva às mensagens endereçadas a ela, alerta com limiar, quem autoriza. **Defeito novo:** "reiniciar a sessão" está habilitado, sem confirmação, no alerta de sessão parada, enquanto a tela 01 põe o reiniciar atrás de gate humano | `workflow-02-estado-do-agente-vivo.html:102-124`, `:127-134` (botão em `:133`); `workflow-01-sessao-de-agente.html:103`, `:159` |
| P15 workflow-03 | 8 | 9 | Faltava cancelar ou reatribuir | **Fechada.** Cancelar: humano ou regente; a sessão dona não cancela a própria (Princípio II). Reatribuir: regente, com ref lido do `ListAgents`, nova tentativa, sem tarefa aberta em dois lugares. Regra de "travada" e declaração do livro de ponto parado no 064. Ressalva: a confirmação do cancelar não mostra o que se perde | `workflow-03-tarefa-aberta.html:115-139` |
| P16 workflow-04 | 7 | 8 | Contradiz o orçamento (aqui "nenhum teto", lá 40 %); piso sem risco declarado | **Fechada em 2 de 2:** o teto exibido é o da Administração (`:166-170`) e o risco de subcontagem tem seção própria (`:155-164`). **Defeito novo:** o resumo mostra "teto vigente 60 % (exemplo)" e a seção seguinte diz "nenhum teto declarado". Os 60 % não têm unidade (tokens, dólar ou % da cota semanal). Também não diz o efeito de controlar contra um piso (o teto pode ser ultrapassado sem ser visto) | `workflow-04-consumo-por-agente.html:85-90`, `:166-170`, `:163` |

## O que ainda falta para 9

Só para as peças abaixo de 9.

- **P12**: dizer qual ponto executa "recusar" e "suspender" e com que mecanismo concreto, ou rebaixar esses dois efeitos a DEPOIS com gatilho e deixar só "avisar" como ENTRA executável. Hoje o texto promete um corte cujo executor não está evidenciado.
- **P13**: distinguir `claude stop` (religável) de `claude rm` (irreversível) na caixa "o que fica salvo"; corrigir "o contexto não é recuperável" ao lado de `--resume`; desenhar na confirmação a passagem pelo pedido de decisão da Regência (relação 5 do mapa); manter o ponto de execução como dívida declarada.
- **P14**: desabilitar "reiniciar a sessão" em `workflow-02-estado-do-agente-vivo.html:133` e apontá-lo para a confirmação de `workflow-01-sessao-de-agente.html:154-159`.
- **P16**: reconciliar `:87` com `:169` (ou tirar o "teto vigente" do resumo); dar unidade ao percentual; declarar que o teto comparado com um piso pode ser estourado sem aviso.
- **P10**: tirar da sessão dona o poder de cadastrar "quem pode usar" e preço de modelo (alinhar com `administracao-03-orcamento.html:116`); espelhar na tela de políticas uma regra de modelo.
- **P9**: acrescentar a linha de quem autoriza `registrar_peca`.
- **P7**: justificar a leitura aberta do livro de todos os projetos contra o default-deny, ou restringi-la por projeto.
- **P5**: corrigir `:243` (relação 5 → 6) e a frase "o único ponto" em `:89-90`.
- **P3**: reescrever a lacuna da linha 52 (hoje "`allow`/`ask` executáveis") para "bloco `permissions` não declarado no repositório"; resolver a circularidade suspender ↔ pausar.
- **P2 e P3**: refazer as citações de `claude-code.md` (tabela do defeito transversal).
- **P4**: registrar nas seções "Limites"/"Lacunas declaradas" que o ponto de execução do controle e o caminho de aprovação do derrubar não estão desenhados.
- **P1**: separar orçamento e taxa em linhas, ou marcar por célula se o `sim` corta ou só avisa.

## Limites do que li

- **Não abri** `verifica-prototipo.py`, `qa-report.md`, `andamento.md`, os outros dois pareceres da rodada, nem as fichas além de `claude-code.md`. Não rodei nenhum script, nem o verificador.
- **Não conferi** as citações `arquivo:linha` de código do repositório (`server.py:479`, `multi-session.py`, `guard-immutables.py:149`).
- **Não conferi** o conteúdo de nenhuma célula da matriz contra as 25 fichas. Li a matriz e as notas.
- **Telas lidas:** as quatro da Mensageria e a `administracao-01-catalogo.html` a partir da linha 48 ou 72; as três do Workflow, também a partir da linha 48. Não li o cabeçalho e o CSS dessas telas, onde pode haver texto de contexto. Li inteiras `workflow-01-sessao-de-agente.html`, `administracao-02-politicas.html` e `administracao-03-orcamento.html`.
- A afirmação de que um hook barra ferramenta e não gasto de modelo vem do que a ficha do Claude Code diz sobre teto de orçamento (`claude-code.md:62`) e do meu conhecimento do harness. Não testei isso.

DIAGNÓSTICO: **mudou.** As lacunas da rodada 1 (gate do derrubar, precedência e escopo da política, efeito ao estourar, quem autoriza cada escrita) foram fechadas no papel. O que sobra são contradições entre telas (P7, P10, P14, P16), citações desatualizadas (P2, P3) e a ausência do mecanismo de execução do controle (P12, P13, P4, P5). Este último fio já aparecia em P4 e P5 na rodada 1 e agora é o principal; se a regente ler isso como "o mesmo diagnóstico", ele vale para P12, P13, P4 e P5, mas na rodada 1 era secundário.
