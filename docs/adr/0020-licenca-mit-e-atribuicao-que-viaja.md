# ADR 0020 — MIT, e a atribuição viaja com a cópia

- **Status**: Aceito · **Data**: 2026-08-10 · **Ciclo**: 046
- **Supersede**: nada. **Superado por**: —

## Contexto

Por 45 ciclos o Maestro recusou uma coleção de terceiros **por causa da licença**
(CC BY-NC-SA, incompatível com a nossa distribuição) enquanto ele próprio, verificado em
2026-08-09: não tinha `LICENSE`, não tinha nota de terceiros, não tinha linha de copyright
nos arquivos vendorizados do `github/spec-kit` — e o manifesto do plugin declarava
`"license": "MIT"`.

Três fatos tornam isso mais que uma formalidade:

1. **Repositório sem licença não é neutro.** O padrão legal é *todos os direitos
   reservados* — mais restritivo que a licença que recusamos. Publicar sem `LICENSE` é
   publicar proibindo.
2. **O material vendorizado é de terceiro.** `.specify/templates/` e `.claude/commands/`
   descendem do `github/spec-kit` (MIT, *Copyright GitHub, Inc.*). O MIT é permissivo e tem
   exatamente **uma** obrigação: o aviso de copyright e o aviso de permissão acompanham as
   cópias e as porções substanciais.
3. **Nós redistribuímos por dois canais.** O `install-maestro.sh` copia para repositórios
   alheios e o plugin empacota. Nenhum dos dois levava aviso nenhum.

## Decisão

**MIT**, `Copyright (c) 2026 GHDaru`, e a atribuição **viaja com a cópia**.

- `LICENSE` na raiz, com o texto íntegro.
- `THIRD-PARTY-NOTICES.md` atribuindo cada upstream com projeto, versão, commit do fork,
  licença e **linha de copyright do titular**, separando o que é **verbatim** do que foi
  **modificado**.
- **Os dois canais levam os avisos.** O instalador leva os dois **renomeados** para
  `docs/governance/MAESTRO-LICENSE` e `docs/governance/MAESTRO-THIRD-PARTY-NOTICES.md`; o
  `package-plugin.sh` os empacota com os nomes originais dentro de `plugin/maestro/`, e o
  `--verify` guarda isso ao reconstruir e comparar.
- `scripts/check-licensing.sh` mede a coerência: o `LICENSE` existe · o que o manifesto
  declara é o que o `LICENSE` diz · todo upstream nomeado em `.specify/UPSTREAM.md` está
  atribuído e **cada projeto atribuído nomeia o seu próprio titular** · o instalador e o
  pacote do plugin carregam os dois arquivos. **Entrada ausente é falha, nunca aprovação**:
  a primeira versão saía com exit 0 se o instalador fosse apagado.

### Por que MIT e não Apache-2.0

Apache-2.0 traz **concessão expressa de patente** e cláusula de retaliação — proteção real
que o MIT não dá. Foi considerada e recusada por duas razões: o upstream que
redistribuímos é MIT (mesma família, sem fricção de compatibilidade a explicar), e o
Apache-2.0 exige `NOTICE` e marcação de arquivos modificados, cerimônia que o Princípio VII
não paga para um método que é essencialmente prosa. **A ausência de concessão de patente é
consequência aceita, não esquecida.**

### Por que renomear no destino

Um `LICENSE` solto na raiz de um repositório alheio afirma que **aquele projeto inteiro** é
MIT do Maestro — o que é falso e é exatamente o tipo de comunicação que o Princípio VIII
proíbe. Renomeados e sob `docs/governance/`, os arquivos dizem a verdade: descrevem apenas
o material do Maestro instalado ali.

### O que a revisão independente corrigiu nesta decisão

A primeira versão deste ADR nomeava **dois** canais de redistribuição no Contexto e corrigia
**um** na Decisão: o plugin seguia empacotando dez comandos derivados do `github/spec-kit`
com um campo `"license": "MIT"` no manifesto e nenhum texto de licença — a mesma "alegação
sem texto" que o Contexto acusa. Um defeito que a própria decisão enxerga e não fecha é o
formato mais caro deles, porque fica documentado como resolvido. Corrigido antes do gate.

## Consequências

**Boas**

- O que era alegação num manifesto passa a ser fato verificável por portão.
- Quem instala o método recebe a obrigação junto, sem receber uma afirmação falsa sobre o
  próprio projeto.
- A incoerência "recusamos licença alheia sem ter a nossa" deixa de existir.

**Custos e limites, declarados**

- **Sem concessão de patente** (ver acima). Se o método vier a embarcar algo patenteável,
  isto se reavalia.
- O portão mede **existência e coerência** dos artefatos que uma licença permissiva exige.
  Ele **não** julga conformidade jurídica. Monetizar (livro, curso) ou aceitar contribuição
  de terceiro exige profissional de verdade.
- **Sem SBOM** (*Software Bill of Materials*) e sem auditoria das dependências de build:
  num sistema agêntico o payload é a prosa, e inventário de dependência não mede o risco
  que importa aqui. Fora de escopo declarado, não esquecido.

## Gatilho de reavaliação

- Primeira contribuição externa aceita · primeira monetização · primeiro upstream com
  licença de família diferente entrando no que redistribuímos.

## Fontes

- MIT License (SPDX `MIT`); Apache License 2.0 §3 (patent grant) e §4 (NOTICE).
- `github/spec-kit` — LICENSE (MIT, *Copyright GitHub, Inc.*).
- `.specify/UPSTREAM.md` (proveniência: verbatim × adaptado).
- Painel de catorze especialistas, ciclo 046 — parecer de licenciamento.
