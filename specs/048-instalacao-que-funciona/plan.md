# Plan 048 — A instalação que funciona onde ela cai

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-11

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ `spec.md` antes deste plano; FR1–FR5 em EARS, os cinco cobertos por portão. |
| II. Human-governed orchestration | ✅ O relato veio de um agente e foi **verificado por mim** antes de virar trabalho; a promoção segue sendo gate humano. |
| III. Reversibility / risk gates | ⚠️ Parcial e declarado: o ciclo **apaga** `.specify/memory/constitution.md`. É reversível por git, mas é remoção — por isso o conteúdo foi lido antes, e o que ele tinha de próprio (nada além do resumo) está preservado em `principles.md`. |
| IV. Test-first / verifiable DoD | ✅ `check-installed.sh` foi escrito **antes** de qualquer correção e visto acusar as nove citações e os dois portões vermelhos. |
| V. Context economy / boundary | ✅ Nada muda de domínio: o portão é `toolkit`. O ciclo até **reduz** o que se carrega, tirando a segunda constituição. |
| VI. Living artifacts | ✅ É o ponto do ciclo: o portão falha quando a instalação e o que ela promete divergem, então a superfície instalável não pode envelhecer em silêncio. |
| VII. Light governance / YAGNI | ✅ Sem traduzir o livro, sem testar comportamento de IA, sem instalar o que o alvo não usa. Cada citação quebrada recebe a **menor** correção que a torna verdadeira. |
| VIII. Intelligible communication | ✅ Dois portões passam a **dizer** que não têm o que medir, em vez de sair vermelhos ou calados. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Não havia incógnita: o relato nomeava dois fatos, e o portão novo levantou os outros sete por execução. Investigação virou portão, que é o artefato que fica. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova. O ciclo conserta citações e move um arquivo de lugar. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface. O portão lê disco e roda scripts. |
| `checklist.md` | `ART:checklist=no` | A tabela das nove citações na `spec.md` **é** a lista, e cada linha é verificada pelo portão. Uma segunda cópia seria a perda que este ciclo combate. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. A superfície é a saída de terminal de quem instalou o método. |

## How

### O portão (`scripts/check-installed.sh`) — 14º

Instala num diretório temporário vazio, escreve o `CLAUDE.md` com `--block` (que é o que o
texto de próximos passos manda fazer), e então:

1. **Todo `check-*.sh` enviado roda lá, e sai verde.** Portão que chega vermelho ensina a
   ignorar vermelho.
2. **Toda citação de caminho é conferida**, com o invariante preciso: *um caminho que existe
   **aqui** e é citado por um arquivo que enviamos tem de existir **lá***. Caminho que não
   existe nos dois lados é referência do upstream a artefato do CLI do speckit — assunto do
   `.specify/UPSTREAM.md`, não do instalador. Sem essa distinção o portão culparia o
   instalador pela prosa do fornecedor.

### As nove citações, uma a uma

| Caminho | Correção | Por quê |
|---|---|---|
| `.specify/memory/constitution.md` | os 3 comandos passam a apontar para `docs/governance/principles.md`; o arquivo é **apagado** | duas constituições é o anti-padrão 22; a fonte de verdade já existe, em inglês e instalada |
| `docs/agents/README.md` · `perfis.md` | `check-roles.sh` diz explicitamente quando o índice não existe; `agent-designer` passa a citar o que é instalado | é conteúdo do **livro**, em português — instalá-lo quebraria o ADR 0014 |
| `.specify/scripts/bash/` | **enviado** | os comandos `/speckit.*` que enviamos o chamam, e o `THIRD-PARTY-NOTICES` já declarava redistribuí-lo |
| `.specify/init-options.json` | **enviado** | registra que o material vendorizado é do speckit 0.4.3 — é proveniência, e é verdade no destino |
| `scripts/check-retro.sh` | **enviado** | é parte do ritual (gatilho por dívida de achados) e o `docs/records/README.md` enviado já o cita |
| `scripts/check-chapters.sh` | `/dod` deixa de citá-lo | é do livro do Maestro; num projeto alheio não existe nem faz sentido |
| `scripts/install-maestro.sh` | a nota deixa de citar o caminho | no destino aquele caminho é do Maestro, não do projeto |

### Os dois portões que nascem vermelhos

- `check-roles.sh`: índice ausente → nota explícita, verde. Índice presente → checagem
  completa nos dois sentidos, como hoje.
- `check-conformance.sh`: **zero** diretórios `specs/NNN-*` → projeto novo, nota e verde.
  Se existirem specs mas nenhuma no alcance do piso, **continua vermelho** — foi assim que
  o ciclo 042 impediu que o piso virasse um botão de desligar com código de sucesso.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `scripts/check-installed.sh` | vermelho antes (9 citações + 2 portões), verde depois |
| mutações no clone descartável | uma por requisito, todas acusadas |
| `scripts/check-language.sh` | verde — nada em português entrou na superfície instalável |
| `scripts/check-licensing.sh` | verde, e agora **verdadeiro**: o que é declarado é enviado |
| `check-links` · `check-boundary` · `check-install` · `check-roles` · `check-conformance 048` | verdes |
| `scripts/package-plugin.sh --verify` · `node publicar/build.mjs` | verdes |
