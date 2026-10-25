# Portainer CE

- **URL**: https://docs.portainer.io/
- **Data da visita**: 2026-10-24
- **Como foi pesquisada**: WebFetch na documentação oficial (docs.portainer.io) e no site
  portainer.io — ver lista abaixo. Tentei a **demo pública** `https://demo.portainer.io` (e
  `https://demo.portainer.io/`) e ambas falharam com **`connect ECONNREFUSED 114.23.206.2:443`**
  — a demo **não abriu**. `docker` **não existe** nesta máquina, então nada foi executado
  localmente. Tudo veio de leitura de documentação.
- **O que foi aberto de verdade** (todos via WebFetch, HTTP 200 salvo indicação):
  - https://docs.portainer.io/ — Home. Descreve CE (*Community Edition*) e BE (*Business
    Edition*): "Portainer Community Edition (CE) is our free, open source option for home users
    and hobbyists"; "CE does not include all the features available in Business Edition";
    BE "easily build and manage containers in Kubernetes, Docker, Docker Swarm, Podman and
    Azure ACI", com "Role-Based Access Control".
  - https://docs.portainer.io/user/docker — Índice do menu Docker: Dashboard, Templates,
    Stacks, Services, Containers, Images, Networks, Volumes, Configs, Secrets, Events, Host,
    Swarm.
  - https://docs.portainer.io/user/docker/containers — Lista/gestão de contêineres; botão
    "Add container"; coluna "Images up to date"; "inspect it, edit or duplicate it", "attach
    volumes, view logs and statistics", "access its console".
  - https://docs.portainer.io/user/docker/containers/view — Detalhe do contêiner: "the
    container's status and details"; "a number of actions available, including starting,
    stopping and removing the container"; webhook, logs, inspect, stats, console.
  - https://docs.portainer.io/user/docker/containers/advanced — Configurações avançadas de
    criação/edição: command, volumes, network, environment variables, labels, **restart
    policy** (Never/Always/On failure/Unless stopped), runtime & resources, capabilities.
  - https://docs.portainer.io/user/docker/stacks — "A stack is a collection of services,
    usually related to one application or usage"; linha órfã, indicadores de imagem; subpáginas
    "Add a new stack", "Inspect or edit a stack", "Remove a stack".
  - https://docs.portainer.io/user/docker/secrets — "The Secrets menu is only available to
    Docker Swarm environments"; "Secrets are encrypted during transit and at rest in Docker
    Swarm"; "In Portainer you can add and remove secrets for use in deployments".
  - https://docs.portainer.io/user/docker/templates — "deploy a container (or a stack of
    containers) to an environment with a set of predetermined configuration values".
  - https://docs.portainer.io/admin/user — Índice de usuários; "Add users to teams then assign
    them to roles (Business Edition)".
  - https://docs.portainer.io/admin/user/add — "Enter a username and a strong password"; "You
    can also set whether this user is an Administrator as well as add the user to any teams".
  - https://docs.portainer.io/admin/user/teams — "Use teams to control user access to
    environments, container and service enablement, and volume control".
  - https://docs.portainer.io/admin/user/roles — RBAC: "Portainer Business Edition comes with
    Role-Based Access Control (RBAC)"; papéis Environment administrator, Edge administrator,
    Operator, Helpdesk, Namespace Operator, Standard User, Read-Only User, Administrator,
    Team Leader; "A single user or team can have different roles for different environments".
  - https://docs.portainer.io/advanced/docker-roles-and-permissions — "Role-Based Access
    Control is only available in Portainer Business Edition"; tabela de papéis (EA/OP/HD/ST/RO)
    × operações por recurso (Containers, Stacks, Images, Volumes, Secrets...).
  - https://docs.portainer.io/admin/settings/authentication — Autenticação interna
    ("encrypting user passwords and storing them in the local Portainer database"), tamanho
    mínimo de senha, "session lifetime" (padrão 8 h), e provedores externos LDAP, Active
    Directory e OAuth.
  - https://docs.portainer.io/admin/settings/credentials — "The Shared credentials feature is
    only available in Portainer Business Edition"; tipos Sidero Omni, SSH e Git.
  - https://docs.portainer.io/admin/registries — Registries: "a repository of container images
    or OCI-format Helm charts"; "OCI registries are only supported in Portainer Business
    Edition"; "browse and manage your registries" (BE).
  - https://docs.portainer.io/admin/environments — Environments: "Endpoints were renamed to
    Environments in version 2.10"; "Environments can be organized in groups and given tags";
    "One Portainer Server instance can manage multiple environments"; "access control per
    environment, group, or policy".
  - https://docs.portainer.io/admin/logs — "Within the Portainer Business Edition UI you can
    view authentication and activity logs".
  - https://docs.portainer.io/admin/logs/activity — Activity log (BE): log de "all actions
    taken through Portainer ... including actions via `kubectl exec`, container exec, node
    shell and pod-exec websocket sessions"; cada entrada tem "date and time, user, endpoint,
    and action"; "read-only and cannot be edited"; exporta CSV.
  - https://docs.portainer.io/start/install-ce — Instalação do CE; aponta para requisitos.
  - https://docs.portainer.io/start/requirements-and-prerequisites — Tabelas de versões de
    Docker testadas; Portainer Agent exige "TCP port `9001` ... accessible on the Agent";
    "The Portainer Edge Agent does not require any open ports".
  - https://docs.portainer.io/llms.txt — Índice completo da documentação (usado para achar as
    páginas acima).
  - https://www.portainer.io/pricing — Planos pagos Starter ($1,045/yr), Scale ($2,095/yr),
    Enterprise (Custom); "Every plan includes all Business Edition features from day one".
  - https://demo.portainer.io e https://demo.portainer.io/ — **`connect ECONNREFUSED
    114.23.206.2:443`** (demo não abriu).

## Tabela fixa (spec 073)

| Grupo | Item | Resultado | Fonte (URL — o que foi visto) |
|---|---|---|---|
| CONTROLE | subir/derrubar sessão ou agente | sim | docs.portainer.io/user/docker/containers/view — "a number of actions available, including starting, stopping and removing the container"; docs.portainer.io/user/docker/stacks — "Remove a stack" |
| CONTROLE | pausar | — | — |
| CONTROLE | retomar | — | — |
| CONTROLE | limites de orçamento e de taxa | — | — |
| CONTROLE | políticas allow/deny/ask | parcial | docs.portainer.io/advanced/docker-roles-and-permissions — RBAC (BE) concede/nega operações por papel ("Role-Based Access Control is only available in Portainer Business Edition"). **Não há o modo "ask"/aprovação** |
| CONTROLE | aprovação humana | — | — |
| ADMINISTRAÇÃO | cadastro de agentes | sim | docs.portainer.io/admin/environments — "One Portainer Server instance can manage multiple environments"; docs.portainer.io/start/requirements-and-prerequisites — Portainer Agent em "TCP port `9001`" (registro de host Docker via Agent) |
| ADMINISTRAÇÃO | papéis e permissões RBAC | sim | docs.portainer.io/admin/user/roles — "Portainer Business Edition comes with Role-Based Access Control (RBAC)"; papéis Environment administrator/Operator/Helpdesk/Standard User/Read-Only User/Administrator. **Só na Business Edition** |
| ADMINISTRAÇÃO | cadastro de skills/ferramentas/modelos | sim | docs.portainer.io/user/docker/templates — "deploy a container (or a stack of containers) to an environment with a set of predetermined configuration values" (templates/modelos) |
| ADMINISTRAÇÃO | chaves e segredos | sim | docs.portainer.io/user/docker/secrets — "add and remove secrets for use in deployments" (Docker Swarm); docs.portainer.io/admin/settings/credentials — "Shared credentials ... only available in Portainer Business Edition" (SSH, Git, Sidero Omni) |
| ADMINISTRAÇÃO | configuração por projeto | sim | docs.portainer.io/admin/environments — "Environments can be organized in groups and given tags"; "One Portainer Server instance can manage multiple environments" |
| ADMINISTRAÇÃO | auditoria | parcial | docs.portainer.io/admin/logs + docs.portainer.io/admin/logs/activity — log de "all actions taken through Portainer" com "date and time, user, endpoint, and action". **Só na Business Edition** |
| GERENCIAMENTO | lista de agentes vivos com estado | sim | docs.portainer.io/user/docker/containers/view — "the container's status and details"; docs.portainer.io/user/docker — menu Containers/Dashboard |
| GERENCIAMENTO | tarefa aberta | — | — |
| GERENCIAMENTO | última atividade | — | — |
| GERENCIAMENTO | consumo por agente/sessão/modelo | — | — |
| GERENCIAMENTO | custo | — | — |
| GERENCIAMENTO | filas e workers | — | — |
| GERENCIAMENTO | rastro/replay de sessão | parcial | docs.portainer.io/admin/logs/activity — rastro de ações em sessões (exec/console/websocket) com "date and time, user, endpoint, and action"; "read-only and cannot be edited". **É trilha de auditoria, não replay de sessão; só BE** |
| GERENCIAMENTO | alertas | — | — |
| INTERCOMUNICAÇÃO | mensagem entre agentes | — | — |
| INTERCOMUNICAÇÃO | protocolos (A2A, MCP) | — | — |
| INTERCOMUNICAÇÃO | caixa de entrada | — | — |
| INTERCOMUNICAÇÃO | roteamento por nome/ref | — | — |
| INTERCOMUNICAÇÃO | livro de mensagens | — | — |
| INTERCOMUNICAÇÃO | colisão de nomes | — | — |

## Observações

- **CE × BE — a separação que importa**: a Portainer **CE** administra Docker/Docker Swarm/
  Kubernetes/Podman/Azure ACI com UI (*User Interface*), templates, stacks, contêineres,
  imagens, volumes, redes, secrets (Swarm). Já **RBAC**, **auditoria** (logs de activity e
  authentication), **shared credentials**, **registries OCI e browse/manage de registries**
  são **Business Edition**. A Home diz explicitamente: "CE does not include all the features
  available in Business Edition".
- **Demo pública não abriu**: `demo.portainer.io` recusou conexão (ECONNREFUSED) nas duas
  tentativas; portanto não houve observação de UI ao vivo — só documentação.
- **Não achei** (célula vazia): pausar/retomar contêiner, limites de taxa/orçamento, aprovação
  humana, filas/workers, consumo por recurso, custo por recurso, alertas, e todo o bloco de
  **intercomunicação** (mensagens entre agentes, A2A/MCP, inbox, roteamento por nome, livro de
  mensagens, colisão de nomes) — a Portainer não é uma plataforma de agentes; nada disso
  aparece na documentação.
- **Ambiente local**: `docker` **não existe** nesta máquina ("O termo 'docker' não é
  reconhecido..."); nada foi instalado nem executado. Pesquisa 100% documental.
- **Preços (site)**: os planos do site são **Business Edition** (Starter/Scale/Enterprise). O
  texto "Running Portainer non-commercially ...?" aponta para Home & Student, mas a página de
  preços **não** traz valor da CE (ela é gratuita e open source, conforme a Home).
