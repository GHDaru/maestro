# Spec 073 — Área administrativa do Maestro

- **Status**: Draft · **Lane**: full · **Date**: 2026-10-24
- **Origin**: demanda do regente (sessão MAESTRO, 24/10) — pesquisar e propor, **sem construir
  software**, a área administrativa do Maestro: agentes e papéis, cadastro de skills, subir e
  derrubar sessões, estado e consumo dos agentes vivos, intercomunicação entre sessões.

## What and why

Um humano conduz muitos agentes (o método Maestro), mas a administração deles hoje é artesanal:
sessões sobem e caem à mão, o consumo é lido de saídas dispersas, e a intercomunicação vive de
mensagens ad hoc. Antes de desenhar (e muito antes de construir) a área administrativa, é preciso
saber **o que já existe no ecossistema** — plataformas de gateway de LLM (*Large Language Model*),
observabilidade de agentes, orquestração e controle de processos — para decidir com fonte, não com
memória. Este ciclo é **pesquisa**: quatro rodadas, nenhuma linha de software.

- **Rodada 1 (este ciclo)**: pesquisa de plataformas, com tabela fixa de funcionalidades e fonte
  verificável em cada célula.
- **Rodada 2**: confronto com o Maestro e decisão do que entra.
- **Rodada 3**: wireframes sobre contexto delimitado de DDD (*Domain-Driven Design*) e linguagem
  ubíqua, cada tela citando a plataforma de origem.
- **Rodada 4 (bar)**: três críticos em contexto fresco (controle, administração e gerenciamento de
  agentes, intercomunicabilidade) dão nota 0 a 10 por peça; **só passa com os três em 9 ou mais**.

## Functional requirements

> A rodada 1 não tem FR de software — tem critérios de aceite da pesquisa (abaixo). As rodadas
> seguintes acrescentam os seus quando o regente der o "segue".

- **FR1**: WHEN uma plataforma é pesquisada THEN ela tem arquivo próprio em
  `specs/073-area-administrativa/pesquisa/<slug>.md` com URL, data da visita, o que foi aberto de
  verdade (demo, docs, repositório, capturas) e a tabela fixa de funcionalidades.
- **FR2**: WHEN a rodada 1 fecha THEN `specs/073-area-administrativa/pesquisa/plataformas.md`
  consolida todas as plataformas numa matriz funcionalidade × plataforma com a fonte em cada célula.
- **FR3**: WHEN uma funcionalidade é marcada sim/não/parcial THEN existe fonte verificável (URL e o
  que foi visto) na célula ou no arquivo da plataforma.
- **FR4**: WHEN um worker entrega THEN `specs/073-area-administrativa/andamento.md` é atualizado (é
  a página de progresso viva do Darú).

### Tabela fixa de funcionalidades (quatro grupos)

- **CONTROLE**: subir/derrubar sessão ou agente, pausar, retomar, limites de orçamento e de taxa,
  políticas allow/deny/ask, aprovação humana.
- **ADMINISTRAÇÃO**: cadastro de agentes, papéis e permissões RBAC (*Role-Based Access Control*),
  cadastro de skills/ferramentas/modelos, chaves e segredos, configuração por projeto, auditoria.
- **GERENCIAMENTO**: lista de agentes vivos com estado, tarefa aberta, última atividade, consumo por
  agente/sessão/modelo, custo, filas e workers, rastro/replay de sessão, alertas.
- **INTERCOMUNICAÇÃO**: mensagem entre agentes, protocolos (A2A — *Agent-to-Agent*; MCP — *Model
  Context Protocol*), caixa de entrada, roteamento por nome/ref, livro de mensagens, colisão de
  nomes.

## Out of scope

- Construir qualquer software, tela, protótipo funcional ou esqueleto de código (as rodadas 2–4
  decidem antes; o bar da rodada 4 é o portão).
- Criar conta em serviço externo, usar credencial real ou colocar dado pessoal em arquivo.
- Decidir arquitetura da área administrativa (é a rodada 2, com o confronto).

## Acceptance criteria (DoD)

<!-- No checkboxes: this states what must hold; whether it held is the qa-report's job. -->

- Cada plataforma pesquisada tem `pesquisa/<slug>.md` com URL, data da visita, o que foi aberto de
  verdade e a tabela fixa (FR1).
- `pesquisa/plataformas.md` consolida todas numa matriz funcionalidade × plataforma com fonte em
  cada célula (FR2).
- Nenhuma funcionalidade sem fonte verificável (FR3) — célula sem fonte é célula vazia, não
  "sim".
- `andamento.md` atualizado a cada DONE (FR4).
- Busca na internet (WebSearch/WebFetch) obrigatória; capturas quando a ferramenta rodar local.

## Clarify

1. O orçamento: a sessão MAESTRO está em 19% do consumo semanal e para em 40%; workers rodam no
   gateway, mas cada DONE reporta os tokens gastos para o regente somar.
2. Worker06 participa da rodada 1 **até** o ciclo 072 chamá-lo de volta para a reverificação
   R1/R2 — a correção do 072 tem prioridade sobre a pesquisa.
