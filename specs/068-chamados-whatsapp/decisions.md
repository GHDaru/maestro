# Decisions: Chamados pelo WhatsApp

## ADR-001: Repositório próprio `chamados`, com a conversa conduzida pela nossa aplicação

**Data**: 06/10/2026 · **Decidido por**: Gilsiley (repositório próprio, só números cadastrados, respostas no G0, G1 e G7, rede nos dois sentidos), com a forma técnica proposta pela Assistente.

### Context

O padrão do chamado (`hindiana DOCS/processo/padrao-chamado.md`, 05/10) põe cada chamado numa pasta `specs/<id>/`, até aqui dentro do repo do produto. A entrada pelo WhatsApp traz texto e capturas do cliente, escritos por terceiros, para dentro da trilha. Além disso, um processo automático passa a commitar. Duas perguntas: onde o chamado vive e quem conduz a conversa de abertura.

### Options considered

1. **Tudo em `hindiana/specs/NNN-slug/`**: uma só árvore com código, spec e chamado. Contras: dado de cliente (relato, captura, nomes) no repo que vai para produção; um processo automático commitando no repo do produto; mistura do registro do caso com o artefato de engenharia.
2. **Repositório próprio `chamados/NNN-slug/`** para o registro do caso (abertura, conversa, evidência do cliente e arquivos de gate), com spec, plan e tasks técnicos em `hindiana/specs/NNN-slug/` no mesmo número. Contras: dois lugares por chamado; o conferidor precisa resolver hashes do hindiana a partir do outro repo.
3. **Conversa conduzida no n8n** (máquina de estados nos nós do n8n) e nossa aplicação recebendo só o chamado pronto. Contras: regra de negócio fora do git e sem teste; cada mudança de pergunta é edição manual no n8n.
4. **Conversa conduzida pela nossa aplicação**, com o n8n só como transporte (normaliza e devolve). Contras: a aplicação guarda estado de conversa (sqlite) e precisa responder rápido.

### Decision

Escolhemos o **repositório próprio `chamados`** (opção 2) e a **conversa na nossa aplicação** (opção 4).

O repositório próprio separa o dado do cliente do código que vai para produção e deixa o processo automático commitar sem tocar no repo do produto. A ligação com a engenharia é o número: `chamados/098-x` ↔ `hindiana/specs/098-x`, e o `G1` aponta para a spec técnica `@ hash`. A conversa na aplicação mantém regra, textos e mapa gate → etapa versionados e testados no mesmo lugar que o conferidor. O n8n fica como cano, trocável.

### Consequences

- **Boas:**
  - O telefone e o texto bruto do cliente nunca entram no repo do produto.
  - A regra da conversa e as mensagens têm teste automático (SC-003, SC-005).
  - O painel junta os dois repos pelo número.
  - Trocar o n8n por outro transporte não muda a regra.
- **Ruins:**
  - Dois lugares por chamado. O conferidor e o painel precisam de `repos: [chamados, hindiana]`, e o número precisa ser único entre os dois (FR-003).
  - A aplicação de entrada vira um serviço a mais na rede interna, com segredo, lista de IPs e monitoramento.
  - A decisão de 05/10 ("tudo no hindiana") passa a valer para a engenharia; o registro do caso sai para o repo `chamados`. A mudança de `ola/especificacao` e `.maestro` (depois do push da 095-b) segue a mesma linha.
