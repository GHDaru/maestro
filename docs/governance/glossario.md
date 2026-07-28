# Glossário — siglas e termos do Maestro

> Dicionário de todas as siglas usadas na governança e no handbook. Nos documentos, cada
> sigla é expandida na **primeira ocorrência**; aqui está a referência completa.

| Sigla / termo | Expansão | No Maestro | Onde |
|---|---|---|---|
| **ADR** | *Architecture Decision Record* | Registro **imutável** de uma decisão (contexto → decisão → consequências). | Cap 12 · `docs/adr/` |
| **API** | *Application Programming Interface* | Contrato de integração entre sistemas. | — |
| **ABAC** | *Attribute-Based Access Control* | Autorização por atributos — decidida **fora** do LLM. | Cap 1 · 10 |
| **RBAC** | *Role-Based Access Control* | Autorização por papel. | Cap 10 |
| **BDD** | *Behavior-Driven Development* | Testes em linguagem de comportamento/negócio. | Cap 9 |
| **Bounded context** | Contexto delimitado (DDD) | A **costura** por onde se corta o trabalho para paralelizar. | Cap 4 · 5 |
| **C4** | Modelo C4 (*Context, Container, Component, Code*) | Diagramas de arquitetura em 4 níveis. | Cap 8 (não adotado agora) |
| **CI** | *Continuous Integration* | Integração contínua — roda testes e gates a cada mudança. | Cap 8 · 9 |
| **CD** | *Continuous Delivery/Deployment* | Entrega/implantação contínua. | — |
| **DDD** | *Domain-Driven Design* | Desenho orientado ao domínio; dá os *bounded contexts*. | Cap 3 · 5 |
| **DoD** | *Definition of Done* | Critérios **verificáveis** de "pronto". | Cap 9 |
| **DoR** | *Definition of Ready* | Critérios de "pronto para começar" (spec executável sem adivinhar). | Cap 9 |
| **DORA** | *DevOps Research and Assessment* | Programa/4 métricas de desempenho de entrega. | Cap 2 |
| **DX** | *Developer Experience* | Experiência de quem desenvolve. | Cap 2 |
| **Fitness function** | Teste de arquitetura | Verifica as regras de dependência (DDD/hexagonal) no CI. | Cap 9 |
| **Forcing function** | Mecanismo que "força" | O que **falha/quebra** se um artefato não é mantido atualizado. | Cap 8 |
| **IA / AI** | Inteligência Artificial | O agente que executa sob orquestração. | — |
| **LLM** | *Large Language Model* | Modelo de linguagem; o motor do agente. | Cap 1 · 5 |
| **MCP** | *Model Context Protocol* | Protocolo para expor/consumir ferramentas a agentes. | — |
| **NNN** | Numeração de specs | Convenção `specs/NNN-nome/` (001, 002…). | Cap 3 · 11 |
| **OPA** | *Open Policy Agent* | Motor de política declarativa (`allow/deny/ask`). | Cap 10 |
| **OWASP** | *Open Worldwide Application Security Project* | Referência de segurança (ex.: LLM01 — prompt injection). | Cap 10 |
| **PII** | *Personally Identifiable Information* | Dados pessoais sensíveis (classe de risco "leitura sensível"). | Cap 10 |
| **PO** | *Product Owner* | Papel de decisão de produto (no Maestro, o humano/Steward). | Cap 6 |
| **PR** | *Pull Request* | Proposta de mudança revisável; na **raia leve**, é o próprio artefato. | Cap 8 · 11 |
| **PRD** | *Product Requirements Document* | Requisitos de produto; função absorvida pela **spec**. | Cap 8 |
| **QA** | *Quality Assurance* | Garantia de qualidade (testes/cobertura). | Cap 6 |
| **RACI** | *Responsible, Accountable, Consulted, Informed* | Matriz de responsabilidades: **R/C/I** delegáveis a agentes, **A** sempre humano. | Cap 6 |
| **Raia** | *Lane* de trabalho | Leve / plena / infra — quanto processo cada mudança recebe. | Cap 3 |
| **ReBAC** | *Relationship-Based Access Control* | Autorização por relacionamento. | Cap 1 |
| **RFC** | *Request for Comments* | Proposta de design para discussão (não adotada avulsa — ADR basta). | Cap 8 |
| **ROI** | *Return on Investment* | Retorno sobre o investimento — a tese executiva do Maestro. | — |
| **SDD** | *Spec-Driven Development* | Desenvolvimento dirigido por especificação. | Cap 3 |
| **SDET** | *Software Development Engineer in Test* | Engenheiro de testes. | Cap 6 |
| **SM** | *Scrum Master* | Papel do Scrum — cortado no Maestro (cerimônia de papel). | Cap 6 · 7 |
| **SPACE** | *Satisfaction, Performance, Activity, Communication, Efficiency* | Framework multidimensional de produtividade. | Cap 2 |
| **SSE** | *Server-Sent Events* | Streaming servidor→cliente. | — |
| **SAST / DAST** | *Static / Dynamic Application Security Testing* | Análise de segurança estática/dinâmica (DevSecOps leve). | Cap 9 |
| **Spec** | Especificação | A **fonte de verdade**: o input que gera o código. | Cap 3 |
| **TDD** | *Test-Driven Development* | Teste antes do código (red → green → refactor). | Cap 9 |
| **UI / UX** | *User Interface / User Experience* | Interface / experiência do usuário. | Cap 6 |
| **WIP** | *Work In Progress* | Trabalho em andamento — limitado pela **atenção humana**. | Cap 7 |
| **YAGNI** | *You Aren't Gonna Need It* | Não construir o especulativo; podar o que não paga. | Cap 12 |
