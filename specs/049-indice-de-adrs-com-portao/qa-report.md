# QA report 049 — O índice de decisões com portão

- **Date**: 2026-08-11 · **Lane**: plena · **Verdict**: aprovado após reprovação e correção

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `scripts/check-adr.sh` | verde no repositório íntegro | ✅ 17 ADRs |
| `check-agents` · `check-roles` · `check-install` · `check-language` · `check-links` · `check-evals` · `check-boundary` · `check-chapters` · `check-licensing` · `check-ecosystem` · `check-installed` · `check-cycle` · `check-retro` | verdes | ✅ |
| `scripts/package-plugin.sh --verify` · `node publicar/build.mjs` | verdes | ✅ |
| `scripts/check-conformance.sh 049` | verde | ✅ |

### O portão foi visto acusar — doze mutações, em clone descartável

| Mutação | Portão |
|---|---|
| **o defeito real do ciclo 046**: índice sem 0018/0019 e 0017 como "Aceito" | ✗ nomeando 0017 e os dois ausentes |
| segunda linha contraditória para o mesmo ADR | ✗ `has 2 rows — one of them is wrong` |
| linha comentada em HTML (some da tabela renderizada) | ✗ `has no row in the index` |
| menção só em prosa, com link | ✗ idem |
| índice `Rejeitado` × ADR `Aceito` | ✗ nomeando os dois estados |
| ADR `Substituído` × índice `Aceito` | ✗ idem |
| ADR `Proposto` × índice `Aceito` | ✗ idem |
| linha fantasma sem link | ✗ `announced and unreachable` |
| ADR mal nomeado (`21-invisivel.md`) | ✗ `would be invisible to this gate` |
| ADR sem linha de `Status` | ✗ |
| índice apagado | ✗ **com receita**: `cp .specify/templates/adr-index-template.md …` |
| `docs/adr/` apagado, estando declarado no `boundary.json` | ✗ |
| **controle** — inclui o 0017 com link markdown no status e um título contendo "superada" | ✓ exit 0 |

Instalação limpa exercitada ponta a ponta: sem `docs/adr/` → nota explícita e verde; com o
primeiro ADR escrito do template e o índice ainda por preencher → vermelho apontando o
placeholder; preenchidos → verde.

## Closing tail — the evidence

- TAIL:review — revisão independente em contexto fresco, por quem não executou. Veredito:
  **NÃO PROMOVER COMO ESTÁ**, três bloqueantes — e os três eram o mesmo tipo de erro:
  **o portão media a frase, não o fato**. (1) `grep -m1` parava na primeira linha, então uma
  **segunda linha contraditória** para o mesmo ADR passava — a variante mais direta do
  defeito de 046. (2) "está listado" era "aparece em qualquer lugar do arquivo": uma linha
  **comentada em HTML** ou uma menção em prosa satisfaziam, embora o ADR sumisse da tabela
  renderizada, que é o que o leitor vê. (3) O invariante de status só existia no eixo
  "superado", e por uma palavra mágica não documentada: `Substituído`, `Revogado`, `Obsoleto`
  desligavam o invariante inteiro, e `Rejeitado` no índice contra `Aceito` no ADR passava —
  enquanto a linha verde afirmava "every status agreeing". Mais dois relevantes (o primeiro
  ADR de um projeto instalado ficava vermelho **sem receita**; linha fantasma sem link) e
  três menores. **Todos corrigidos**: o casamento passa a ser por **linha de tabela** com o
  número no primeiro campo, unicidade exigida; o status passa por um **vocabulário fechado**
  (accepted · proposed · rejected · superseded) que mapeia sinônimos nas duas línguas; e o
  índice ganhou template instalável, citado na mensagem de falha.
- TAIL:security — passe proporcional à classe de risco (um portão de leitura e um template
  de texto). **(a) Execução**: nenhuma; o portão lê arquivos e não roda nada. **(b) Injeção
  de padrão**: o número do ADR e o nome do arquivo vêm do disco e são usados em `grep` — o
  casamento do link usa `-E` com o nome interpolado, e o nome vem do glob `[0-9][0-9][0-9][0-9]-*.md`,
  não de entrada livre. **(c) Superfície instalável**: cresceu com o portão e o
  `adr-index-template.md`, ambos em inglês e cobertos por `check-language`. **(d) Conteúdo
  injetável**: o template é um formulário com comentários, sem diretiva executável.
- TAIL:gate — DoD verde, catorze portões + plugin + build verdes, `check-conformance.sh 049`
  verde. **Aguarda o gate humano** de promoção `dev` → `main`, que não é delegável.

## Requirement coverage

- **FR1** — todo ADR no disco tem **exatamente uma** linha de tabela, com o número no
  primeiro campo e link ao próprio arquivo. Comentário, tachado e prosa não contam.
- **FR2** — toda linha do índice aponta para arquivo existente; linha sem link nenhum falha.
- **FR3** — o status é comparado por **estado**, não por palavra: quatro estados, sinônimos
  mapeados nas duas línguas, e um menu de template por preencher é falha própria e nomeada.
- **FR4** — ADR sem linha de status falha, porque não há com o que o índice concordar.

## Achados registrados neste ciclo

- **Eu escrevi um portão que media a frase e não o fato** — o anti-padrão 13, que este
  repositório nomeia e ensina, na terceira versão seguida em que só a revisão independente o
  viu.
- **Duas heurísticas minhas quebraram casos legítimos** e só apareceram ao rodar a bateria:
  colchetes de um link markdown no status do 0017 (lidos como placeholder) e um título
  contendo "superada" (lido como estado). As duas viraram controle positivo.
- **Reversão de escopo declarada**: a spec dizia que o portão não viajaria; ao rodar o
  `check-installed.sh` ficou claro que isso contradizia a lição do ciclo 048. Passou a viajar,
  com o padrão de ausência legítima e template de índice.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
