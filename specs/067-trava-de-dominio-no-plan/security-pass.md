# TAIL:security — ciclo 067 (trava de domínio no plan)

Passagem independente em contexto fresco (agente `security`, 20/10/2026, só leitura; sem shell,
medido por leitura e grep sobre o worktree em `b5775ac` + artefatos). Classe de risco declarada
no plano: **baixa** (o portão só lê `specs/*/plan.md`; roda na CI e localmente).

## Achados

1. **(baixa) Bloco 3b — injeção/execução: nenhuma.** `scripts/check-conformance.sh:362-383`: o
   conteúdo do `plan.md` entra só por stdin (`<<<"$line"`), nunca na expressão do `sed`; `${k}`
   vem do array constante `DOMAIN` (`:68`). Sem `eval`, `$(...)` sobre conteúdo nem
   `printf "$conteudo"`. Um `)` dentro de crase ou um `|` da célula Why produzem **falso
   vermelho** (item inválido, `:383`), nunca falso verde. Único falso verde possível: `grep -m1`
   (`:362`) pega a *primeira* linha com `DOM:x=` — uma menção em prosa antes da tabela vence a
   linha real; e `edge(x)` aceita motivo de 1 caractere (`:379`). Correção mínima (ciclo
   seguinte): ancorar o grep na linha de tabela e exigir tamanho mínimo dentro do parêntese.
   `pipefail` respeitado; `grep -m1 FILE || true` não está em pipe (anti-padrão 21 não se aplica).
2. **(baixa) Knob `MAESTRO_MIN_CYCLE_DOMAIN` fecha, não abre.** `:60-67`: zeros à esquerda
   resolvidos por `10#`; número além de 2^63 faz o bash enrolar em silêncio, mas qualquer
   resultado ≤ 67 só aperta (`:357`) e > 67 é recusado (exit 2). Vazio cai no default. Sem
   caminho fail-open. Opcional: limitar a `^[0-9]{1,3}$`.
3. **(média, herdado) DORA inflável por evento forjado.** `painel/server.py:141-147,158`:
   `ambiente` vem de `evidencia` (texto livre) e **ausência conta como produção**;
   `grava_evento` (`:391-399`) e `valida_evento` (`:368-388`) não exigem `ambiente` em `deploy`
   nem autenticam `autor`. É a mesma classe do achado 2 do ciclo 066; o 067 só **subtrai**
   deploys (filtro), não amplia a superfície. Correção mínima: `deploy` exige
   `evidencia.ambiente`; ausente ≠ produção. `index.html:293,299` interpola só inteiros do
   servidor e `esc()` nos textos — sem XSS novo.
4. **Segredos/rede/escrita:** grep em `check-conformance.sh` por `curl|wget|http|tee|mktemp|TOKEN|SECRET`
   → zero; o script só lê. `plan-template.md:66-69` adiciona 4 linhas de tabela. Nenhuma credencial.

## Veredito

TAIL:security verde — sem injeção, sem fail-open, sem segredo; 1 achado médio herdado (DORA sem
autenticação, 066-#2, já dívida do 072) e 2 baixas de robustez do grep, registradas para o ciclo
que tocar o bloco 3b. Classe efetiva: leitura (Princípio III).
