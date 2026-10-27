# Gate de plano do ciclo 074 — decidido por delegação (ADR 0026), 27/10/2026, sobre 1fc978b

**Decisão da regente: APROVADO COM AJUSTES.** Crítico em contexto fresco: `process-guardian`
(Sonnet). Os ajustes são de texto e **não bloqueiam o início da base**: Worker02 começa T01/T02
e Worker06 começa T07 (fixtures) **agora**; o Gerente aplica os ajustes no `plan.md`/`tasks.md`
no commit seguinte, antes de despachar T03–T06.

## Bloqueantes aceitos

- **B1** `plan.md` ganha `## Complexity Tracking` (Princípio IV: "abre offline", "recarregar
  restaura" **e** "18 elementos com efeito" julgados pelo crítico que anda — S4/S7/S2;
  inevitável porque não há verificação de fonte; limitado pelo roteiro e reversível) e fecha com
  "Veredito: sem violação; um desvio declarado no IV".
- **B2** toda tarefa T01–T12 traz a linha `DoD:` com comando e valor esperado (os exemplos do
  crítico valem como estão; skill `verifiable-dod`).
- **B3** T12 (glossário) executa **antes** da T03, mesmo dono (uma tarefa ativa por sessão,
  `task-ledger.md`), e pousa antes do primeiro verde do T09.
- **B4** T07 (fixtures) começa junto com a T01; T03–T06 só após T02 **e** T07 integrados; T02
  ganha o DoD "carrega as oito fixtures sem erro".

## Secundários aceitos

- **S1** o esqueleto do `verifica-navegacao.py` com o corpus de mutação (f) entra logo depois da
  T02 (Princípio IV: o portão nasce antes das telas); o "primeiro verde" fica na integração.
- **S3** o DONE vai à **sessão regente viva, conferida no `ListAgents` na hora** — nenhum ref é
  fixado em documento versionado (o briefing § 6 fica superado neste ponto; registrar no Clarify).
- **S4** `prototipo/acoes/*.js` aceito como acréscimo declarado; o verificador (e) aceita
  `<script src>` **local**.
- **S5** `tarefa.json` com Worker06 e MAESTRO ("—" com motivo); "16º ENTRA" → "ENTRA (correção 2)".
- **S6** siglas antes do cabeçalho do plano; `DOM:` do plano distinguido de DOM (Document Object Model).
- **S7** `spec.md` FR4: irreversíveis = reiniciar, derrubar, entregar a destino não resolvido, estourar teto.
- **S8** (g) **importa** o módulo do 073 com `importlib` (nome com hífen), reutiliza o parser e os
  termos do glossário e percorre `telas/**/*.html`; o arquivo do 073 **não é editado**; a regra 1
  (`data-fonte` em todo `<a>`/`<button>`) vale nos links da trilha.
- **S9** (h) falha também se `data-acao="derrubar"` não declarar `data-alvo`.
- **S10** T11 pendente (design system, condicionada ao 073) não bloqueia o DONE; estado no qa-report.
- **S11** `plan.md:28`: "gate decidido pela regente por delegação (ADR 0026), com crítico em
  contexto fresco; o gate de merge segue humano e não delegável".
- **S12** mensagens e docstring do `verifica-navegacao.py` em **inglês** (ADR 0014, como o 073).
- `.claude/launch.json` passa a ser rastreado neste PR (resposta ao Gerente).

## Parecer do crítico (síntese)

Constitution Check com oito linhas e evidência, sem Complexity Tracking nem veredito; ajustes do
gate de UX todos aplicados (B-UX1 § 5, B-UX2 J2.3, S-a..S-f, coluna "decisão que serve",
anatomia § 2.5); tasks com ids no padrão e as quatro caudas, mas sem DoD por tarefa e com dois
problemas de ordem; fixtures cobrem os oito agregados com roster do 073, projeto `maestro`, autor
"Ana Exemplo", efeitos só em memória; nenhuma contradição com as decisões fixas do briefing; T11
como tarefa condicional, nunca edição do 073 durante o julgamento; siglas ok salvo S6. Não rodou
scripts; conferiu `verifica-prototipo.py` e `exemplo.json` em disco.
