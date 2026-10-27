# Rodada 4 — correção 3 (decidida pelo Darú em 27/10/2026, depois da parada do laço)

> A regra das duas rodadas parou o laço (`parada-do-laco.md`, `1e85cf1`). O Darú decidiu
> **reabrir uma correção 3 completa, com os três juízes de novo**, e tomou as três decisões de
> produto. Ponto de partida: HEAD `4e421a4` + plano do 074 (`1fc978b`). Alvo: as 7 notas em 8
> (juiz 1: P1, P5, P12; juiz 2: P8, P10, P15, P16) e as ressalvas menores. O juiz 3 já deu 16/16;
> a correção não pode regredir nada da Mensageria (regra 6 e verificador continuam o gate).

## Decisões do Darú (fixas)

- **D1 — matriz**: a linha "limites de orçamento e de taxa" **fica uma só** (tabela fixa de 26
  mantida); cada célula `sim`/`parcial` ganha a marca **`corta`** ou **`avisa`** (nota de coluna
  vira marca por célula), com a fonte da ficha. Célula sem fonte para a distinção: `avisa?` com
  motivo. O confronto cita a marca.
- **D2 — MCP sob a política**: "qual agente pode chamar qual ferramenta MCP" **é escopo da
  política allow/deny/ask por agente**. A tela de políticas ganha uma regra de exemplo com
  escopo `ferramenta MCP` (ex.: `registrar_peca`: `ask` para Worker, `allow` para regente por
  delegação, `deny` para sessão de outro projeto); o protocolo (`mensageria-04`) aponta para ela
  em cada ferramenta; o confronto registra a decisão; o mapa (§ 6.5) lista a política como ENTRA
  da Administração (fecha também P5 do juiz 1).
- **D3 — emissor do aviso de teto**: **desenhar agora**. O emissor é a ingestão de consumo do
  painel (`painel/custo.py`, ao ingerir): compara o consumo medido com o teto e o limiar
  declarados na Administração e, ao cruzar o limiar, **enfileira uma mensagem** na fila outbox
  endereçada à sessão dona e ao regente (`nome · ref · projeto`), com `data-fonte` apontando o
  módulo. A tela de orçamento ganha a seção "Quem emite o aviso" (processo, gatilho, idade do
  relógio, o que acontece se a ingestão estiver parada — "aviso atrasado, nunca perdido");
  `workflow-04` e `mensageria-02` mostram uma linha de exemplo do aviso. O **corte** (recusar,
  suspender) continua DEPOIS.

## Tarefas por dono (commit "ciclo 073: correção 3 da rodada 4 — <fatia>")

| Dono | Fatia |
|---|---|
| **Worker04** | `administracao-03-orcamento`: tabela de tetos com recusar/suspender marcados DEPOIS por linha (ou coluna só "avisar"); precedência = "o menor teto aplicável vence" **sem** a glosa do recorte; seção "Quem emite o aviso" (D3); `administracao-02-politicas`: regra de exemplo com escopo `ferramenta MCP` (D2) + frase "há `deny` não sobrescritível (o guard de imutáveis)"; `administracao-01-catalogo`: filtro e formulário com "Agente (perfil)" |
| **Worker05** | `workflow-02`: cartão "caída", cartões coerentes com a tabela, exemplo do Worker02 igual em `workflow-01/02/03`; `workflow-03`: `data-fonte` de desde/tentativas/tokens = "— (ledger parado no 064)"; `workflow-04`: linha de exemplo do aviso de teto (D3); `workflow-01`: citação `claude-code.md:59` do `stop`/`rm` marcada "a confirmar" ou ficha corrigida com Worker06 |
| **Worker03** | `mensageria-03`: linha "os nomes vêm do catálogo, seção Agentes (perfis)" (relação 3, caminho de volta); `mensageria-04`: cada ferramenta aponta para a regra MCP da política (D2); `mensageria-01/02`: ids de mensagem e remetentes iguais entre as duas telas; `mensageria-02`: linha de exemplo do aviso de teto |
| **Worker06** | `plataformas.md`: marca `corta`/`avisa` por célula na linha de orçamento/taxa (D1), com fonte; `claude-code.md:59`: conferir `stop` × `rm` × `attach`/`--resume` na documentação e corrigir a ficha; segurança documental; conformance 073 nos dois modos |
| **Worker02** | `confronto-decisao.md`: D1, D2, D3 registrados (ENTRA 4 = "declarar teto + avisar, com emissor desenhado"; ferramenta MCP como escopo da política); verbete "limite de orçamento" do glossário proposto ("declarado + aviso"); `mapa-de-contextos.md § 6.5`: política declarativa como ENTRA da Administração; verificador: só rodar (sem regra nova) |
| **Worker01** | README do protótipo (marcas da matriz, D2, D3, ENTRA 4 reescrito) e glossário (`docs/governance/glossary.md`: "ferramenta MCP como escopo de política", "emissor do aviso") |
| **Gerente** | integra, verificador 11 telas / 0 achados / seis regras, conformance nos dois modos, `andamento.md`, `[[DONE 073-correcao-3]]` a `MAESTRO [5d2fba]` com HEAD e tokens; não despacha juízes |

## Depois

Os três juízes voltam (contexto fresco, mesmos mandatos, comparando com a rodada 3). Resultado
vai ao Darú de qualquer forma: atingida → `[[DONE 073]]`, gate, merge na dev, promoção; não
atingida → o Darú decide de novo (fechar com ressalvas ou nova correção).
