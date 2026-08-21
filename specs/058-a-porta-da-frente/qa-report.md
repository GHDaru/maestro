# QA report 058 — A porta da frente

- **Date**: 2026-08-17 · **Lane**: infra · **Verdict**: aprovado após correção do parecer

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `maestro` sem argumento | lista os subcomandos, sai 0 | ✅ |
| `maestro init ./rel` de **outro diretório** | instala **onde o usuário está** | ✅ (antes: instalava dentro do repo do Maestro dizendo "✓ installed") |
| `maestro check <dir>` | mede e **nomeia** o alvo | ✅ (antes: media o repo do Maestro e dava verde alheio) |
| `maestro init` sem alvo, dentro do Maestro | recusa | ✅ |
| sem TTY e sem `--yes` | **recusa**, nada criado | ✅ exit 2 |
| `--ai` como último argumento | erro nomeado | ✅ (antes: morria sem imprimir nada) |
| `--ai` inválido | recusa **antes** de criar diretório | ✅ |
| dois alvos | recusa | ✅ (antes: instalava no segundo, calado) |
| `--dry-run` | escreve **zero** arquivos, sem veredito | ✅ |
| `maestro version` | uma linha | ✅ (antes: `0.2.0` + `?` quando o CHANGELOG crescesse) |
| `init --ai codex --no-hooks --yes` | instala sem a camada | ✅ |
| capa do site → receita | **um** clique | ✅ |
| bateria de 17 portões · plugin · build | verdes | ✅ |

## Closing tail — the evidence

- **TAIL:review** — revisão independente em contexto fresco. **Reprovou: 19 achados.** O pior
  não é um detalhe:

  1. **`maestro init ./meu-projeto` instalava dentro do repositório do Maestro** e imprimia
     "✓ installed and coherent". Um `cd "$HERE"` no topo fazia todo caminho relativo — a forma
     mais comum — resolver contra o repo, não contra quem digitou. **A própria capa do site
     que este ciclo escreveu anuncia essa forma.** Sucesso relatado, num diretório que ninguém
     nomeou.
  2. **`maestro check` dava verde alheio**: de qualquer projeto não instalado ele media o
     repositório do Maestro e dizia que estava tudo certo, sem nunca dizer o que mediu.
  3. **`init` sem alvo instalava o método dentro do método.**
  4. **Sem terminal e sem `--yes`, ele inventava consentimento** — instalava para `claude`
     quando nenhum agente foi declarado, e criava diretórios que ninguém aprovou. Pior: o
     próprio texto de uso dizia que `--yes` era "obrigatório sem terminal". Uma mentira nova,
     cunhada por este ciclo, no arquivo que o portão novo guarda.
  5. **O portão era cego para o próprio arquivo.** O extrator lia **prosa com parênteses**
     como se fosse `case`, então qualquer flag inventada documentada numa linha com `(...)`
     se auto-anulava — e uma flag `--nuke` documentada e inexistente passava verde.
  6. **O portão concatenava as fontes**: esvaziar o `# Usage` (que é a mentira nº 3, exatamente
     como ela era) continuava verde porque a receita ainda tinha as flags.
  7. **`version()` era anti-padrão 21 — quinta aparição** — e o banner passaria a imprimir a
     versão **e um `?`** assim que o CHANGELOG crescesse além do buffer do cano. O CHANGELOG
     deste repositório cresce **toda PR**, por função de força.
  8. **`--dry-run` escrevia e depois declarava a instalação quebrada.**
  9. **`--ai` inválido criava o diretório antes de recusar** — e a asserção que eu escrevi
     para guardar isso **pré-criava o diretório**, ficando incapaz de falhar.
  10. **Uma quarta cópia da mentira**: o `README.md`, a primeira página, repetia `--forcar` e
      o "não sobrescreve". O portão não olhava para ele.

  Mais: `--ai` como último argumento matava o script sem imprimir nada; dois alvos eram
  engolidos (o script que ele embrulha recusa — embrulhar removeu a recusa); `--help` era
  aceito e documentado em lugar nenhum; flags curtas não eram medidas; os temporários do
  portão tinham nome previsível em diretório mundialmente gravável, sem `trap`; e o `version`
  era a terceira cópia à mão do mesmo *pipeline* de CHANGELOG.

  **E ao provar a correção, achei outro meu**: `exit` dentro de `$( )` sai do **subshell**, não
  do script — a recusa por falta de terminal virava resposta vazia, com a mensagem errada e o
  código de saída errado. Trocado por variável global.

  **Não refutado**: o HTML da capa (tokens definidos nos três temas, link gerado e coberto pelo
  portão de links do build), a exclusão correta do `-*)`, `comm` sobre entradas ordenadas,
  `bin/` carregando peso em `boundary.json` e `check-language.sh`, e a proveniência das três
  mentiras — todas reais, conferidas em `git show HEAD`.

- **TAIL:security** — classe de risco alta: um comando novo que **cria diretórios e escreve em
  caminho fornecido pelo usuário**. Mitigações, todas do parecer: (a) o alvo é resolvido contra
  o diretório de quem chamou, e não mais contra o repositório — era o vetor real, e escrevia
  onde ninguém pediu; (b) o agente é validado **antes** de qualquer `mkdir`; (c) alvo que
  existe e não é diretório recusa; (d) instalar dentro do próprio Maestro recusa; (e) o portão
  passou a usar `mktemp -d` com `trap`, em vez de nome previsível em `/tmp` criado com `>`,
  que segue symlink plantado. **Limite declarado**: `init` não valida o conteúdo do caminho
  além disso — quem o executa escolhe onde escrever, como em qualquer instalador.

- **TAIL:mutation** — o ciclo cria `check-flags.sh` e mexe em `check-installed.sh`. Sete
  mutações, todas **vistas reprovando**: flag no parser fora do `# Usage` · flag inventada no
  `# Usage` · `--forcar` de volta na receita · `--forcar` no README · `# Usage` esvaziado ·
  flag do `maestro` fora do `usage()` · flag curta `-q` sem documentação. E uma oitava, que
  achou defeito: com a documentação **vazia**, o portão saía 1 **sem imprimir nada** — um
  `grep` sem correspondência derrubando a atribuição sob `set -e`. Portão que morre em vez de
  relatar é indistinguível de portão que não achou nada.

- **TAIL:gate** — DoD verde, 17 portões verdes, plugin em dia, livro em 39 páginas.
  **Aguarda o gate humano.**

## Requirement coverage

- **FR1/FR2** — `maestro` com oito subcomandos; `init` em quatro passos, com a tabela do 057.
- **FR3** — roda sem humano, e **recusa** em vez de responder por ele quando falta declaração.
- **FR4** — todo subcomando despacha. `version` era a exceção e virou a única leitura correta
  do CHANGELOG dos três lugares que a fazem.
- **FR5** — termina verificando, e sai diferente de zero quando falha.
- **FR6** — dois sentidos na referência, um na prosa, com o motivo escrito na spec.
- **FR7** — "Instalar agora" na capa, um clique até a receita.

## Limites declarados, não corrigidos

- **A mentira nº 2 não é coberta por portão.** "Não sobrescreve" é **prosa sobre
  comportamento**, não uma flag: foi corrigida em três arquivos e nada impede que volte.
  Dizer isso é melhor que fingir cobertura.
- **O README diz "dezesseis portões, treze bloqueando"** na linha que cita **v0.2.0**. É uma
  citação **datada de uma versão publicada**; hoje são 17 e 14. Corrigir a frase faria a capa
  descrever o HEAD alegando ser a v0.2.0. Ela se acerta no próximo corte de versão.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
