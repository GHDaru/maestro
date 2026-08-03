# Maestro — o processo em BPMN

> **BPMN** (*Business Process Model and Notation*, Notação de Modelagem de Processos de
> Negócio) — o método desenhado como processo, com raias por executor.
> **Cada caixa é um link**: clique para ir ao capítulo, receita ou norma que define aquele
> passo. O desenho é o índice do livro na ordem em que o trabalho acontece.

<div class="bpmn">

<div class="bpmn-raia">
  <div class="bpmn-rot"><b>Steward</b><small>humano · Accountable · os gates indelegáveis</small></div>
  <div class="bpmn-fluxo">
    <a class="bpmn-no bpmn-hum" href="../governance/operating-model.md"><b>Intenção</b><small>o quê · por quê · apetite</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-gate" href="../handbook/09-definition-of-ready-done.md">APROVA SPEC (DoR)</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-gate" href="../handbook/10-gates-classes-de-risco.md">APROVA PLANO</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-gate" href="../handbook/10-gates-classes-de-risco.md">GATE DE MERGE</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-gate" href="../receitas/rodar-a-retro.md">DÍVIDA DE ACHADOS?</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-hum" href="../receitas/rodar-a-retro.md"><b>Retro</b><small>erro → regra versionada ⟲</small></a>
  </div>
</div>

<div class="bpmn-raia">
  <div class="bpmn-rot"><b>Agentes de IA</b><small>13 subagentes estreitos</small></div>
  <div class="bpmn-fluxo">
    <a class="bpmn-no bpmn-ag" href="../handbook/03-spec-driven.md"><b>Especificar</b><small>spec-agent · EARS</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-ag" href="../agents/comunicacao.md"><b>Clarificar</b><small>ambiguidade → pergunta</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-ag" href="../handbook/05-orquestracao.md"><b>Planejar</b><small>plan-arquiteto</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-ag" href="../receitas/abrir-um-ciclo.md"><b>Fatiar</b><small>tasks por fronteira</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-ag" href="../handbook/04-fluxo-agentic-contexto.md"><b>Implementar</b><small>dev · diffs pequenos</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-ag" href="../agents/perfis.md"><b>Verificar</b><small>review fresco · security · qa</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-ag" href="../handbook/08-entregaveis-artefatos.md"><b>Documentar</b><small>tech-writer · mesmo PR</small></a>
  </div>
</div>

<div class="bpmn-raia">
  <div class="bpmn-rot"><b>Ramo de interface</b><small>só quando há tela</small></div>
  <div class="bpmn-fluxo">
    <a class="bpmn-gate" href="../governance/operating-model.md">TEM UI? senão, pula</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-ag" href="../agents/perfis.md"><b>Semântica</b><small>ux-semantica · papel antes do componente</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-art" href="../handbook/08-entregaveis-artefatos.md">ux-design.md</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-gate" href="../handbook/10-gates-classes-de-risco.md">APROVA UX</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../jornada/README.md"><b>Captura do build real</b><small>script versionado</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-ag" href="../jornada/README.md"><b>Heurística datada</b><small>achados + severidade</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-art" href="../jornada/README.md">journeys/NNN.md</a>
  </div>
</div>

<div class="bpmn-raia">
  <div class="bpmn-rot"><b>Automação</b><small>scripts · integração contínua</small></div>
  <div class="bpmn-fluxo">
    <a class="bpmn-no bpmn-aut" href="../receitas/abrir-um-ciclo.md"><b>new-cycle</b><small>esqueleto NNN</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../governance/principles.md"><b>Constitution Check</b><small>princípios I–VIII</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../receitas/escrever-criterio-verificavel.md"><b>Testes + fitness</b><small>8 portões · feliz + falha</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-gate bpmn-dod" href="../handbook/09-definition-of-ready-done.md">DoD VERDE?</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../handbook/11-rastreabilidade.md"><b>promote-main</b><small>+ registra o gate</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../livro/guia-editorial.md"><b>Publica</b><small>site · livro</small></a>
  </div>
</div>

<div class="bpmn-raia">
  <div class="bpmn-rot"><b>Distribuição</b><small>o método instalável</small></div>
  <div class="bpmn-fluxo">
    <a class="bpmn-no bpmn-aut" href="../receitas/instalar-o-maestro.md"><b>empacotar-plugin</b><small>fontes → pacote</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-gate" href="../receitas/instalar-o-maestro.md">PACOTE SINCRO?</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../receitas/instalar-o-maestro.md"><b>A · install-maestro.sh</b><small>o método inteiro</small></a>
    <span class="bpmn-ou">ou</span>
    <a class="bpmn-no bpmn-aut" href="../receitas/instalar-o-maestro.md"><b>B · /plugin install</b><small>agentes + skills + comandos</small></a>
    <span class="bpmn-ou">ou</span>
    <a class="bpmn-no bpmn-aut" href="../receitas/instalar-o-maestro.md"><b>C · npx skills add</b><small>só as skills</small></a>
  </div>
</div>

<div class="bpmn-raia">
  <div class="bpmn-rot"><b>Portões</b><small>a DoD executável — 8 checks</small></div>
  <div class="bpmn-fluxo">
    <a class="bpmn-no bpmn-aut" href="../handbook/06-papeis-raci.md"><b>check-agents</b><small>invariantes dos 13 papéis</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../governance/principles.md"><b>check-roles</b><small>papel × executável · princípios × check</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../receitas/instalar-o-maestro.md"><b>check-install</b><small>método instalado de fato</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../adr/README.md"><b>check-language</b><small>inglês no instalável</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../handbook/03-spec-driven.md"><b>check-cycle</b><small>raia justificada · elo do commit</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../handbook/11-rastreabilidade.md"><b>check-links</b><small>todo link do repo resolve</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../livro/guia-editorial.md"><b>check-chapters</b><small>9 seções · skill × capítulo</small></a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-no bpmn-aut" href="../receitas/rodar-a-retro.md"><b>check-retro</b><small>dívida de achados</small></a>
  </div>
</div>

<div class="bpmn-raia">
  <div class="bpmn-rot"><b>Artefatos</b><small>a trilha auditável</small></div>
  <div class="bpmn-fluxo">
    <a class="bpmn-art" href="../handbook/03-spec-driven.md">spec.md</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-art" href="../adr/README.md">plan.md + ADR</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-art" href="../receitas/abrir-um-ciclo.md">tasks.md</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-art" href="../handbook/04-fluxo-agentic-contexto.md">código + testes</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-art" href="../handbook/08-entregaveis-artefatos.md">qa-report.md</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-art" href="../livro/guia-editorial.md">CHANGELOG · docs</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-art" href="../records/README.md">decisoes.jsonl</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-art" href="../governance/axioms.md">axioma / teorema</a>
    <span class="bpmn-seta">→</span>
    <a class="bpmn-art" href="../governance/principles.md">regra nova ⟲</a>
  </div>
</div>

<p class="bpmn-legenda">
  <span><i class="bpmn-hum"></i> humano (barra sólida à esquerda)</span>
  <span><i class="bpmn-ag"></i> agente de IA</span>
  <span><i class="bpmn-aut"></i> automação (script/CI)</span>
  <span>◆ gate humano (ouro) · ◆ DoD mecânica (verde)</span>
  <span>▭ tracejado — artefato produzido</span>
</p>

</div>

> **Versão para apresentação** (imagem única, boa para slide e impressão):
> [`05-bpmn-processo.png`](05-bpmn-processo.png) · fonte:
> [`fontes/05-bpmn-processo.html`](fontes/05-bpmn-processo.html) · gerado no ciclo 017,
> raia de distribuição no ciclo 019, versão navegável no ciclo 020, raia de portões e
> gatilho da retro no ciclo 035.

![BPMN do Maestro](05-bpmn-processo.png)

## Como ler

**Sete raias, por quem executa:**

| Raia | Executa |
|---|---|
| **Steward** (humano) | Intenção · os três gates indelegáveis · a retrospectiva |
| **Agentes de IA** | Especificar → clarificar → planejar → fatiar → implementar → verificar → documentar |
| **Ramo de interface** | Só quando há tela: semântica (papel antes do componente) → `ux-design.md` → ◆gate de UX → captura do build real → heurística datada → journey |
| **Automação** | Esqueleto do ciclo · Constitution Check · testes e *fitness functions* · promoção com registro · publicação |
| **Distribuição** | O método sai do repositório: empacotar → ◆pacote sincronizado? → três camadas (A script completo · B plugin do Claude Code · C `npx skills add`) |
| **Portões** | A Definição de Pronto executável: oito checks que falham sozinhos (agentes, papéis, instalação, idioma, ciclo, links, capítulos, dívida de achados) |
| **Artefatos** | A trilha auditável: `spec.md` → `plan.md`+ADR → `tasks.md` → código+testes → `qa-report.md` → docs → `decisoes.jsonl` → achado aberto → axioma/teorema → regra nova |

**O losango é onde o fluxo para.** Quatro em ouro (humanos, indelegáveis): aprovar a
spec (DoR), aprovar o plano, o gate de merge e — na raia infra — autorizar deploy ou
migração. Um em verde: a Definição de Pronto (DoD), mecânica, que bloqueia sozinha.

## As cinco leituras do desenho

1. **Antes de tudo vem a raia de trabalho**: `ambiguidade × raio × irreversibilidade`
   decide quanto processo a mudança recebe. Na raia *leve*, o pull request é o artefato e
   as três primeiras caixas são puladas — o desenho completo é o caso *pleno*.
2. **O gate não julga o raciocínio do agente — localiza a responsabilidade.** Por isso ele
   está na raia do humano, não na dos agentes.
3. **Feature com tela abre um ramo** — o ramo de interface não é opcional quando há UI:
   papel semântico **antes** do componente, gate de UX, e jornada viva (captura gerada do
   build real + heurística **datada**). Heurística mais velha que a captura é documentação
   vencida. *(Acrescentado no ciclo 018: o desenho anterior refletia o toolkit, não a norma.)*
4. **O método é instalável** — a raia de distribuição mostra o Maestro saindo do próprio
   repositório em três camadas, cada uma declarando o que **não** leva (ADR 0012).
5. **O laço fecha na retrospectiva — e agora ela tem gatilho.** O losango *dívida de
   achados* é o relógio que faltava: achado que não coube no ciclo entra no índice como
   `achado-NNN` e `check-retro.sh` cobra a cerimônia quando a dívida passa de quatro abertos
   ou de seis ciclos de idade. Erro recorrente vira regra versionada, e a regra nova é
   argumentada contra os [axiomas](../governance/axioms.md). *(ciclo 035.)*
6. **A raia de portões é a Definição de Pronto executável.** Oito checks que falham sozinhos,
   cada um nascido de um achado real — nenhum deles foi projetado por antecipação.

**Ver também**: [SIPOC](04-sipoc.md) (o mesmo ciclo como cadeia fornecedor→cliente) ·
[Fluxo](03-fluxo.md) (a linha do tempo) · [capítulo 01](../handbook/01-principio-central.md)
(por que os gates estão onde estão).
