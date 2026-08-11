# QA report 052 — Symlink não é porta de saída

- **Date**: 2026-08-11 · **Lane**: leve · **Verdict**: aprovado

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| ataque reproduzido antes | instalador escreve dentro de `/fora` | ✅ observado |
| depois da correção | `! refused (a symlink on this path leads outside the target): skills/…` e o arquivo em `/fora` intacto | ✅ |
| `scripts/check-installed.sh` | doze asserções, duas novas | ✅ |
| os outros quinze portões · plugin · build | verdes | ✅ |

## Closing tail — the evidence

- TAIL:review — revisão independente em contexto fresco. **Este ciclo nasceu de uma**: o
  achado é do parecer do ciclo 051, que o classificou como limite herdado do `cp -r` com
  consequência maior depois que o instalador ganhou poder de remover. A correção é a recusa
  que aquele parecer pediu, e o ataque dele virou asserção do portão.
- TAIL:security — é o ponto do ciclo. **Superfície**: escrita e remoção dentro de repositório
  de terceiro. **Vetor**: um *symlink* no alvo — que o dono do repositório pode ter criado
  por motivo legítimo — fazia o `cp` escrever fora e faria a poda **remover** fora.
  **Mitigação**: recusa em ambos os pontos, com o caminho nomeado; o script passa a fazer
  **menos**, que é a direção certa para quem apaga. **Limite declarado**: um *symlink* criado
  **entre** a checagem e a escrita não é coberto — é uma corrida que exigiria escrita atômica
  por descritor, desproporcional para um instalador que roda a pedido de quem o executa.
- TAIL:gate — DoD verde, dezesseis portões verdes. Aguarda o gate humano.

## Requirement coverage

- **FR1** — destino ou qualquer diretório acima dele sendo link → recusa nomeada.
- **FR2** — mesma checagem antes do `rm`.
- **FR3** — `refused N` no resumo.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
