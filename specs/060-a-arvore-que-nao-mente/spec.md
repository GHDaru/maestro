# Spec 060 — A árvore que não mente

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-17
- **Origem**: o Steward perguntou *"a árvore do Claude está no livro/documentação?"*. Não
  estava: o ciclo 059 escreveu "vamos colocar na documentação" e colocou na **capa do
  repositório**, que é outra coisa. Quem chega pelo site — pela porta que o 058 criou — não vê.

> **Raia**: plena. **Ambiguidade** baixa (o defeito é conhecido e medido); **raio** contido a
> documentação mais uma asserção num portão que já existe; **irreversibilidade** baixa.

## O quê e por quê

**Medido antes de escrever:**

| Fato | Como se sabe |
|---|---|
| A árvore existe fora do livro, em duas cópias | `grep -rln 'meu-app/'` devolve **dois** arquivos: `README.md` e o `plugin/maestro/README.md` gerado dele |
| O `README.md` **não** está no livro | não aparece em `publicar/sumario.json` |
| A receita **está** no livro e **não** tem a árvore | `grep -c 'meu-app/'` na receita = **0** |
| O bloco para IA não está em lugar nenhum do livro | `grep -c` na receita e no `comece-por-aqui` = 0 |

E há a lacuna maior, que a pergunta expõe: **nada verifica que a árvore publicada corresponde
a uma instalação real.** Hoje ela está certa porque foi gerada de uma instalação e conferida
pela revisão. No ciclo em que o instalador mudar o que copia, ela passa a mentir e nada avisa.
É a mesma família do `check-version` e do `check-flags` — um fato dito em dois lugares — só que
os dois lugares aqui são **um documento e o disco**.

## Requisitos funcionais

- **FR1**: A árvore pós-instalação DEVERÁ viver **num lugar só**, dentro do livro, e o
  `README.md` DEVERÁ apontar para lá em vez de repetir. Duas cópias divergem; é o que este
  método passa a sessão inteira provando.
- **FR2**: O livro DEVERÁ deixar visível que existe **instrução para uma IA que abre o
  repositório**, e onde ela está.
- **FR3**: O SISTEMA DEVERÁ **reprovar** quando a árvore documentada divergir de uma
  instalação real: diretório documentado que não é criado, e diretório criado que a
  documentação não menciona.
- **FR4**: A verificação do FR3 DEVERÁ rodar contra uma instalação **feita na hora**, nunca
  contra uma lista escrita à mão — senão são duas listas, e o problema volta um nível acima.

## Fora de escopo

- **Mover o bloco para IA para o livro.** Ele existe para um agente que **abre o
  repositório**, e o que um agente abre é o `README.md`, não o site publicado. Movê-lo o
  enfraqueceria em nome de simetria. O livro **aponta** para ele (FR2) — uma cópia, no lugar
  do consumidor, referenciada de onde faz falta.
- Um 18º portão. A asserção entra no `check-installed.sh`, que **já instala num diretório
  temporário**: criar um portão novo para reusar a mesma instalação seria cerimônia.
- Documentar a árvore de cada agente. A publicada é a do `--ai claude`, **declarada como
  tal** desde o 059; o portão confere essa.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- A árvore está na receita, dentro do livro, e o `README.md` aponta para ela sem repeti-la.
- O livro diz que existe instrução para IA e onde encontrá-la.
- O portão reprova nos **dois** sentidos — documentado e ausente, criado e não documentado —
  cada um **visto falhando**.
- O portão lê a árvore **do documento** e compara com uma instalação feita na hora.
- Bateria completa, plugin e build verdes.

## Clarify

1. E se alguém quiser a árvore no README de novo? → O portão do FR3 lê **a receita**. Uma
   segunda árvore no README voltaria a divergir sem aviso — por isso o README aponta.
2. A árvore documenta diretórios ou arquivos? → **Diretórios de primeiro nível mais o
   `CLAUDE.md`**. Arquivo a arquivo tornaria a documentação um manifesto, e manifesto já existe
   em `.maestro/manifest.tsv`.
