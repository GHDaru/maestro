# [[DONE id=072-condicoes outcome=delivered]] — fallback commitado (o mesmo texto foi ao regente por SendMessage)

> Fallback do fechamento das condições do gate do 072. O regente já abriu o TAIL:gate por
> delegação (`e4f5eb4`) e promoveu o ciclo à main (`d094763`, registro `45edb56`); este arquivo
> consolida a evidência que ficou pendente do lado do Gerente.

- **Condições**: T15 `11d295b` (integrado `d71cee6`) · T16 `39c2957`+`c8632db` (`bbfab80`) ·
  T17 `02e434f` (`1998e3e`) · T18 `ae1fb84` (`85b1b7f`) · T19 `ab32ffc`.
- **Reverificação independente (Worker06, `d71cee6`)**: as quatro condições conferem;
  `28 passed` em `painel/tests/test_regencia.py`; `check-conformance.sh 072` verde nos dois modos
  (normal e `TICKED_ONLY=1`). Tokens W06 (piso): ~5.320k (54 turnos com usage).
- **Captura pós-T16 (Worker01, `6f91826`, integrado em `e79ca27`)**: regerada do build real pelo
  `docs/jornada/scripts/captura-072.sh`; o banner `1H60M` **não aparece mais** —
  `LEITURA VELHA: 15H35M`, coerente (floor(15,58h)=15, round(35,1min)=35) — **R8 fechado no
  build**; R7 (quadro estreito: `#main` 232px, uma trilha de 210px, G0–G9 empilhados) reproduz
  igual e segue para a rodada 2; a foto de 24/10 que registrava o defeito foi sobrescrita pela
  regeração (nome fixo do script) — o achado permanece no texto (jornada, linha R8; qa-report
  § 072-T17 e § 072-T17-captura).
- **Supersessão da suíte**: 13 → 15 → 24 → 26 (T16: TestT16ChamadoNaoNavega,
  TestT16LeituraVelhaConcorda) → 28 (T15: TestF11IdDoPedido); medida na árvore integrada:
  **28 passed + 48 passed**.
- **Tokens T16 (Worker04, piso)**: 13,39M input (deepseek-v4.1-flash), como no DONE dele.
- **Caveats declarados**: merges `e5f7a09`/`85b1b7f` sem citação de ciclo no subject —
  `git commit --amend` bloqueado por deny rule do usuário; dívida registrada, não corrigida.
  `check-cycle.sh 072` (W01, background): exit 1 por dívida PRÉ-EXISTENTE da linha — lane não
  declarada nos specs 066/070; lane `full` sem justificativa no 070-workflow-sqlite; 2 merges
  antigos sem citação de ciclo — nenhum achado dos commits novos.
