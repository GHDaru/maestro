# QA report 050 — Fechar a v0.2.0

- **Date**: 2026-08-11 · **Lane**: plena · **Verdict**: aprovado após reprovação e correção

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `scripts/check-version.sh` | verde em 0.1.0, vermelho no meio do corte, verde em 0.2.0 | ✅ os três estados observados |
| os outros quinze portões | verdes | ✅ |
| `scripts/package-plugin.sh --verify` · `node publicar/build.mjs` | verdes | ✅ 33 arquivos · 38 páginas |
| `scripts/check-conformance.sh 050` | verde | ✅ |
| `git tag -l` | `v0.2.0` local, no commit da versão | ✅ (ver TAIL:gate) |

### O portão foi visto acusar — e visto **deixar de acusar** onde não devia

| Mutação | Portão |
|---|---|
| README/roadmap/plugin ficando para trás (3 mutações) | ✗ cada uma |
| lugar que deixa de declarar versão | ✗ |
| CHANGELOG só com `[Unreleased]` | ✗ |
| **o estado intermediário real deste ciclo** | ✗ |
| README revertido **com menção histórica à 0.2.0 antes** | ✗ (antes: falso **verde**) |
| roadmap revertido com comentário citando 0.2.0 acima | ✗ (antes: falso verde) |
| `## [0.10.0]` inserida **abaixo** da 0.2.0 | ✗ `headings are out of order` |
| `## [0.3.0]` escrita sob `[Unreleased]` | ✗ — o cabeçalho de versão é tratado como declaração de release, então o portão força escolher: ou tira o cabeçalho, ou corta a versão de verdade |
| número extra na linha do cabeçalho (`fork do spec-kit 0.4.3`) | ✓ **verde** — antes era falso vermelho |
| controle | ✓ exit 0 |

## Closing tail — the evidence

- TAIL:review — revisão independente em contexto fresco, por quem não executou. Veredito:
  **NÃO PROMOVER COMO ESTÁ**, quatro bloqueantes. **Dois eram falsidades na nota de release**,
  que é o documento que este ciclo existe para produzir e que gente de fora lê: (a) a nota
  afirmava que *"a raia leve e a variante acadêmica não foram feitas"* — a **raia leve
  existe, cobriu 12 dos 48 ciclos** e vem do ADR 0005, e *"variante acadêmica"* não aparece
  em lugar nenhum do repositório exceto naquela linha; (b) *"os portões novos têm piso de
  ciclo"* — só o `check-conformance` tem piso, e ele é do ciclo 042. O terceiro bloqueante
  era um **falso verde provado** no portão novo, exatamente na falha que o cabeçalho dele diz
  existir para impedir: ele lia a primeira string com cara de versão do arquivo, então uma
  menção histórica desarmava a checagem enquanto a capa ainda dizia v0.1.0. O quarto deixava
  a conformidade vermelha (um `[` numa justificativa do `plan.md` era lido como placeholder),
  o que **barraria o `promote-main.sh`**. Mais cinco relevantes e quatro menores — entre eles
  que eu contei "cinco ideias" quando são **seis**, e que o roadmap ficou com "quinze portões"
  quando eu já tinha corrigido a capa e o CHANGELOG para dezesseis. **Todos corrigidos.**
- TAIL:security — passe proporcional à classe de risco (prosa e um portão de leitura).
  **(a) Execução**: nenhuma; o portão lê arquivos. **(b) Interpolação**: os regexes das
  linhas declarantes são literais escritos no script, não vêm de arquivo; o único dado
  interpolado é o número de versão, comparado por igualdade de string. **(c) Superfície
  instalável**: **não cresceu** — o portão não viaja, e a razão está na spec. **(d) O que
  esta versão publica**: uma nota de release que declara o que a versão não tem, inclusive a
  tag anterior que nunca chegou ao GitHub. Nada de credencial, host interno ou segredo entra
  na nota.
- TAIL:gate — DoD verde, dezesseis portões + plugin + build verdes, `check-conformance 050`
  verde. A tag local `v0.2.0` foi criada no commit da versão. **Aguarda o gate humano** de
  promoção `dev` → `main`, e **a publicação da tag**, que este ambiente não faz: o push de
  tag recebe 403 do proxy de saída (o de branch passa), e a orientação é reportar o host
  barrado em vez de contornar.

## Requirement coverage

- **FR1** — a nota tem as três partes, e a do meio lista sete limites verificáveis, cada um
  conferido contra o repositório depois da revisão.
- **FR2** — as quatro declarações comparadas a partir da **linha que declara**, mais a ordem
  dos cabeçalhos do CHANGELOG, porque "mais nova" ali é posicional.
- **FR3** — lugar que não tem linha de declaração falha.
- **FR4** — a tag não publicada está na lista do que a versão não tem, com a razão técnica.

## Achados registrados neste ciclo

- **Escrevi duas afirmações falsas numa nota de release.** Uma delas — "a raia leve não foi
  feita" — é contradita por um portão do próprio repositório, que imprime `leve: 12`. A outra
  citava uma coisa que não existe em lugar nenhum. Nenhum portão cobre a veracidade de prosa,
  e é por isso que a revisão em contexto fresco é a forma, não a cerimônia.
- **Corrigi um ramo e deixei o irmão**: ao acertar a contagem de portões, atualizei a capa e o
  CHANGELOG e esqueci o roadmap — anti-padrão 16, dentro do ciclo cujo entregável é um portão
  contra afirmar a mesma coisa de dois jeitos.
- **O portão nasceu com o defeito que ele diz impedir.** Lia o arquivo, não a declaração.

## Nota sobre o status no roadmap

F25 fica ✅ pela mesma convenção das linhas F21–F24: a fase é marcada quando o trabalho está
completo e verificado, restando o gate humano — que é o passo seguinte, não parte da entrega.
A revisão sugeriu 🔄; mantive ✅ para não criar uma inconsistência com as quatro linhas
anteriores, e registro a divergência aqui em vez de resolvê-la em silêncio.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
- **Publicação da tag `v0.2.0`** aguarda rede liberada ou ação do Steward.
