# QA report 064 — Capa para a IA que instala

- **Data**: 2026-08-26 · **Raia**: leve · **Veredito**: DoD verde; falta a revisão
  independente e o portão humano.

## Fitness functions (DoD)

| Verificação | Esperado | Resultado |
|---|---|---|
| 14 portões bloqueantes | todos código 0 | verde — `check-agents`, `check-roles`, `check-install`, `check-language`, `check-links`, `check-evals`, `check-boundary`, `check-chapters`, `check-licensing`, `check-ecosystem`, `check-installed`, `check-adr`, `check-version`, `check-flags` |
| `check-installed.sh` — ids | as duas páginas comparadas contra `install-agents.tsv` | `✓ instalar-o-maestro.md: every --ai id … (4)` e `✓ README.md: every --ai id … (4)` |
| `check-installed.sh` — contagens | toda contagem do README conferida contra instalação real | 13 subagentes · 6 skills · 13 scripts · 9 portões · 12 comandos · 12 templates — todas conferidas |
| `check-flags.sh` | flag prometida × flag que o parser aceita, nas duas direções | verde com `--ai`, `--yes`, `--dry-run`, `--no-hooks`, `--force` publicadas |
| `check-conformance.sh --ticked-only` | caixa marcada tem evidência | verde |
| `package-plugin.sh --verify` | plugin em sincronia | verde depois de reempacotar (33 arquivos) |

## Cauda de fechamento — a evidência

- **TAIL:review** — pendente. Por T2, quem executou não verifica: falta o parecer em contexto
  fresco, por quem não escreveu esta página.

- **TAIL:security** — classe de risco **baixa**. O ciclo altera uma página publicada e o
  escopo de leitura de um portão; não introduz credencial, entrada de rede nem execução de
  código de terceiro. Um ponto foi examinado e descartado: o comando publicado no README
  clona para `/tmp/maestro`, e diretório previsível em `/tmp` é vetor de troca por symlink —
  mas quem escreve ali é o `git clone`, que **recusa** um destino existente, e o alvo da
  instalação é o projeto do leitor, não o clone. O instalador já recusa symlink de diretório
  no alvo desde o ciclo 052. Nada a fazer.

- **TAIL:mutation** — o ciclo alterou **um** portão: o bloco de ids do
  `scripts/check-installed.sh`, que passou a ler o README além da receita. Três mutações, cada
  uma vista reprovando com código 1, e a contraprova rodada **antes e depois** das três:

  | Mutação | Comando | O que o portão imprimiu |
  |---|---|---|
  | id fantasma | `sed -i 's/\| \`cursor-agent\` \| Cursor/\| \`cursor\` \| Cursor/' README.md` | `✗ README.md tells you to use --ai cursor, and the installer refuses it` + `✗ the installer accepts --ai cursor-agent, and README.md never lists it` |
  | tabela ausente | remoção do bloco `\| \`--ai\` \|` inteiro | `✗ README.md publishes no --ai table — the page that tells you to choose an agent lists none` |
  | id esquecido | `sed -i '/^\| \`codex\` \|/d' README.md` | `✗ the installer accepts --ai codex, and README.md never lists it` |

  Contraprova, com o README intacto, antes e depois:
  `✓ README.md: every --ai id is one the installer accepts, and vice versa (4)` e
  `✓ a fresh installation runs every gate it ships and names no path it does not create.`

  A mutação da tabela ausente é a que importa: ela prova que o portão distingue "a página está
  certa" de "não olhei" — anti-padrão 16, que é a forma como a versão anterior deste bloco
  teria certificado um README sem tabela nenhuma.

  Verificado também que a extração escopada não vaza: nas duas páginas ela devolve
  exatamente 4 ids, e nenhuma das outras tabelas do README (flags, camadas, estrutura,
  caminhos menores) aparece como id fantasma.

- **TAIL:gate** — pendente, do Steward.

## Cobertura dos requisitos

- **FR1** — o README abre a seção com `init . --ai claude --yes`, e diz o que acontece sem a
  flag: código 2, zero arquivos, `no terminal to ask about which agent`. Medido antes de
  escrever, em 2026-08-26.
- **FR2** — tabela publicada e comparada nas duas direções contra `install-agents.tsv`.
- **FR3** — tabela ausente reprova; mutação 2 acima.
- **FR4** — a seção "Se você é uma IA" abre com a bifurcação instalar × trabalhar no método,
  e a âncora `#instalar-o-maestro-no-seu-projeto` resolve (`check-links.sh` verde).
- **FR5** — a verificação publicada é `scripts/check-install.sh`, precedida de `cd` para o
  projeto alvo, com a razão escrita: rodar de dentro do clone devolve verde sobre o
  repositório do método.

## Achados abertos por este ciclo

- Nenhum novo. Um erro de processo, sem achado porque não é do repositório: usei
  `git checkout README.md` para desfazer a primeira mutação, com a reescrita ainda **não
  estagiada** — e `git checkout <path>` restaura do índice, então apagou o trabalho.
  Refeito a partir do rascunho e, daí em diante, mutação com cópia de arquivo.

## Portão pendente

- A promoção `dev` → `main` aguarda aprovação humana.
