# Scripts do Maestro

Scripts do **ritual repetido** — tiram o passo mecânico da atenção do Orquestrador (o
gargalo) sem tirar dele a **decisão**. Cada script nasceu de dor de retro, não especulação.

| Script | O que faz | Quando usar | O que NÃO decide |
|---|---|---|---|
| [`promover-main.sh`](./promover-main.sh) | `dev → main` + push com retry exponencial | Depois do **gate humano** de merge | **Se** promover — exige confirmação e aborta com árvore suja |
| [`novo-ciclo.sh`](./novo-ciclo.sh) | Cria `specs/NNN-slug/` com os 4 artefatos-esqueleto | Ao abrir um ciclo novo | O conteúdo — só o esqueleto; você preenche |
| [`verificar-agentes.sh`](./verificar-agentes.sh) | Roda os invariantes dos subagentes (contagem, frontmatter, read-only) | Antes de dar por pronto um ciclo de agentes | Nada — só reporta; exit ≠ 0 se quebra |
| [`retro.sh`](./retro.sh) | Pré-computa o material da retro (ciclos, vereditos, gates pendentes, decisões, inventário) | Na retro de fim de ciclo | As respostas — a retro continua humana |
| [`registrar-decisao.sh`](./registrar-decisao.sh) | Anexa decisão ao índice `docs/registro/decisoes.jsonl` (append-only, valida JSON) | Ao aceitar ADR / decidir gate | O mérito — só registra o que o humano decidiu |
| [`verificar-papeis.sh`](./verificar-papeis.sh) | Papel prescrito no modelo × agente existente; artefato essencial × template | Antes de fechar ciclo que mexe em papéis | Nada — só reporta; exit ≠ 0 se a norma não tem executável |
| [`verificar-instalacao.sh`](./verificar-instalacao.sh) | O método está instalado **de fato** aqui? camadas + instrução da IA + skills todas visíveis | Neste repo e em todo projeto que recebe o método | Nada — só reporta; exit ≠ 0 se a IA não foi instruída |
| [`instalar-maestro.sh`](./instalar-maestro.sh) | Instala o método completo em outro repositório; `--bloco` imprime a instrução para o `CLAUDE.md` | Ao levar o Maestro para um projeto | Não sobrescreve; `--dry-run` mostra antes |
| [`empacotar-plugin.sh`](./empacotar-plugin.sh) | Gera `plugin/maestro/` (Claude Code) das fontes; `--verificar` prova a sincronia | Ao mudar agente/skill/comando | Nada — reempacota ou acusa divergência |

## Princípio (II + III)

O script executa o **mecânico**; o **gate continua humano**. `promover-main.sh` **não**
promove sozinho: mostra os commits, pede confirmação (ou `--yes` explícito) e aborta se a
árvore estiver suja ou `dev` não estiver à frente de `main`. Automatizar a *execução* do
ritual é economia de contexto; automatizar a *decisão* seria violar o Princípio II.

## Uso rápido

```bash
scripts/novo-ciclo.sh 007 vendorizar-spec-kit   # abre o próximo ciclo
scripts/verificar-agentes.sh                    # fitness function dos agentes
scripts/verificar-instalacao.sh                 # o método está instalado de fato?
scripts/promover-main.sh                        # promove após o "sim" (pergunta antes)
```
