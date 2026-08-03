# ADR 0013 — Instrução para a IA: fonte única e gerada do disco

- **Status**: Aceito · **Data**: 2026-08-02
- **Ciclo**: 021 · **Decisor**: Steward

## Contexto

O Maestro se instala em outros projetos desde o ciclo 018, mas nunca havia sido instalado
**no próprio Maestro** — e a auto-instalação, feita agora, achou o que se esperaria achar
em qualquer projeto que recebeu o método e seguiu a vida:

1. `CLAUDE.md` e `AGENTS.md` eram cópias quase iguais, escritas à mão. O `AGENTS.md`
   ficou sem a regra "skills primeiro" (adicionada ao `CLAUDE.md` no ciclo 011): quem lê
   `AGENTS.md` — a maioria dos assistentes que não é Claude Code — trabalhava sem ela.
2. A lista de skills no `CLAUDE.md` estava em cinco de seis: a `living-journey`, criada no
   ciclo 018, existia no disco e era **invisível** para a IA havia três ciclos.
3. O `Constitution Check` da skill e de dois agentes dizia "I–VII"; a constituição tem
   VIII desde o ciclo 013 (ADR 0010). Oito ciclos de planos sem onde marcar o princípio.

Os três são a mesma falha: **lista escrita à mão que não é comparada com o disco**.
Nenhuma delas quebrava nada visivelmente — apenas a IA seguia menos método do que o
repositório declarava ter.

## Decisão

1. **Fonte única**: `AGENTS.md` passa a ser link simbólico para `CLAUDE.md`. Duas cópias
   escritas à mão divergem — a pergunta não é *se*, é *quando*.
2. **Instrução gerada**: `scripts/install-maestro.sh --block` monta o bloco de instrução
   **lendo `skills/`**, com nome e primeira frase de cada `SKILL.md`. Quem instala cola o
   que o disco tem, não o que a documentação lembrava de ter.
3. **Fitness function de instalação**: `scripts/check-install.sh` verifica as duas
   metades — camadas presentes **e** IA instruída — e falha se uma skill do disco não
   aparecer na instrução. Roda neste repositório e em todo projeto que recebe o método.
4. **Contagem de princípios**: `scripts/check-roles.sh` passa a comparar quantos
   princípios a constituição tem com quantas linhas o template de plano checa.

## Alternativas consideradas

- **Manter duas cópias e revisar na retro**: é o que estava valendo. Falhou três vezes
  seguidas — norma sem forcing function depende de memória, e a memória é o que falha
  primeiro (lição do ciclo 017).
- **`AGENTS.md` como ponteiro de uma linha ("veja CLAUDE.md")**: some com a duplicação,
  mas custa um salto de leitura a todo agente e falha se a ferramenta lê o arquivo sem
  seguir referência. O link simbólico entrega o conteúdo inteiro sem cópia.
- **Gerar o `CLAUDE.md` inteiro por script**: tira do humano a parte que é dele — o que
  este projeto tem de particular. Só o **bloco do método** é gerado; o resto é escrito.
- **Não fazer nada**: o método continuaria se instalando em outros repositórios com o
  mesmo defeito que tinha no seu — e a primeira IA a reclamar de "Maestro não instalado"
  já tinha reclamado (ciclo 018).

## Consequências

- (+) Skill nova sem entrada na instrução **falha o check** — a invisibilidade acabou.
- (+) Quem instala em outro projeto recebe a lista correta sem copiar à mão.
- (+) A auto-instalação vira teste permanente: o Maestro é o primeiro usuário do Maestro.
- (−) Link simbólico não é conteúdo no GitHub: quem abre `AGENTS.md` no navegador vê um
   ponteiro, não o texto. Aceito — quem lê `AGENTS.md` é máquina, e máquina segue o link.
- (−) O bloco gerado depende do campo `description` das skills ser boa primeira frase.
   Descrição ruim vira instrução ruim — custo assumido, com o ganho de ser sempre atual.

## Registro

- `scripts/check-install.sh` (novo) · `scripts/install-maestro.sh` (`--bloco`)
- `scripts/check-roles.sh` (princípios × Constitution Check)
- `CLAUDE.md` reescrito · `AGENTS.md` → link simbólico
- `skills/constitution-check/`, `.claude/agents/{plan-arquiteto,guardiao-processo}.md`: I–VIII
- `docs/receitas/instalar-o-maestro.md` · spec do ciclo `specs/021-maestro-instalado-no-maestro/`
