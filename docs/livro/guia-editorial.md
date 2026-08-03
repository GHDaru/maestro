# Guia Editorial — como o Livro Maestro é escrito

> A versão operacional do projeto pedagógico: é o que se consulta **enquanto escreve**.
> Aprovado pelo Steward em 2026-08-01 (ciclo 013). Livro **vivo**: capítulo datado,
> histórico registrado.

## 1. O projeto pedagógico em quatro linhas

| Framework | O que dita no livro |
|---|---|
| **Backward Design** (Wiggins & McTighe) | Todo capítulo se projeta de trás para frente: objetivos → como verifico que aprendeu → só então o conteúdo |
| **Diátaxis** (Procida) | Quatro tipos de texto que **nunca se misturam** na mesma página: Jornada = *tutorial* · Capítulos = *explicação* · Receitas = *como-fazer* · Princípios/modelo/glossário = *referência* |
| **Carga cognitiva** (Sweller) | Uma ideia nova por vez; exemplo resolvido **antes** de exercício; andaime que diminui ao longo do livro |
| **4C/ID** (van Merriënboer) | A Jornada é a "tarefa inteira"; capítulos são informação de apoio; receitas são treino de parte |

## 2. Esqueleto obrigatório de capítulo (9 seções)

1. **Objetivos** — 3–5, com verbos mensuráveis (explicar, comparar, aplicar, avaliar).
2. **O problema** — por que este elemento existe; a dor concreta.
3. **A ideia central** — uma frase memorável; o que fica se o leitor esquecer o resto.
4. **A regra vigente** — o que o Maestro **manda** fazer (liga ao modelo operacional).
5. **Fundamentos** — teoria e frameworks avaliados, com fontes citadas.
6. **⭐ Na prática — o ciclo real** — evidência dos nossos próprios ciclos (número da spec,
   identificador do registro, saída de comando). **Obrigatória**: sem exemplo real, o
   capítulo não publica.
7. **Erros e anti-padrões** — o que dá errado, nomeado (liga à skill `anti-patterns`).
8. **Verificação** — 2–3 perguntas que testam exatamente os objetivos do item 1.
9. **O que roubar** — leitura executiva: o que exportar para outro contexto.

### Por que o item 6 é a nossa marca

Livros de metodologia usam exemplos inventados. Nós temos **13 ciclos reais** documentados,
com decisões registradas e comandos verificáveis. O capítulo de gates não *fala* de gate:
mostra o `gate-main-e32023f` no índice de decisões. Isso é a rastreabilidade (Princípio VI)
virando didática — e é o que nenhum concorrente consegue copiar sem ter operado o método.

## 3. Regras de escrita permanentes

- **Sigla nunca nasce nua** (Princípio VIII): primeira ocorrência **em cada página** por
  extenso, com a abreviação entre parênteses; termo novo entra no glossário.
- **Evidência por caminho**: afirmação sobre o método aponta arquivo, ciclo ou comando.
- **Prosa em português**; termos técnicos consagrados sem tradução (spec, gate, commit).
- **Tabela para fato enumerável**; a explicação vive na prosa, não nas células.
- **Uma ideia nova por seção** — se a seção mistura dois temas, separe (skill
  `fight-the-pile-up`).
- **Voz**: segunda pessoa para instrução ("escreva a spec"), primeira do plural para
  decisão nossa ("decidimos manter uma ferramenta só").

## 4. Livro vivo — datação obrigatória

Todo capítulo abre com:

```
> **Capturado em** AAAA-MM · última revisão AAAA-MM-DD · ciclo NNN
```

Três datas distintas: **do fato** (no corpo — imutável), **de captura** (cabeçalho —
quando fotografamos o estado da arte), **do ciclo** (qual spec produziu). Reavaliar gera
nova captura; nunca se sobrescreve o histórico.

## 5. As cinco trilhas do site

| Trilha | Tipo (Diátaxis) | O que é |
|---|---|---|
| **A Jornada** | tutorial | A sequência de conhecimento — o diálogo que construiu o método |
| **Os Capítulos** | explicação | Os elementos, no esqueleto de 9 seções |
| **Receitas** | como-fazer | Abrir um ciclo, escrever critério verificável, rodar a retro |
| **Referência** | referência | Princípios, modelo operacional, glossário, agentes, skills, templates |
| **Bastidores** | referência | Registros de decisão, apêndices de estudo, changelog — e o link para o repositório |

## 6. Cadência educacional

| Trilha | Tempo | Percurso |
|---|---|---|
| **Entender** | ~20 min | Capa → as três ideias → um ciclo real de ponta a ponta |
| **Aprender** | ~2 h | A Jornada completa (uma parada por elemento) |
| **Aplicar** | ~1 dia | Receitas + rodar o próprio primeiro ciclo |
| **Aprofundar** | contínuo | Capítulos + bastidores |

## 7. Iron Law editorial

```
NENHUM CAPÍTULO PUBLICA SEM OBJETIVOS, EXEMPLO REAL E VERIFICAÇÃO
```

Violar a letra é violar o espírito. Isso **não** é desculpa: "o tema é abstrato" (então o
exemplo real é ainda mais necessário) · "os objetivos são óbvios" (se são, escrevê-los
custa um minuto) · "verifico depois" (depois é onde o amontoado nasce).
