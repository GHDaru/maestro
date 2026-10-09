---
gate: G3
papel: criterio
objeto: painel/chamados.py @ d2822ef e scripts/maestro/conferir_chamado.py @ 8adb545a
veredito: APPROVE
por: W01
data: 2026-10-09 08:14 -0300
data_objeto: 2026-10-09 07:43:06 -0300
---

# G3 critério — W01 @ d2822ef (painel) + 8adb545a (CLI)

Dois objetos: painel (maestro) e CLI (hindiana). Não-autor (Assistente é autora).

## Veredito: APPROVE

Todos os 4 SHALLs (R1 a R4) têm código que atende. R1 e R2 têm teste
vermelho provando a falha na base. R3 e R4 são code-attended com observação.

## Tabela SHALL → código → teste → falha na base (hash G2)

### R1 — Vigente = maior data do cabeçalho

| Objeto | Código (arquivo:linha) | Teste | Falha na base (hash G2) |
|---|---|---|---|
| Painel | `chamados.py:115-118` (`ordem_veredito`: `data(item["data"])` como 1º elemento da tupla); `chamados.py:151` (`validos = sorted(..., key=ordem_veredito)`); `chamados.py:219` (`v = validos[-1]["veredito"]`) | `test_chamados.py:99` (`test_mais_novo_vence_mesmo_vindo_antes_no_alfabeto`: b865c4a PASSA 21:00 vs fb901a1 FALHA 20:40 → G6 ok) | 6741315 (base 2796cbf: alfabético pegava fb901a1 FALHA → bad) |
| CLI | `conferir_chamado.py:127-129` (`validos = sorted(..., key=lambda i: (data(...) or MINIMO, ...))`); `conferir_chamado.py:189` (`validos[-1]`) | `test_conferir_chamado.py:25` (`test_g6_mais_novo_vence_mesmo_vindo_antes_no_alfabeto`: mesmo cenário → PASSOU) | 899b8ed5 (base: alfabético pegava fb901a1 FALHA → BARRADO) |

### R2 — Empate de data: commit do arquivo, depois nome

| Objeto | Código (arquivo:linha) | Teste | Falha na base (hash G2) |
|---|---|---|---|
| Painel | `chamados.py:118` (`dt.datetime.fromisoformat(quando) if quando else MINIMO, item["arquivo"]` — 2º e 3º elementos da tupla) | `test_chamados.py:104` (`test_empate_de_data_desempata_pelo_commit_do_arquivo`: ambos 21:00, b865c4a commit 21:05 vs fb901a1 commit 21:01 → G6 ok) | 6741315 |
| CLI | `conferir_chamado.py:128-129` (`dt.datetime.strptime(i["commit"], ...) if i["commit"] else MINIMO, i["arquivo"]`) | `test_conferir_chamado.py:25` (mesmo teste R1 — a sort key inclui commit e nome como tiebreakers; sem teste específico para o empate) | 899b8ed5 |

### R3 — Sem data legível = mais antigo

| Objeto | Código (arquivo:linha) | Teste | Falha na base (hash G2) |
|---|---|---|---|
| Painel | `chamados.py:112` (`MINIMO = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)`); `chamados.py:118` (`data(item["data"]) or MINIMO` — None → MINIMO) | `test_chamados.py:99` (R1 test — `or MINIMO` é parte da sort key testada; sem teste específico para data ilegível) | 6741315 |
| CLI | `conferir_chamado.py:31` (`MINIMO = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)`); `conferir_chamado.py:128` (`data(...) or MINIMO`) | `test_conferir_chamado.py:25` (R1 test — mesmo `or MINIMO` na sort key) | 899b8ed5 |

### R4 — Trilha em ordem de data, não de nome

| Objeto | Código (arquivo:linha) | Teste | Falha na base (hash G2) |
|---|---|---|---|
| Painel | `chamados.py:393` (`eventos.sort(key=lambda e: _utc(e["quando"]) or dt.datetime.min.replace(tzinfo=dt.timezone.utc))` — trilha ordenada por data) | `test_chamados.py:99,104` (testes R1/R2 exercitam `confere` que produz o `validos` ordenado por data; trilha herda a ordem) | 6741315 |
| CLI | N/A (CLI não tem função trilha; `validos` em `conferir_chamado.py:127-129` já é ordenado por data) | `test_conferir_chamado.py:25` | 899b8ed5 |

## Observações (não bloqueiam)

1. **R2 CLI:** o teste (`test_conferir_chamado.py:25`) cobre R1 (maior data vence) mas
   não testa especificamente o desempate por commit do arquivo (R2). O código implementa
   (`conferir_chamado.py:128-129`), mas não há teste específico para o empate no CLI.
   O painel tem teste específico (`test_chamados.py:104`).

2. **R3:** `or MINIMO` é parte da sort key exercitada pelos testes R1, mas nenhum teste
   cria um veredito sem data legível para provar que ele vai para o mais antigo. O código
   é claro (`data(...) or MINIMO`).

3. **R4:** a trilha do painel (`chamados.py:393`) ordena eventos por data. Não há teste
   específico para a ordem da trilha. O CLI não tem trilha (N/A).

## Conferidor

```
Chamado 070-conferidor-ordem-veredito: está em abertura
  abertura  FALTA     sem entregável
  G1        EM CURSO  spec sem crítica
  G3        FALTA     sem entregável
  ...
```

Sessao: W01
