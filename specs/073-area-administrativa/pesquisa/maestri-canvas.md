# Maestri — o canvas infinito para orquestrar agentes de IA

- **URL**: https://www.themaestri.app/pt-br
- **Data da visita**: 2026-10-24
- **Como foi pesquisada**: WebFetch na página oficial em português (site do produto; não há documentação
  técnica separada aberta nesta visita). Não roda nesta máquina (app nativo macOS 15.4+, Apple Silicon).
- **O que foi aberto de verdade** (URL — o que a página realmente trazia):
  - `https://www.themaestri.app/pt-br` — página de produto: *"Cada um ganha um papel, todos conversam
    entre si e a operação inteira fica à sua frente"*. Recursos citados: cada terminal é um **nó** e roda
    Claude Code, Codex, OpenCode ou shell comum; **papéis** (ex.: "Unslopifier", "Bug Whisperer", "Git
    Wizard"); **portais** (janelas de navegador/emulador embutidas); **Prompt Composer** (digitar "@"
    aponta para terminal, nota ou portal); **chat e notas adesivas por terminal** (os próprios agentes
    escrevem progresso/resumos/decisões); canvas próprio **"MaestriCanvas"** (zoom, agrupamento, setas);
    **bandas** (agrupar terminais); **andares** (cópia isolada do workspace por *Copy-on-write* **APFS**);
    **Ombro** (assistente on-device que resume tarefas concluídas). Planos: Grátis (US$ 0), Pro
    (R$ 95, pagamento único), Times (licença por assento, até 100 assentos).
  - Comunicação entre agentes descrita como *"talk to each other through PTY (*Pseudo-Terminal*)"* —
    *"Just one agent typing into another's terminal"*, **sem API nem middleware**.

## Tabela fixa (spec 073)

| Grupo | Item | Resultado | Fonte (URL — o que foi visto) |
|---|---|---|---|
| CONTROLE | subir/derrubar sessão ou agente | **parcial** | themaestri.app — cada terminal é um nó e o app abriga terminais (Claude Code/Codex/OpenCode), mas a página **não** descreve controles explícitos de start/stop de sessão |
| CONTROLE | pausar | **—** | Nada visto na página sobre pausar |
| CONTROLE | retomar | **—** | Nada visto na página sobre retomar |
| CONTROLE | limites de orçamento e de taxa | **—** | A página não menciona orçamento, limite de gasto nem custo de tokens |
| CONTROLE | políticas allow/deny/ask | **—** | Nada visto na página |
| CONTROLE | aprovação humana | **—** | Nada visto na página |
| ADMINISTRAÇÃO | cadastro de agentes | **sim** | themaestri.app — "Cada um ganha um papel"; escolha do motor por terminal (Claude Code, Codex, OpenCode, shell) |
| ADMINISTRAÇÃO | papéis e permissões RBAC (*Role-Based Access Control*) | **parcial** | themaestri.app — existem **papéis** (instruções reutilizáveis com responsabilidade por agente), mas a página não descreve permissões granulares tipo RBAC |
| ADMINISTRAÇÃO | cadastro de skills/ferramentas/modelos | **parcial** | themaestri.app — "papéis" funcionam como instruções reutilizáveis; a palavra *skills* não aparece, e o modelo é herdado do motor escolhido |
| ADMINISTRAÇÃO | chaves e segredos | **—** | A página ressalva que o tráfego dos agentes não é interceptado; nada sobre cofre de chaves |
| ADMINISTRAÇÃO | configuração por projeto | **sim** | themaestri.app — "um canvas por contexto"; configuração em JSON e notas em Markdown |
| ADMINISTRAÇÃO | auditoria | **—** | A página anuncia "Zero telemetria" e tudo local; nada de trilha de auditoria |
| GERENCIAMENTO | lista de agentes vivos com estado | **parcial** | themaestri.app — "Vários agentes rodando" e "Você chega, olha e já sabe onde tudo está": o canvas mostra o estado, mas não há lista tabular de agentes com estado |
| GERENCIAMENTO | tarefa aberta | **parcial** | themaestri.app — notas adesivas por terminal escritas pelos agentes (progresso, resumos, decisões) |
| GERENCIAMENTO | última atividade | **parcial** | themaestri.app — o assistente **Ombro** "resume tarefas concluídas"; não é um campo de última atividade por agente |
| GERENCIAMENTO | consumo por agente/sessão/modelo | **—** | Nada visto na página |
| GERENCIAMENTO | custo | **—** | Nada visto na página |
| GERENCIAMENTO | filas e workers | **—** | Nada visto na página |
| GERENCIAMENTO | rastro/replay de sessão | **parcial** | themaestri.app — **andares** (cópia isolada do workspace por *Copy-on-write* APFS) para branch/PR/teste arriscado; não é replay de sessão |
| GERENCIAMENTO | alertas | **—** | Nada visto na página |
| INTERCOMUNICAÇÃO | mensagem entre agentes | **sim** | themaestri.app — agentes *"talk to each other through PTY"*, um digita no terminal do outro; "conexão entre agentes" está no plano Grátis |
| INTERCOMUNICAÇÃO | protocolos (A2A (*Agent-to-Agent*), MCP (*Model Context Protocol*)) | **—** | A página diz explicitamente que a comunicação é por PTY "sem API nem middleware"; MCP/A2A não são citados |
| INTERCOMUNICAÇÃO | caixa de entrada | **parcial** | themaestri.app — cada terminal tem **chat** com texto formatado, diagramas e tabelas; não é um inbox de agente |
| INTERCOMUNICAÇÃO | roteamento por nome/ref | **parcial** | themaestri.app — no **Prompt Composer**, digitar "@" aponta para terminal, nota ou portal conectado |
| INTERCOMUNICAÇÃO | livro de mensagens | **parcial** | themaestri.app — chat e notas por terminal guardam o histórico da conversa; não é um livro de mensagens entre agentes |
| INTERCOMUNICAÇÃO | colisão de nomes | **—** | Nada visto na página |

## Observações

- **Rodou local**: não (app nativo macOS Apple Silicon; não há binário para Windows/Linux citado nesta
  página além de "versões para Windows e Linux" sem link).
- **Natureza**: orquestração visual de terminais — o ponto forte é o **canvas** e a delegação por PTY;
  administração/governança (orçamento, RBAC, auditoria, alertas) **não** aparecem na página de produto.
- **Pago vs. livre**: Grátis (1 workspace, agentes ilimitados) · Pro (pagamento único) · Times (por assento).
- **Lacuna**: a página é de marketing, não documentação; várias células ficaram vazias por falta de fonte —
  não por ausência confirmada.
