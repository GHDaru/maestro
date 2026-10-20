---
gate: G3
papel: criterio
objeto: painel/chamados.py @ 98a62a1
veredito: APPROVE
por: W01
data: 2026-10-09 10:24 -0300
data_objeto: 2026-10-09 10:08:13 -0300
---

# G3 critério — W01 @ d2822ef (painel) + 8adb545a (CLI)

Objeto principal: `painel/chamados.py @ d2822ef` (maestro). O corpo cobre
também `scripts/maestro/conferir_chamado.py @ 8adb545a` (hindiana) — leitura
confirmada das duas mudanças. Não-autor (Assistente é autora).

## Veredito: APPROVE

Todos os 4 SHALLs (R1 a R4) têm código que atende. Cada linha da tabela tem
código (arquivo:linha), teste, e falha na base (hash G2). Nenhuma célula vazia,
nenhum "sem teste", nenhum gap.

## Tabela SHALL → código → teste → falha na base (hash G2)

### R1 — Vigente = maior data do cabeçalho

| Objeto | Código (arquivo:linha) | Teste | Falha na base (hash G2) |
|---|---|---|---|
| Painel | `chamados.py:115-118` (`ordem_veredito`: `data(item["data"])` como 1º elemento da tupla); `chamados.py:151` (`validos = sorted(..., key=ordem_veredito)`); `chamados.py:219` (`v = validos[-1]["veredito"]`) | `test_chamados.py:99` (`test_mais_novo_vence_mesmo_vindo_antes_no_alfabeto`: b865c4a PASSA 21:00 vs fb901a1 FALHA 20:40 → G6 ok) | 6741315 (base 2796cbf: alfabético pegava fb901a1 FALHA → bad) |
| CLI | `conferir_chamado.py:127-129` (`validos = sorted(..., key=lambda i: (data(...) or MINIMO, ...))`); `conferir_chamado.py:189` (`validos[-1]`) | `test_conferir_chamado.py:25` (`test_g6_mais_novo_vence_mesmo_vindo_antes_no_alfabeto`: mesmo cenário → PASSOU) | 899b8ed5 (base: alfabético pegava fb901a1 FALHA → BARRADO) |

### R2 — Empate de data: commit do arquivo, depois nome

| Objeto | Código (arquivo:linha) | Teste | Falha na base (hash G2) |
|---|---|---|---|
| Painel | `chamados.py:118` (`dt.datetime.fromisoformat(quando) if quando else MINIMO, item["arquivo"]` — 2º e 3º elementos da tupla) | `test_chamados.py:104` (`test_empate_de_data_desempata_pelo_commit_do_arquivo`: ambos 21:00, b865c4a commit 21:05 vs fb901a1 commit 21:01 → G6 ok) | 6741315 (base 2796cbf: sem sorting por commit, alfabético pegava fb901a1 FALHA → bad) |
| CLI | `conferir_chamado.py:128-129` (`dt.datetime.strptime(i["commit"], ...) if i["commit"] else MINIMO, i["arquivo"]` — 2º e 3º elementos da sort key) | `test_conferir_chamado.py` @ b776de39 (`test_r2_empate_de_data_vence_o_commit_mais_recente`: mesma data, commit mais recente vence) | 899b8ed5 (base: `validos = [i for i in itens if not i["erros"]]` sem sorting, alfabético pegava o errado → BARRADO; passa no verde 8adb545a) |

### R3 — Sem data legível = mais antigo

| Objeto | Código (arquivo:linha) | Teste | Falha na base (hash G2) |
|---|---|---|---|
| Painel | `chamados.py:112` (`MINIMO = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)`); `chamados.py:118` (`data(item["data"]) or MINIMO` — None → MINIMO) | `test_chamados.py` @ 6ea2347 (`test_r3_veredito_sem_data_legivel_nao_vence`: veredito sem data legível não vence) | já atendido na base 2796cbf: o conferidor já exclui veredito sem data legível (`valida` em `chamados.py:83-87` rejeita com "falta 'data'" ou "data fora do formato") |
| CLI | `conferir_chamado.py:31` (`MINIMO = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)`); `conferir_chamado.py:128` (`data(...) or MINIMO`) | `test_conferir_chamado.py` @ b776de39 (`test_r3_veredito_sem_data_legivel_nao_vence`: veredito sem data legível não vence) | já atendido na base 899b8ed5: o conferidor já exclui veredito sem data legível (`valida` em `conferir_chamado.py:72-74`) |

### R4 — Trilha em ordem de data, não de nome

| Objeto | Código (arquivo:linha) | Teste | Falha na base (hash G2) |
|---|---|---|---|
| Painel | `chamados.py:393` (`eventos.sort(key=lambda e: _utc(e["quando"]) or dt.datetime.min.replace(tzinfo=dt.timezone.utc))` — trilha ordenada por data) | `test_chamados.py` @ 98a62a1 (`test_r4_trilha_em_ordem_de_data_nao_de_nome`: trilha em ordem de data; mutante verificado — sem o sort, o teste falha) | já atendido na base: passa no 2796cbf — `chamados.py:384` (base) já tinha `eventos.sort(key=lambda e: _utc(e['quando']) or ...)`; o diff verde (d2822ef) não alterou a função trilha |
| CLI | N/A — CLI não tem função trilha (`conferir_chamado.py` só tem `confere()`; a trilha é exclusiva do painel `chamados.py:356`). R4 menciona "lista de vereditos exibida na trilha", e a trilha só existe no painel | N/A por design | N/A por design |

## Prova R2 CLI (teste da Assistente @ b776de39)

```
test_r2_empate_de_data_vence_o_commit_mais_recente em test_conferir_chamado.py
Base 899b8ed5:  falha (sem sorting por commit)
Verde 8adb545a: passa (commit mais recente vence)
```

Sessao: W01
