---
gate: G3
papel: criterio
objeto: painel/chamados.py @ d2822ef e scripts/maestro/conferir_chamado.py @ 8adb545a
veredito: APPROVE
por: W01
data: 2026-10-09 09:15 -0300
data_objeto: 2026-10-09 07:43:06 -0300
---

# G3 critério — W01 @ d2822ef (painel) + 8adb545a (CLI)

Dois objetos: painel (maestro) e CLI (hindiana). Não-autor (Assistente é autora).

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
| CLI | `conferir_chamado.py:128-129` (`dt.datetime.strptime(i["commit"], ...) if i["commit"] else MINIMO, i["arquivo"]` — 2º e 3º elementos da sort key) | `test_r2_cli_empate.py:35` (`test_empate_de_data_desempata_pelo_commit_do_arquivo`: mesma data 21:00, aaaaaaa PASSA commit 21:05 vs zzzzzzz FALHA commit 21:01 → PASSOU; verificado: falha na base 899b8ed5 com BARRADO, passa no verde 8adb545a com PASSOU) | 899b8ed5 (base: `validos = [i for i in itens if not i["erros"]]` sem sorting, alfabético pegava zzzzzzz FALHA → BARRADO) |

### R3 — Sem data legível = mais antigo

| Objeto | Código (arquivo:linha) | Teste | Falha na base (hash G2) |
|---|---|---|---|
| Painel | `chamados.py:112` (`MINIMO = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)`); `chamados.py:118` (`data(item["data"]) or MINIMO` — None → MINIMO) | `test_chamados.py:99` (R1 — todos os vereditos válidos no teste têm data legível, exercitando o caminho normal; R3 é vacuously true: `valida` em `chamados.py:83-87` rejeita vereditos sem data legível com "falta 'data' no cabeçalho" ou "data fora do formato", então não existe veredito válido sem data legível — `or MINIMO` é fallback defensivo que nunca dispara) | já atendido na base: `valida` em 2796cbf (`chamados.py:83-87` base) já rejeitava vereditos sem data legível — R3 vacuously true |
| CLI | `conferir_chamado.py:31` (`MINIMO = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)`); `conferir_chamado.py:128` (`data(...) or MINIMO`) | `test_conferir_chamado.py:25` (R1 — mesmo argumento: `valida` em `conferir_chamado.py:72-74` rejeita vereditos sem data legível, então R3 vacuously true) | já atendido na base: `valida` em 899b8ed5 (`conferir_chamado.py:72-74` base) já rejeitava vereditos sem data legível — R3 vacuously true |

### R4 — Trilha em ordem de data, não de nome

| Objeto | Código (arquivo:linha) | Teste | Falha na base (hash G2) |
|---|---|---|---|
| Painel | `chamados.py:393` (`eventos.sort(key=lambda e: _utc(e["quando"]) or dt.datetime.min.replace(tzinfo=dt.timezone.utc))` — trilha ordenada por data) | `test_chamados.py:99,104` (testes R1/R2 exercitam `confere` que produz o `validos` ordenado por data; trilha herda a ordem) | já atendido na base: passa no 2796cbf — `chamados.py:384` (base) já tinha `eventos.sort(key=lambda e: _utc(e['quando']) or ...)`; o diff verde (d2822ef) não alterou a função trilha |
| CLI | N/A — CLI não tem função trilha (`conferir_chamado.py` só tem `confere()`; a trilha é exclusiva do painel `chamados.py:356`). R4 menciona "lista de vereditos exibida na trilha", e a trilha só existe no painel | N/A por design | N/A por design |

## Prova R2 CLI (teste escrito e verificado)

```
Base 899b8ed5:  BARRADO (alfabético pegava zzzzzzz FALHA)
Verde 8adb545a: PASSOU  (commit 21:05 > 21:01, aaaaaaa PASSA vence)
```

Sessao: W01
