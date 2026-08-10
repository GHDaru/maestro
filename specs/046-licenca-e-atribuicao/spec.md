# Spec 046 — Licença e atribuição do que é redistribuído

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-09
- **Origem**: painel de catorze especialistas convocado antes do ciclo do catálogo. O
  especialista em licenciamento achou algo que não era sobre o catálogo — era sobre nós — e
  eu verifiquei o achado antes de aceitá-lo.

> **Raia**: plena. **Ambiguidade** baixa (o defeito é factual e a correção é conhecida);
> **raio** amplo (o instalador copia isto para repositórios de terceiros);
> **irreversibilidade** baixa — arquivos de texto.

## O quê e por quê

Por 45 ciclos o Maestro **rejeitou uma coleção de terceiros por licença** (CC BY-NC-SA,
incompatível com a nossa distribuição) enquanto, ele próprio:

| Verificado em 2026-08-09 | Resultado |
|---|---|
| `LICENSE` no repositório | **nenhum** |
| `NOTICE` / `THIRD-PARTY-NOTICES` | **nenhum** |
| aviso de copyright nos arquivos vendorizados do `github/spec-kit` | **nenhum** |
| `plugin/maestro/.claude-plugin/plugin.json` | declara `"license": "MIT"` |

Repositório sem licença não é "neutro": é **todos os direitos reservados**, que é pior que a
licença recusada. E o MIT — permissivo — tem exatamente uma obrigação: o aviso de copyright
e o aviso de permissão acompanham cópias e porções substanciais. O `install-maestro.sh`
copia material vendorizado para repositórios de terceiros, e o plugin o redistribui; nenhum
dos dois levava aviso nenhum.

Rejeitar a licença alheia enquanto se ignora a própria é a forma de defeito que este
repositório não para de encontrar em si mesmo.

## Requisitos funcionais

- **FR1**: QUANDO o repositório for publicado, O SISTEMA DEVERÁ carregar o texto da licença
  MIT, e não apenas a alegação num manifesto.
- **FR2**: QUANDO material de terceiro for redistribuído, O SISTEMA DEVERÁ atribuí-lo com
  projeto, versão, licença e **linha de copyright do titular**, distinguindo verbatim de
  modificado.
- **FR3**: QUANDO o método for redistribuído — **pelos dois canais**: instalado noutro
  repositório e empacotado como plugin — O SISTEMA DEVERÁ levar junto a licença e a
  atribuição, **sem** afirmar que o projeto de destino é MIT.
  <!-- Escrito primeiro só para o instalador. A revisão independente mostrou que o plugin,
       que redistribui dez comandos derivados do spec-kit, saía sem texto de licença nenhum
       — o mesmo defeito que esta spec abre acusando, no canal que ela não olhou. -->

- **FR4**: QUANDO um manifesto declarar uma licença, O SISTEMA DEVERÁ falhar se o
  repositório não carregar essa licença.
- **FR5**: QUANDO um upstream for nomeado na proveniência, O SISTEMA DEVERÁ falhar se ele
  não estiver atribuído nas notas de terceiros.

## Fora de escopo

- Auditoria de licença das dependências de build (`markdown-it` e afins). São
  desenvolvimento, não são redistribuídas, e analisá-las é o teatro que o painel nomeou.
- SBOM (*Software Bill of Materials*). Num sistema agêntico o payload é a prosa — inventário
  de dependências não mede o risco que importa aqui.
- Aconselhamento jurídico. O portão mede a existência e a coerência dos artefatos que uma
  licença permissiva exige; **não** julga conformidade. Monetizar (livro, curso) ou aceitar
  contribuição de terceiro exige profissional de verdade.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- `LICENSE` com o texto MIT e titular declarado existe na raiz.
- `THIRD-PARTY-NOTICES.md` atribui `github/spec-kit` com versão, commit do fork, licença e
  linha de copyright, e separa o que é verbatim do que foi modificado.
- `install-maestro.sh` leva os dois para o destino **renomeados**, sob `docs/governance/`.
- `package-plugin.sh` empacota os dois no plugin, e `--verify` guarda isso ao reconstruir.
- `scripts/check-licensing.sh` cobre FR1 a FR5 e foi visto acusar em **cada** um, por
  mutação: um portão que passa no estado quebrado não cobre nada.
- `EARS`, `BMAD` e `SBOM` entram no glossário — as três apareceram em documentos nossos sem
  nunca terem sido registradas.

## Clarify

1. Por que renomear no destino? Porque um `LICENSE` solto na raiz de um repositório alheio
   afirma que **aquele projeto inteiro** é MIT do Maestro. Os arquivos descrevem apenas o
   material instalado, então vão para `docs/governance/MAESTRO-LICENSE` e
   `MAESTRO-THIRD-PARTY-NOTICES.md`.
