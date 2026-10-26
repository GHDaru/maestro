# [[DONE id=073-correcao-1 cycle=073 outcome=delivered]] — fallback commitado (o mesmo teor foi ao regente por SendMessage)

> Correção 1 da rodada 4 do ciclo 073 (área administrativa), fechada. **HEAD: `e522a69`** (branch
> `066-painel-de-regencia`). A segunda rodada de juízes é do regente, em contexto fresco.

## As seis fatias + o fechamento da regra 5, tudo integrado

| Fatia | Dono | Commit | Integração |
|---|---|---|---|
| preâmbulo R8 — rename das 3 telas da Administração | Worker04 | `9bb5917` | `741b130` |
| preâmbulo R9 — base de citação única + § Convenções + mapa §7 "fila outbox" | Worker02 | `46d254c` | `6a32e24` |
| Mensageria (4 telas: carimbo, pretendido × resolvido, estados, refs colidentes vivo/morto, canal real, quem autoriza) | Worker03 | `edbb32f`+`80a4c6d` | `d83920e` |
| Administração (3 telas: cadastrar proposto, precedência deny>ask>allow + default-deny, tetos por projeto/agente/modelo, auditoria com `changed_by`) | Worker04 | `5be4a31` | `bfe1da5` |
| README (tabela de identidade, colisões termo × endereço, ENTRA 12 e 17, navegação medida) + glossário (+2 termos) | Worker01 | `0deccf4` | `bd51e4d` |
| Workflow (4 telas: derrubar por confirmação com regente protegido, reiniciar, ações por estado, custo em US$ com teto da Administração) + inventário | Worker05 | `952ce53` | `5d91a1a` |
| Confronto (ENTRA 15 · NÃO PRECISA 6 · DEPOIS 11, com gatilhos) + mapa (orçamento na Administração, invariante de endereço ambíguo, § 7.1) + **regra 5 do verificador** | Worker02 | `11efa79` | `eb638b2` |
| fechamento da regra 5 — Workflow (4) | Worker05 | `fb599bb` | fast-forward |
| fechamento da regra 5 — Mensageria (34) | Worker03 | `a04b6d0` | merge pós-`fb599bb` |
| Matriz (6 células, nenhuma `—`→`sim`; contagens por script 169/225/12/244; "corta × avisa"; "não encontrado na documentação lida") | Worker06 | `4257101` | `cb8a11a` |

## O gate e a conformance

```text
python specs/073-area-administrativa/prototipo/verifica-prototipo.py
-- verifica-prototipo: 11 screen(s), 0 finding(s)   [exit 0]
```

Cinco regras vivas, **incluindo a regra 5** (identidade `nome · ref · projeto`, ref `[xxxxxx]`
adjacente em todo texto visível e atributo; isenção só na tabela `data-rotulo="colisão de nomes"`).
Mutação da regra 5 (W02): 36 → 6 com a regra cega, restauração provada por SHA-256.

```text
bash scripts/check-conformance.sh 073              → exit-normal=0
TICKED_ONLY=1 bash scripts/check-conformance.sh 073 → exit-ticked=0
```

**Discrepância declarada:** a regra 5 acusou 29 no corpus do W02 e **39** no topo integrado (o
corpus dele não tinha as telas da correção 1 do W03/W05; a tabela de endereços da `mensageria-03`
trouxe 11). Fechados por dono: 34 W03 (ref em `<span class="mono">` → nó de texto diferente) e
4 W05 (ref separado por `:`/`(agente)`). Detalhe no qa-report § fechamento.

## Tokens (pisos — `tarefas.jsonl` parou no ciclo 064; soma de `message.usage` dos transcripts)

W04 R8 4.219.636 · W02 R9 821.054 · W03 mensageria 5.542.221 · W04 administração 11.671.366 ·
W01 readme+glossário 3.248.622 · W05 workflow+inventário 16.918.086 · W02 confronto/mapa/regra 5
20.453.582 · W05 regra 5 4.156.209 · W03 regra 5 4.119.310 · W06 matriz 5.274.507 —
**total ≈ 76,4 M (piso, não fatura)**.

## Limites cumpridos

Nenhum push, nenhum merge na dev/main, nenhum promote-main.sh, nenhum `rm -rf`, nenhuma leitura de
`.env`/`settings.local.json`, só acréscimo em ADR/decisoes.jsonl, sem código de produto, sem
segredo, siglas expandidas (Princípio VIII). Juízes da segunda rodada **não despachados** — são do
regente. Se a segunda rodada repetir o diagnóstico, o laço para (regra das duas rodadas).
