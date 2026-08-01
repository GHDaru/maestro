---
name: combater-amontoado
description: Checklist de revisão didática que transforma documento denso ("amontoado" — muita sigla sem dicionário, tudo numa página, sem narrativa) em texto claro, sem alterar o conteúdo técnico. Use quando estiver escrevendo ou revisando qualquer doc do Maestro (handbook, guia, README, ADR), quando um texto tiver siglas não explicadas ou jargão órfão, ou quando alguém disser que um documento está "pesado", "denso" ou "difícil de entender".
---

# Combater o amontoado

## Iron Law

```
NENHUMA SIGLA NUA — TODA SIGLA EXPANDIDA NA 1ª OCORRÊNCIA E NO GLOSSÁRIO
```

**Violar a letra desta regra é violar o espírito dela.** Isso NÃO é desculpa:
- "Essa sigla todo mundo conhece" — o leitor de amanhã (ou o agente novo) não conhece.
- "Expando depois" — depois é onde nasce o amontoado.

"Amontoado" é o defeito nomeado pelo Steward: documento denso, muita sigla sem dicionário,
tudo empilhado sem storytelling. Esta skill é a régua para corrigir a **forma** — nunca o
fato técnico.

## Quando disparar

Escrevendo/revisando doc do Maestro; texto com sigla não explicada ou jargão órfão; feedback
de "pesado/denso/difícil".

## Checklist (cada item é verificável)

1. **Um assunto por página/seção.** Se a seção mistura dois temas, separe. (Regra do
   `didatica-editor`.)
2. **Sigla expandida na 1ª ocorrência** e presente no glossário. Ex.: "DoD (Definition of
   Done — o que conta como pronto)". Check: nenhuma sigla nova aparece "nua".
3. **Zero jargão órfão** — todo termo especializado tem definição acessível a um clique
   (glossário) ou inline. Se não dá pra linkar, explique em uma frase.
4. **Ordem que conta história**: do concreto para o abstrato, do problema para a regra.
   Comece pelo *porquê*, não pela taxonomia.
5. **Exemplo > definição seca.** Toda regra ganha um exemplo real (de preferência de um ciclo
   nosso).
6. **Preserve o conteúdo.** Reescreveu o fato técnico? Saiu do escopo desta skill — isso é
   decisão do autor/arquiteto, não do editor.

## Como aplicar

- Leia o doc uma vez marcando cada item do checklist que falha.
- Corrija forma, ordem e glossário; **não** invente nem remova fato.
- Se faltar um termo no glossário, adicione lá (fonte única) e linke — não redefina local.

## Exemplo

> ❌ "O DoR e o DoD gateiam o ciclo via RACI." (3 siglas nuas, sem história)
> ✅ "Antes de começar, checamos se a spec está pronta (DoR — Definition of Ready). No fim,
> se está feita (DoD — Definition of Done). Quem aprova cada porta é o dono (o *Accountable*
> do RACI)." (siglas expandidas, ordem narrativa, papel explicado)

**Consumido por:** `didatica-editor` (aplica), `tech-writer` (integra no PR).
