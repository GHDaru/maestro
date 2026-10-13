# Tasks 064 — Capa para a IA que instala

## Verificação primeiro
- [x] T0 — medir a recusa sem terminal: código de saída, mensagem e arquivos escritos

## Implementação
- [x] T1 — reescrever a seção de instalação do README na ordem que uma IA precisa
- [x] T2 — bifurcação no topo da seção "Se você é uma IA": instalar × trabalhar no método
- [x] T3 — publicar a tabela dos ids do `--ai` no README
- [x] T4 — estender o portão de ids de `check-installed.sh` às duas páginas, com extração escopada
- [x] T5 — tabela ausente passa a reprovar, nas duas páginas
- [x] T6 — verificação pós-instalação passa a ser `check-install.sh`, de dentro do projeto
- [x] T7 — corrigir "12 capítulos" para 13

## Depois da revisão independente (reprovou a primeira entrega)
- [x] T8 — encadear o comando publicado e tirar o clone de `/tmp` (achado 1, bloqueante)
- [x] T9 — `site/index.html`: a capa publicada passa a ter a mesma forma (achado 2, bloqueante)
- [x] T10 — portão novo: todo `--ai <valor>` das três páginas × `install-agents.tsv` (achado 3)
- [x] T11 — portão novo: as âncoras do README para ele mesmo resolvem (achado 4)
- [x] T12 — "quatro perguntas" → três; a tabela de camadas passa a dizer que é `--ai claude` (achados 6 e 8)
- [x] T13 — corrigir as afirmações sem lastro em `spec.md` e `qa-report.md` (achados 4 e 7)
- [x] T14 — achados 5 e 9 registrados como dívida declarada em `docs/records/decisoes.jsonl`

## Cauda de fechamento — OBRIGATÓRIA, uma linha cada, nunca apagar
<!-- MARQUE SÓ AO ESCREVER A EVIDÊNCIA, nunca antes: a caixa registra o que aconteceu.
     Não apague uma linha para dizer que não se aplica: escreva `n/a: <razão>` nela.
     check-conformance.sh exige a evidência de cada passo não-n/a no qa-report.md. -->
- [x] TAIL:review — revisão independente em contexto fresco, por quem não executou
- [x] TAIL:security — passagem de segurança proporcional à classe de risco
- [x] TAIL:mutation — todo portão criado ou alterado aqui, quebrado de propósito e visto reprovando
- [x] TAIL:gate — DoD verde -> parecer do guardião -> portão humano de merge (não delegável)
