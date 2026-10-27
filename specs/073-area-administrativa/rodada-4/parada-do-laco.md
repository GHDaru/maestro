# Rodada 4 — parada do laço: o que vai ao Darú (regente, 27/10/2026, sobre HEAD 4e421a4)

> Terceira e última leitura dos três juízes em contexto fresco. **Juiz 3 (intercomunicabilidade):
> barra atingida, 16 peças em 9.** **Juiz 1 (controle): 13 em 9, três em 8** (P1 matriz, P5
> mapa, P12 orçamento). **Juiz 2 (administração): 12 em 9, quatro em 8** (P8 orçamento, P10
> estado do agente vivo, P15 roteamento, P16 protocolo). O diagnóstico mudou nos três (nenhuma
> peça caiu; os fios da rodada 2 fecharam). Pela regra combinada — terceira leitura abaixo de
> 9 não gera correção 3 — **o laço para e a decisão é do Darú**. Pareceres:
> `juiz-{1,2,3}-*-rodada-3.md`.

## Trajetória (44 notas abaixo de 9 → 7)

| Leitura | Juiz 1 em 9 | Juiz 2 em 9 | Juiz 3 em 9 | Nota mínima |
|---|---|---|---|---|
| 1 (83c386e) | 0 / 16 | 0 / 16 | 0 / 16 | 5 |
| 2 (faca232) | 4 / 16 | 5 / 16 | 6 / 16 | 7 |
| 3 (4e421a4) | 13 / 16 | 12 / 16 | 16 / 16 | 8 |

## O que resta, separado por natureza

### A. Edições de texto (sem decisão nova; ~1 h de um Worker, uma leitura só)

1. **Tabela de tetos** (`administracao-03-orcamento.html:146,156,166,171-175`): marcar "recusar"
   e "suspender" como DEPOIS nas linhas (ou reduzir a coluna a "avisar") e cortar a glosa "recorte
   mais estreito"; vale só "o menor teto aplicável vence". *(juízes 1 e 2)*
2. **Política no mapa** (`mapa-de-contextos.md § 6.5`): acrescentar "política declarativa
   (allow/deny/ask)" como ENTRA da Administração — hoje o § 6.5 lista quatro e a tela se declara
   da Administração. *(juiz 1)*
3. **Estado do agente vivo** (`workflow-02`): cartão "caída" no resumo; cartões coerentes com a
   tabela; exemplo do Worker02 igual nas três telas do Workflow. *(juiz 2)*
4. **Roteamento → catálogo** (`mensageria-03`): uma linha "os nomes vêm do catálogo, seção
   Agentes (perfis)" (relação 3, caminho de volta). *(juiz 2)*
5. **Ressalvas menores**: ids de mensagem iguais entre `mensageria-01` e `-02`; verbete
   "limite de orçamento" do glossário proposto ("executável" → "declarado + aviso"); filtro do
   catálogo com "Agente (perfil)"; citação `claude-code.md:59` do `stop`/`rm` marcada "a
   confirmar" ou a ficha corrigida; frase sobre `deny` não sobrescritível nas políticas.

### B. Decisões de produto (só o Darú)

- **D1 — Matriz de plataformas, linha "limites de orçamento e de taxa"** (juiz 1, P1): separar
  em duas linhas (muda a "tabela fixa de 26" que a spec do 073 fixou → 27) **ou** marcar por
  célula se o `sim` corta ou só avisa, mantendo as 26. Recomendação da regente: **marcar por
  célula** (não mexe na spec; o confronto já desdobrou as duas).
- **D2 — Chamadas MCP sob a política allow/deny/ask por agente** (juiz 2, P16; lacuna que repete
  nas três leituras): hoje o protocolo só diz quem autoriza leitura e escrita de cada ferramenta;
  não diz se "qual agente pode chamar qual ferramenta MCP" é regra da política. Opções: (a) sim,
  a ferramenta MCP é um escopo da política (a tela de políticas ganha uma regra de exemplo e o
  protocolo aponta para ela); (b) não nesta rodada — DEPOIS com gatilho ("quando o painel tiver
  mais de uma ferramenta de escrita"). Recomendação da regente: **(a)** — é uma regra de exemplo
  e coerente com "toda ação de escrita diz quem autoriza".
- **D3 — Quem emite o aviso de teto** (juiz 1, P12): o aviso é "efeito de hoje", mas nenhum
  processo calcula o cruzamento do limiar. Opções: (a) declarar como dívida da raia infra junto
  com o ponto de execução do corte (uma linha em "Limites"); (b) desenhar agora o emissor (o
  hook de consumo do painel, `painel/custo.py`, ao ingerir). Recomendação: **(a)** — mesma
  natureza da dívida já declarada.

### C. O que a regente propõe como fechamento

**Aceitar o 073 como "barra atingida com ressalvas declaradas"** (como o ADR 0025 fez com o
070): as 16 ENTRA têm tela, as 25 plataformas têm ficha, três leituras independentes convergiram
para 41 de 48 notas em 9 e o que resta é texto mais três decisões. As edições do bloco A e as
decisões D1–D3 entram como **correção de fechamento** (uma rodada, sem nova leitura dos três
juízes; uma revisão fresca de um só crítico confere os 9 itens), e o ciclo fecha com `[[DONE
073]]`, gate por delegação, merge na dev e promoção. A alternativa é uma correção 3 completa com
os três juízes de novo (≈ 500 k tokens da regente por leitura).

**Precisa do Darú**: D1, D2, D3 e a escolha entre "fechamento com ressalvas" e "correção 3".
