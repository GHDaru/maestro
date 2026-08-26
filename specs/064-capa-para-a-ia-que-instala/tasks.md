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

## Cauda de fechamento — OBRIGATÓRIA, uma linha cada, nunca apagar
<!-- MARQUE SÓ AO ESCREVER A EVIDÊNCIA, nunca antes: a caixa registra o que aconteceu.
     Não apague uma linha para dizer que não se aplica: escreva `n/a: <razão>` nela.
     check-conformance.sh exige a evidência de cada passo não-n/a no qa-report.md. -->
- [ ] TAIL:review — revisão independente em contexto fresco, por quem não executou
- [x] TAIL:security — passagem de segurança proporcional à classe de risco
- [x] TAIL:mutation — todo portão criado ou alterado aqui, quebrado de propósito e visto reprovando
- [ ] TAIL:gate — DoD verde -> parecer do guardião -> portão humano de merge (não delegável)
