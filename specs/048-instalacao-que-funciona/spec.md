# Spec 048 — A instalação que funciona onde ela cai

- **Status**: Em andamento · **Raia**: plena · **Data**: 2026-08-11
- **Origem**: relato de um agente companheiro que **instalou o Maestro noutro repositório** e
  bateu em duas paredes. Verifiquei as duas antes de aceitar, e o portão novo achou mais sete.

> **Raia**: plena. **Ambiguidade** média (o que fazer com cada citação quebrada é decisão, não
> mecânica); **raio** amplo (é a superfície que vai para repositórios de terceiros);
> **irreversibilidade** baixa.

## O quê e por quê

Duas lacunas relatadas, ambas confirmadas em 2026-08-11:

| Relato | Verificação |
|---|---|
| `install-maestro.sh` não copia `docs/agents/`, e `check-roles.sh` falha após instalação limpa | ✅ o instalador copia `docs/governance/*` e `docs/records/README.md`, nunca `docs/agents/`; `check-roles.sh:80` lê `docs/agents/README.md` |
| `/speckit.constitution` aponta para `.specify/memory/constitution.md`, que a instalação não cria | ✅ oito citações em três comandos vendorizados; o instalador não copia `.specify/memory/` |

As duas são **o mesmo defeito**: *enviamos uma coisa que aponta para outra que não enviamos.*
É o anti-padrão 22 — o método instalado como cópia com perda — e **nenhum portão podia
vê-lo**, porque todos os treze mediam o repositório de origem, onde o alvo por acaso existe.
Ninguém nunca **rodou a cópia instalada**.

Escrito o portão que instala num diretório vazio e exercita o resultado, ele achou **nove**
citações quebradas, não duas:

| Caminho citado por arquivo instalado | Quem cita |
|---|---|
| `.specify/memory/constitution.md` | 3 comandos `/speckit.*` (8 citações) |
| `docs/agents/README.md` · `docs/agents/perfis.md` | `check-roles.sh`, `agent-designer` |
| `.specify/scripts/bash/` | `THIRD-PARTY-NOTICES` — que **declara redistribuir** o que não envia |
| `.specify/init-options.json` | `/speckit.specify` |
| `scripts/check-retro.sh` | `docs/records/README.md` |
| `scripts/check-chapters.sh` | `/dod` |
| `scripts/install-maestro.sh` | `THIRD-PARTY-NOTICES` |

E um portão **nasce vermelho** em toda instalação nova: `check-conformance.sh` falha com
"nenhum ciclo no alcance" num projeto que ainda não tem ciclo. Portão que chega vermelho
ensina quem instalou o método a ignorar vermelho.

## Requisitos funcionais

- **FR1**: QUANDO o método for instalado num diretório vazio, O SISTEMA DEVERÁ rodar **todos**
  os portões que ele mesmo enviou, e todos DEVERÃO sair verdes.
- **FR2**: QUANDO um arquivo instalado citar um caminho do método que **existe na origem**, O
  SISTEMA DEVERÁ falhar se esse caminho não existir na instalação.
- **FR3**: QUANDO um portão não tiver o que verificar num projeto novo, O SISTEMA DEVERÁ
  dizê-lo **explicitamente** e sair verde — nunca em silêncio, e nunca vermelho.
- **FR4**: QUANDO o método tiver uma constituição, O SISTEMA DEVERÁ ter **uma só**, e os
  comandos vendorizados DEVERÃO apontar para ela.
- **FR5**: QUANDO as notas de terceiros declararem material redistribuído, O SISTEMA DEVERÁ
  de fato redistribuí-lo.

## Fora de escopo

- **Traduzir `docs/agents/` para inglês** para poder instalá-lo. É conteúdo do livro
  (português por decisão, ADR 0014) e publicado no site; traduzir para satisfazer um portão
  seria mover a fronteira para não consertar o defeito.
- **Testar se a IA obedece** ao método instalado. O portão mede coerência da instalação, não
  comportamento — isso é o que `evals/` faz, e a distinção é o anti-padrão 13.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- `scripts/check-installed.sh` instala num diretório temporário vazio, roda todo portão
  enviado e confere toda citação de caminho — e foi visto acusar as nove.
- As nove citações quebradas deixam de existir: cada uma **enviada** ou **deixada de citar**,
  com a razão escrita.
- A constituição passa a ser uma só: `docs/governance/principles.md`. A cópia com perda em
  `.specify/memory/constitution.md` deixa de existir, e a divergência frente ao upstream é
  **declarada** em `.specify/UPSTREAM.md` (regra 2: divergência declarada, nunca silenciosa).
- `check-roles.sh` e `check-conformance.sh` dizem explicitamente quando não têm o que medir.
- `THIRD-PARTY-NOTICES.md` volta a ser verdade: o que ele declara redistribuído é enviado.
- O portão entra na CI como bloqueante.

## Clarify

1. **Por que não simplesmente copiar `docs/agents/`?** Porque é português e é livro. A regra
   (ADR 0014) é que a superfície instalável é inglesa; copiar aquilo enviaria português para
   dentro do repositório de terceiro e quebraria `check-language`. O defeito não é a falta do
   arquivo: é um portão instalável exigindo um artefato do **livro**.
2. **Por que apagar `.specify/memory/constitution.md` em vez de instalá-lo?** Porque ele é,
   nas próprias palavras dele, "o resumo — texto completo em `principles.md`". Duas
   constituições é a definição do anti-padrão 22, dentro do repositório que o nomeou.
