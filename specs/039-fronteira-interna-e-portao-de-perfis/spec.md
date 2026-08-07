# Spec 039 — Fronteira interna e portão para os perfis de agente

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-06
- **Origem**: dois pedidos do Steward na mesma conversa — (a) "não vamos fatiar", revertendo
  o ADR 0017 antes de qualquer arquivo se mover; e (b) "está bem dividido isto no
  repositório?", que virou auditoria e encontrou um defeito real.

> **Raia**: plena. **Ambiguidade** baixa (as duas mudanças são conhecidas e pequenas);
> **raio** amplo (mexe em ADR, no índice de decisões e em dois portões); **irreversibilidade**
> baixa — nada é apagado; o índice é append-only e o ADR 0017 fica intacto.

## O quê e por quê

**Parte A — o repositório estava afirmando uma decisão revertida.** O ADR 0017 foi aceito
com status "Aceito" dizendo *divisão em dois repositórios*; o roadmap tinha `F14b — aguarda
gate humano`; o `boundary.json` descrevia dois repositórios com nomes. O Steward reverteu
depois da tabela comparativa. Enquanto esses artefatos não mudassem, a próxima sessão leria
"vamos separar" como verdade vigente — que é o axioma A4 cobrando o preço.

**Parte B — `docs/agents/` era lista à mão sem portão.** A auditoria mediu:
`docs/agents/README.md` documenta 13 agentes com suas tools; `.claude/agents/` tem 13
executáveis; e `grep -l "docs/agents" scripts/*.sh` **não retorna nada**. O `check-roles.sh`
comparava o modelo operacional × agentes, nunca o índice de perfis × disco.

Os 13 batiam com os 13 no dia da auditoria. **É por isso que era perigoso**: parecia
saudável, e a saúde dependia de memória. É a família de falha que o ciclo 021 documentou —
três derivas simultâneas, todas de lista escrita à mão nunca comparada com o disco.

## Requisitos funcionais

- **FR1**: QUANDO uma decisão registrada em ADR for revertida, O SISTEMA DEVERÁ registrar a
  reversão em ADR novo e marcar o anterior como superado, sem editar o corpo do original.
- **FR2**: QUANDO um agente existir em `.claude/agents/`, O SISTEMA DEVERÁ falhar se ele
  não estiver documentado no índice de perfis.
- **FR3**: QUANDO o índice de perfis citar um agente, O SISTEMA DEVERÁ falhar se o arquivo
  não existir.
- **FR4**: QUANDO um agente tiver uma *tool* no disco, O SISTEMA DEVERÁ falhar se a linha
  dele no índice não a listar — é onde uma deriva silenciosa custa mais caro (princípio III:
  quem julga não escreve).
- **FR5**: QUANDO o índice declarar um total em prosa, O SISTEMA DEVERÁ falhar se o número
  divergir da contagem no disco.

## Fora de escopo

- Reestruturar `docs/`. A auditoria achou três incômodos menores (`docs/livro/` e
  `docs/jornada/` com um arquivo cada; PDFs gerados dentro de `docs/handbook/`; nomes de
  diretório que não codificam a regra de idioma) e a recomendação foi **não mexer**:
  consertar custa tocar 17 referências, e renome em massa já virou o anti-padrão 18 aqui.
- A duplicação de 32 arquivos em `plugin/maestro/`. É duplicação **com forcing function**
  (`package-plugin.sh --verify`), que é a forma mitigada — e ela acusou no ciclo 037.
- Comparar `perfis.md` (a prosa) com os agentes. O vínculo estrutural vive no `README.md`,
  que já existe para essa função; duplicá-lo em prosa seria checar as palavras, não o fato.

## Critérios de aceite (DoD)

- [x] ADR 0018 supersede o 0017; o 0017 recebe status de superado com o corpo intacto.
- [x] `boundary.json` descreve **domínios internos**, não repositórios; `check-boundary.sh`
      acompanha, incluindo as mensagens.
- [x] `check-roles.sh` cobre FR2–FR5 e foi **visto acusar** nas quatro condições.
- [x] O índice de decisões registra a reversão, e os dois registros errados do ciclo
      anterior são corrigidos por linha nova (append-only).
- [x] Portões continuam no estado esperado.

## Clarify

1. O `boundary.json` sobrevive à reversão? **Sim.** Ele resolve um problema que existe com
   um repositório só: antes dele, nenhum arquivo tinha dono declarado e verificado. O que
   muda é o vocabulário (domínio, não repositório) e a razão da terceira invariante.
