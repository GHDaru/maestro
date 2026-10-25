# Task 072-T03b — texto do despacho (SendMessage falhou 3×; fallback acordado com o MAESTRO)

> O canal SendMessage para o Worker03 caiu três vezes seguidas (classificador indisponível).
> Conforme combinado com o MAESTRO ("se falhar duas vezes, commite o texto na sua branch, que eu
> leio de lá"), o texto integral do despacho fica aqui. O Worker03 [0b5dd3] deve executar o que
> segue; o Gerente [242008] integra o resultado.

`[[TASK id=072-T03b kind=test attempt=2 cycle=072 redoes=072-T03#1]]`

Gate do plano APROVADO COM CONDIÇÕES. Reconcilie e AMPLIE os testes na SUA worktree
`.claude\worktrees\worker03` (branch `w/worker03`, agora em 4669787 — confira com
`git rev-parse --short HEAD`; o merge do seu c1eb802 já está na branch de trabalho). Ao responder,
enderece a "Gerente [242008]" E copie o [[DONE]] para "MAESTRO [d60db8]". Commit final:
"ciclo 072: testes reconciliados e ampliados (gate do plano)". Sem implementação — só testes,
todos VERMELHOS pela razão certa.

## Nomes fixados (adapte os testes; ninguém negocia)

- `normaliza(valor, erros=None)` → dict `{canonico, original, motivo?}` (seu F6 adapta a isso).
- `idade_do_carimbo(carimbo, agora)` (seu F7 adapta).
- `portao_derivado(chamado, gate, status, commit)` → item com id "chamado+gate"; e NOVO helper
  puro `portoes_do_regente(chamado, commit_de)` → lista, que chama `portao_derivado`
  (o SEU teste venceu — ele entra).
- Funções puras que os seus testes já assumiam e agora são oficiais: `sem_fonte(motivo)` →
  "— motivo: ...", `aviso_ingestao(ingerido_em, agora)`, `cabecalho_fila(itens, agora)` →
  `{n, idade_mais_velha}`, `proposta_transicao(chamado, de, para, arquivos)` →
  `{permitido, falta?}`; todas em `painel/regencia/`.
- `acrescenta(caminho, linha)` vive em `painel/fila_registro.py` (adaptador); o F14 importa
  `fila_registro`. Escrita: um único write por linha, `open(..., "a")`, `threading.Lock`.
- Rota `POST /api/regencia/transicao`, corpo `{chamado, de, para}`; 422 com motivo (seu F3
  adapta o corpo).
- Pessoa: `cfg["regencia"]["pessoas"]` (lista de nomes humanos no `projetos/<nome>.json`);
  ruling com autor FORA da lista → recusado (422), mesmo com `registrado_por`. Ruling com pedido
  INEXISTENTE → recusado.

## Adaptações e testes novos (todos vermelhos pela razão certa)

1. Adaptar os 13 existentes aos nomes fixados (F6 dict de normaliza; F7 assinatura; F3 corpo
   `{chamado, de, para}`; F14 importando fila_registro).
2. Teste NEGATIVO de pessoa: ruling com autor fora de `cfg["regencia"]["pessoas"]` → 422
   (obrigatório, FR20/ambiguidade 1a).
3. Teste de ruling ÓRFÃO: ruling com pedido inexistente → recusado (obrigatório).
4. Teste de append CONCORRENTE: dois POST em paralelo → duas linhas, nenhuma perdida.
5. Teste estático (AST): `fila_registro.py` só abre arquivo em modo "a".
6. Testes de `ordena_fila` (FR15: prazo × bloqueio, nº de destravados) e `cabecalho_fila`
   (`{n, idade_mais_velha}`).
7. Teste FR4: marcador builder≠crítico (`autor_da_peca == por` → vermelho; diferentes → sem
   vermelho; sem `autor_da_peca` → "—" com motivo).
8. Teste FR5: parser de `painel/chamados.py` expõe `autor_da_peca` no item (regressão: sem o
   campo → "—" com motivo; `test_chamados.py` segue verde).
9. Teste FR1: dez colunas G0–G9 na ordem de `GATES` (nem mais, nem menos; abertura/GD fora).
10. Teste FR7: filtro por frente (`cfg["frentes"]`).
11. Teste FR11: `valida_pedido` exige os campos obrigatórios (id, pedido_por, pergunta,
    opcoes ≥1 com id+descricao, recomendacao, prazo, destrava, destino, status).
12. F1/F9: ficam como teste sobre o HTML SERVIDO + fragmentos; `_texto_do_botao` não conta
    `${...}` como texto (limitação D-072-8: renderização JS não verificada nesta rodada — o
    plano declara).

## Regressões e limites

- Regressões que seguem valendo: os 48 testes existentes intactos;
  `python painel/chamados.py painel/projetos/exemplo.json` → exit 0.
- Limites de sempre: só a sua worktree, sem push/merge/rm -rf, sem .env/settings.local.json,
  fixture sem dados reais.
- Aproveite e remova os dois arquivos temporários (`rg_new.txt`, `rg_old.txt`) da raiz da sua
  worktree via `bash rm` (Remove-Item foi negado; se bash rm também for, deixe e declare).

## Entrega

Ao terminar: commit e `[[DONE id=072-T03b outcome=delivered]]` para "Gerente [242008]" com SAÍDA
de comandos (`git log --oneline -1`; `pytest test_regencia.py -q` com a contagem de falhas e os
nomes; regressão dos 48), cópia para "MAESTRO [d60db8]". Se travar:
`[[DONE id=072-T03b outcome=blocked]]` com o que falta.
