# ADR 0018 — Fronteira interna em vez de divisão em dois repositórios

- **Status**: Aceito · **Data**: 2026-08-06
- **Ciclo**: 039 · **Decisor**: Steward
- **Supersede**: [ADR 0017](0017-divisao-em-dois-repositorios.md) — a decisão de dividir em
  dois repositórios foi revertida antes de qualquer arquivo se mover.

## Contexto

O ADR 0017 aceitou dividir o repositório em **toolkit** (lido por máquinas) e **guia**
(lido por pessoas), derivando o corte do corolário C10, e entregou a fatia 1: a fronteira
declarada em `boundary.json` e verificada por `check-boundary.sh`. Nenhum arquivo se moveu
— por desenho, porque divisão de repositório é irreversibilidade alta.

Antes do gate da fatia 2, o Steward pediu a comparação com prós e contras. **A medição
mudou a decisão**, e é por isso que ela foi feita antes de mover:

| Medida | Valor |
|---|---|
| Commits que tocam **substância** nos dois lados | **18 de 86 (20%)** |
| Commits só do toolkit / só do guia | 10 (11%) / 22 (25%) |
| Peso rastreado: toolkit × guia | 846 KB × 5,6 MB |
| Arquivos que o instalador copia do lado do guia | **0** |
| Versões fechadas / tags git no histórico | **0 / 0** |

O primeiro número foi corrigido durante a própria medição: o bruto dava 40%, mas
`CHANGELOG.md`, `docs/roadmap.md`, `docs/records/` e `specs/` são tocados por **toda**
entrega por forcing function, não por acoplamento. Descontados, o acoplamento substantivo
é 20% — e ainda assim são os commits que mais importam (axiomas + BPMN, retro que virou
portão, inglês no instalável).

Três supostos ganhos da separação não sobreviveram à medição:

- *"o instalável fica menor"* — já está. `install-maestro.sh` copia **caminhos**, não
  repositórios, e nunca copiou nada do livro. A separação não mudaria um byte do que é
  instalado.
- *"cada um libera no seu ritmo"* — nunca liberamos: zero tags, zero versões fechadas.
- *"times separados trabalham em paralelo"* — há um contribuidor.

Sobraram três ganhos reais — contexto do agente, peso de clone (7×) e dependências isoladas
— nenhum urgente. Contra eles, quatro perdas mensuráveis: atomicidade dos 20% acoplados,
252 links relativos verificados caindo para 35 externos não verificados, a evidência de
código do livro ficando sem portão possível, e um mecanismo de espelho novo com defasagem
própria — justamente o modo de falha que T7/C11 acabara de descrever.

## Decisão

1. **Um repositório.** A divisão em dois é rejeitada agora, com gatilho para reavaliar.
2. **A fronteira continua**, como fronteira **interna**: `boundary.json` deixa de descrever
   dois repositórios e passa a declarar dois **domínios** (`domains`), com os caminhos
   `shared` marcando o que o toolkit possui e o site publica.
3. **As três invariantes continuam**, e a terceira **muda de razão, não de valor**: já não
   protege contra perder páginas no dia da mudança; protege contra o site publicar um
   documento voltado a máquina que ninguém declarou público.
4. **Gatilhos para reabrir** (observáveis, não datas): o guia ganhar ciclo de vida próprio
   (uma versão que não corresponde a uma versão do método); aparecer quem contribua só com
   o livro; ou alguém instalar o método e reclamar do peso ou do ruído.

## Alternativas consideradas

- **Executar a fatia 2 como planejado.** Rejeitada pela medição acima.
- **Deixar o ADR 0017 de pé e só não executar.** Rejeitada por A4: artefato que afirma uma
  decisão revertida vira a verdade que a próxima sessão lê. O achado só morre quando o
  registro muda.
- **Apagar `boundary.json` junto com a decisão.** Rejeitada: o arquivo resolve um problema
  que existe com um repositório só — todo arquivo passou a ter dono declarado e verificado,
  e antes disso não tinha.

## Consequências

**Boas.** Nada se move, então nenhuma das quatro perdas acontece. A fronteira fica
explícita e verificada, que era o ganho principal da fatia 1 — e ele **não dependia** da
fatia 2. Reabrir a discussão depois custa pouco: o critério já existe e está verde.

**Ruins, e assumidas.**

- **Os três ganhos reais ficam na mesa.** O agente que mexe no livro continua carregando
  instrução de um repositório com 368 arquivos; quem instala continua clonando 6,5 MB para
  usar 846 KB. Não é grátis — é adiado, com gatilho escrito.
- **`check-language.sh` continua existindo como fronteira interna de idioma**, que é uma
  cerimônia que a separação teria eliminado.
- **Dois ADRs sobre o mesmo assunto em três dias.** O 0017 registra um corte que não vai
  acontecer. Fica assim de propósito: ADR é imutável, e o par 0017 → 0018 mostra que a
  medição mudou a decisão — que é o comportamento que se quer, não um erro a esconder.

## Referências

- ADR 0017 (superado) · `boundary.json` · `scripts/check-boundary.sh`
- Corolário C10 em `docs/governance/axioms.md`
- Gatilhos de reabertura: `docs/roadmap.md` § Gatilhos abertos
