---
gate: G3
papel: codigo
classe: B
objeto: painel/chamados.py @ d2822ef
spec: 00-chamado.md
vermelho: 6741315
data_objeto: 2026-10-09 07:43 -0300
veredito: APPROVE
por: W10
data: 2026-10-09 09:36 -0300
runner2: pendente medição na VM
---

# G3 código do 070: crítica de código sobre d2822ef (painel) e 8adb545a (CLI)

Autor: Assistente. Crítico: W10 (não é autor).

## Objeto

Dois objetos neste chamado:
1. **Painel** (maestro repo): `painel/chamados.py` @ d2822ef — verde, vermelho 6741315 (base 2796cbf)
2. **CLI** (hindiana repo): `scripts/maestro/conferir_chamado.py` @ 8adb545a — verde, vermelho 899b8ed5 (base a5d9bcff)

A correção é a mesma semântica em ambos: ordenar vereditos válidos por data do cabeçalho (mais nova vence), desempatando pelo commit do arquivo e depois pelo nome.

**Confirmação de leitura e teste das duas mudanças:** ambas as implementações
foram lidas linha a linha. O painel (`painel/chamados.py:118`) define
`ordem_veredito` com tupla `(data, commit, nome)` e aplica `sorted` em
`validos` (linha 151). O CLI (`scripts/maestro/conferir_chamado.py:127-130`)
aplica a mesma lógica inline com `strptime`. O vermelho 6741315 falha na base
2796cbf (sem `sorted`, ordem alfabética decide) e o verde d2822ef passa. O
vermelho 899b8ed5 falha na base a5d9bcff e o verde 8adb545a passa.

## Tabela SHALL

| ID | SHALL | código (arquivo:linha) | teste (arquivo:linha) | falha na base |
|----|-------|------------------------|----------------------|---------------|
| R1 | O veredito vigente é o de maior data do cabeçalho, não o último na ordem alfabética | `painel/chamados.py:118` — `return (data(item["data"]) or MINIMO, ...)` (primeiro elemento da tupla de sort) | `painel/tests/test_chamados.py:99` — `test_mais_novo_vence_mesmo_vindo_antes_no_alfabeto` | 2796cbf: sem `sorted`, FALHA (alfabeticamente último) vence; estado do gate sai errado |
| R2 | Empate de data desempata pelo commit do arquivo (mais recente vence) | `painel/chamados.py:118` — `dt.datetime.fromisoformat(quando) if quando else MINIMO` (segundo elemento da tupla) | `painel/tests/test_chamados.py:104` — `test_empate_de_data_desempata_pelo_commit_do_arquivo` | 2796cbf: sem `sorted`, não há desempate por commit; ordem alfabética decide |
| R3 | Empate final desempata pelo nome do arquivo (terceiro elemento da tupla) | `painel/chamados.py:118` — `item["arquivo"]` (terceiro elemento) | `painel/tests/test_chamados.py:104` — mesmo teste (cobertura indireta) | 2796cbf: sem `sorted`, nome não participa do critério |
| R4 | `validos` é ordenado por `ordem_veredito` antes de decidir o estado do gate | `painel/chamados.py:151` — `validos = sorted((i for i in itens if not i["erros"]), key=lambda i: ordem_veredito(i, commit_de))` | `painel/tests/test_chamados.py:99` — `assertEqual(g["estado"], "ok")` | 2796cbf: `validos = [i for i in itens if not i["erros"]]` (list comprehension sem sort) |

### CLI (hindiana repo) — mesma correção inline

| ID | SHALL | código (arquivo:linha) | teste (arquivo:linha) | falha na base |
|----|-------|------------------------|----------------------|---------------|
| R1 | O veredito vigente é o de maior data do cabeçalho | `scripts/maestro/conferir_chamado.py:128` — `data(i["h"].get("data", "")) or MINIMO` (primeiro elemento da tupla de sort) | `scripts/maestro/test_conferir_chamado.py:25` — `test_g6_mais_novo_vence_mesmo_vindo_antes_no_alfabeto` | a5d9bcff: sem `sorted`, FALHA (alfabeticamente último) vence; `g["estado"]` sai BARRADO |
| R2 | Empate de data desempata pelo commit do arquivo | `scripts/maestro/conferir_chamado.py:129` — `dt.datetime.strptime(i["commit"], ...) if i["commit"] else MINIMO` (segundo elemento) | `scripts/maestro/test_conferir_chamado.py:25` — mesmo teste (cobertura indireta) | a5d9bcff: sem `sorted`, não há desempate por commit |
| R3 | Empate final desempata pelo nome do arquivo | `scripts/maestro/conferir_chamado.py:130` — `i["arquivo"]` (terceiro elemento) | `scripts/maestro/test_conferir_chamado.py:25` — mesmo teste (cobertura indireta) | a5d9bcff: sem `sorted`, nome não participa |
| R4 | `validos` é ordenado antes de decidir o estado | `scripts/maestro/conferir_chamado.py:127` — `validos = sorted((i for i in itens if not i["erros"]), key=lambda i: ...)` | `scripts/maestro/test_conferir_chamado.py:48` — `assertEqual(g["estado"], "PASSOU", g)` | a5d9bcff: `validos = [i for i in itens if not i["erros"]]` (list comprehension sem sort) |

## Análise

A correção é correta e idiomática. A função `ordem_veredito` (painel) retorna
uma tupla `(data, commit, nome)` que `sorted` usa como chave — o Python ordena
tuplas elemento a elemento, exatamente a semântica exigida (data → commit → nome).
O CLI aplica a mesma lógica inline com `strptime` em vez de `fromisoformat`
porque o formato do commit é `%Y-%m-%d %H:%M:%S %z` (saída de `git log --format=%ai`),
enquanto o painel recebe ISO. Ambos tratam o caso de commit ausente com `MINIMO`.

O `MINIMO = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)` é um sentinel
seguro — qualquer data real de veredito será posterior.

A correção não altera o critério de aprovação (PASSA/BARRA), só a seleção
do veredito vigente entre múltiplos válidos. Não introduz regressão.

Sessao: W10
