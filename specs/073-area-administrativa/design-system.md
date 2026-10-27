# Design system do painel de regência — v1 (medido em 26/10/2026)

> **Origem**: referência visual indicada pelo Darú, `https://yandehdemocenter.live/demo/smart-core`
> (Smart Core, a parte cadastral). A central de demos é uma casca escura que embute a aplicação
> real por `iframe` (`core-revisao-negocio.lovable.app`). Medi as duas camadas com
> `getComputedStyle` e as variáveis CSS do `:root`; nada é copiado, são **tokens** (valores) e
> **papéis** (para que servem). A identidade escolhida para o Maestro é a da **aplicação** (tema
> claro, Inter, laranja), não a da casca; a casca fica registrada como tema escuro alternativo.
>
> Siglas: CSS (*Cascading Style Sheets*) · HSL (*hue, saturation, lightness*, formato de cor) ·
> OKLCH (*lightness, chroma, hue* em OKLab) · UX (*user experience*) · CTA (*call to action*,
> ação principal de um cartão).

## 1. Tokens medidos (aplicação Smart Core — tema claro, o nosso)

Os valores vêm do `:root` da aplicação (HSL sem a função, no padrão shadcn/ui) e das cores
computadas mais frequentes.

| Token (nosso nome) | Valor medido | Papel |
|---|---|---|
| `--fundo` | `hsl(220 27% 98%)` = `#f9f9fb` | fundo da página |
| `--superficie` | `hsl(0 0% 100%)` | cartão, popover |
| `--superficie-2` | `hsl(210 40% 96%)` | chip inativo, fundo de ícone, campo de busca |
| `--tinta` | `hsl(222 47% 11%)` = `rgb(15,23,41)` | texto principal, segmento ativo (fundo), navy quase preto |
| `--texto-2` | `hsl(215 16% 47%)` = `rgb(101,117,139)` | texto secundário, legenda, placeholder |
| `--borda` | `hsl(214 32% 91%)` = `rgb(225,231,239)` | borda de cartão, chip, campo (a cor mais usada: 888 ocorrências) |
| `--borda-2` | `hsl(220 28% 82%)` | borda de ênfase |
| `--primaria` | `hsl(21 100% 55%)` = `rgb(255,106,26)` | ação principal, destaque numérico, link de ação |
| `--primaria-escura` | `hsl(21 100% 41%)` | hover do primário |
| `--primaria-clara` | `hsl(21 100% 96%)` | fundo de ícone laranja, realce suave |
| `--sucesso` | `hsl(159 74% 48%)` = `rgb(32,213,150)` | estado saudável, item de navegação ativo |
| `--alerta` | `hsl(42 93% 58%)` | atenção, "esperando" |
| `--erro` | `hsl(4 79% 58%)` = `rgb(233,75,63)` | erro, bloqueado, "para revisar" |
| `--info` | `hsl(239 84% 67%)` (= `--grafico-5`) | informação, série secundária |
| `--grafico-1..5` | `21 100% 55%` · `21 100% 86%` · `4 79% 58%` · `42 93% 58%` · `239 84% 67%` | séries: laranja, laranja-claro, vermelho, âmbar, índigo |
| `--raio-sm` / `--raio` / `--raio-lg` / `--raio-xl` / `--raio-pilula` | `6px` · `12px` · `16px` · `20px` · `9999px` | campos e ícones · chips e botões secundários · cartões · cartões grandes · botões e segmentos |
| `--sombra-sm` | `0 1px 2px hsl(220 25% 20% / .04)` | cartão em repouso |
| `--sombra` | `0 1px 3px hsl(220 25% 20% / .05), 0 1px 2px hsl(220 25% 20% / .03)` | cartão, botão primário, segmento ativo |
| `--sombra-md` / `--sombra-lg` / `--sombra-xl` | `0 2px 6px … .06` · `0 8px 24px … .08` · `0 16px 40px … .10` | popover · diálogo · modal |
| `--fonte` | `Inter, system-ui, sans-serif` | tudo (1060 nós); `ui-monospace` só para código |
| `--gradiente-primario` | `linear-gradient(135deg, hsl(21 100% 55%), hsl(14 95% 50%))` | fundo do botão "Novo", ícone de destaque |

**Tipografia medida**: título de página `22px / 27.5px`, peso 600 (o destaque em laranja usa o
mesmo tamanho); saudação `22px` peso 600 em `--tinta` com a frase-chave em `--primaria`; título de
cartão `14px` peso 600; corpo `14px / 21px` peso 400; secundário `13px / 19.5px` em `--texto-2`;
chip `11.5px` peso 500; rótulo de categoria em caixa alta `10px` peso 500, `letter-spacing`
visível; contadores `12px` peso 700.

**Componentes medidos**:

- **Botão primário** ("Novo Workflow"): fundo `--primaria`, texto branco, `14px`, altura 36 px,
  raio pílula, ícone "+" num círculo branco translúcido à esquerda, `--sombra`.
- **Segmento** (Hoje · Semana · Mês): trilho `--superficie-2` com raio pílula; ativo = fundo
  `--tinta`, texto `--fundo`, `13px` 500, padding `6px 16px`, `--sombra`; inativo = sem fundo,
  texto `--texto-2`.
- **Chip de filtro** (Estoque, Vendas…): fundo `--fundo`, borda `--borda`, raio pílula, altura 28 px,
  `11.5px` 500, ícone à esquerda; chip ativo = fundo `--primaria`, texto branco, contador em pílula
  branca translúcida.
- **Cartão** ("Pronto pra automatizar?"): fundo branco, borda `--borda`, raio `16px`, `--sombra`,
  padding 24 px; título `14px` 600 + subtítulo `13px` em `--texto-2`.
- **Cartão de lista** (sugestões): ícone em quadrado `--primaria-clara`/`--superficie-2` com raio
  `12px`; rótulo de categoria em caixa alta `10px` à direita; título `14px` 600; descrição `13px`
  `--texto-2`; rodapé com estado ("Pronto pra usar") à esquerda e **CTA laranja** pílula à direita.
- **Linha de lista compacta** (exemplos): ícone 32 px, título `13px` 600, subtítulo `12px`,
  chevron à direita, borda `--borda`, raio `12px`.
- **Campo de texto grande** (prompt): borda `--borda`, raio `16px`, placeholder `--texto-2`,
  ações (anexar, falar, enviar) como botões redondos 36 px dentro do campo.
- **Busca**: pílula `--superficie-2`, ícone lupa, atalho `⌘K` em caixa mono dentro do campo;
  contador "35 resultados" em `--texto-2` ao lado.
- **Barra superior**: busca à esquerda, botão primário, avatar circular laranja, seletor "BU
  Selecionada" em pílula branca, idioma, sino; tudo numa faixa branca com raio `20px` e `--sombra`.
- **Navegação inferior** (três itens): ícone + rótulo `12px`; ativo em `--sucesso` com fundo
  `--sucesso` a 10 %; inativo em `--texto-2`.
- **Status**: ponto colorido + texto `13px` (`--alerta` "Sistema saudável"; `--erro` "2 erros para
  revisar" em peso 500).

## 2. Tokens da casca (central de demos — tema escuro, alternativo)

`--tinta-escura: oklch(14.5% 0 0)` (fundo) · `--tinta-suave: oklch(20.5% 0 0)` (cartão) ·
`--osso: oklch(95.7% .014 84.6)` (texto creme e botão primário) · `--borda: oklch(100% 0 0 / .10)` ·
`--linha-vermelha: oklch(59.3% .243 32.5)` (foco e alerta) · fontes `DM Sans` + `JetBrains Mono`
(rótulos de ação em caixa alta, `10px`, `letter-spacing 2.8px`) · raio `0.625rem`, cartão `24px`.
Hierarquia por opacidade do creme (100 · 45 · 35 · 25 %). Fica como **tema escuro** do painel
quando houver; não mistura com o tema claro.

## 3. Princípios (o que a referência faz bem e vamos manter)

1. **Uma cor de ação só** (laranja) e **uma de estado positivo** (verde); vermelho só para erro
   e bloqueio; âmbar para atenção. Todo o resto é navy e cinza-azulado.
2. **Hierarquia por peso e cinza**, não por tamanho: títulos de cartão em 14 px 600; o que importa
   fica em `--tinta`, o contexto em `--texto-2`.
3. **Pílulas para o que é escolha** (segmentos, chips, botões), **raio 12 a 16 px para o que é
   conteúdo** (cartões, campos). Sombras quase invisíveis; a borda `--borda` faz o trabalho.
4. **Categoria em caixa alta pequena** no canto do cartão, ícone em tile colorido suave à
   esquerda, CTA laranja à direita: a anatomia do cartão de lista.
5. **A frase-chave da página em laranja** ("você tem 55 automações em execução agora"): número e
   ação juntos, uma linha, com seta laranja.

## 4. Objetos do Maestro sobre estes tokens (linguagem ubíqua → componente)

| Objeto (glossário) | Componente de referência | Regras visuais |
|---|---|---|
| **Frase-chave do regente** ("você tem 3 decisões esperando, a mais velha há 7 h") | saudação com destaque laranja + seta | número e ação em `--primaria`; idade do relógio em `--texto-2` |
| **Sessão de agente** (ref) | linha de lista compacta | nome em `--tinta` 13px 600; ref `[7c8d05]` em `ui-monospace` `--texto-2`; chevron abre a sessão |
| **Estado do agente vivo** | ponto de status + texto | trabalhando `--sucesso`; esperando `--alerta`; bloqueado `--erro`; sem tarefa `--texto-2`; sem sinal `--borda-2` tachado |
| **Veredito normalizado** (com o original ao lado) | chip | aprovado `--sucesso` a 10 % com texto `--sucesso`; devolvido `--primaria-clara` com `--primaria-escura`; vermelho provado `--erro` a 10 %; em curso `--superficie-2`; inválido tachado; original em mono `--texto-2` |
| **Coluna G0–G9** (gate) | cabeçalho de categoria em caixa alta 10px + contador 12px 700 | limite de idade em `--texto-2` |
| **Cartão de chamado em gate** | cartão de lista | tile com a sigla do gate; categoria = frente; título = id em mono + resumo; rodapé: idade à esquerda, selo de evidência à direita |
| **Pedido de decisão** (fila) | cartão de lista com CTA | CTA laranja "Responder"; prazo estourado = borda esquerda `--erro`; "o que destrava" como chips |
| **Ruling** | formulário em cartão + botão primário | opções em chips selecionáveis (ativa = `--primaria`); autor humano em campo com borda `--borda`; "Registrar ruling" pílula laranja |
| **Portão do regente** | item da fila com tile `--primaria-clara` | marcador no cartão do kanban em laranja |
| **Caixa de entrada / livro de mensagens** | lista compacta com ponto de não lida | não lida em `--tinta` + ponto laranja; lida em `--texto-2`; colisão de nome = chip `--erro` a 10 % "endereçar por ref" |
| **Filtro por frente / contexto** | chip de filtro com contador | ativo laranja, inativo com borda |
| **Consumo por agente / limite de orçamento** | número grande 22px 600 + barra | barra `--grafico-2` até 80 % do teto, `--primaria` até 100 %, `--erro` acima; etiqueta "declarado" ou "medido" em caixa alta 10px |
| **Período** (hoje · semana · mês) | segmento | igual à referência |
| **"—" com motivo** (regra F8) | texto `--texto-2` | nunca vazio |
| **`data-fonte`** (regra F1) | rodapé do cartão em `--texto-2` 12px, mono | comando ou caminho que produziu o número |
| **Navegação** | barra inferior (3 a 5 itens) ou lateral em desktop | ativo em `--sucesso`; Regência · Chamados · Fila · Sessões · Administração |

## 5. Aplicação

- `prototipo/tokens.css` com os tokens da seção 1 (nomes em português, valores medidos), e uma
  página `prototipo/amostra.html` que mostra cada componente da seção 4 com os objetos do Maestro:
  tarefa da rodada 4 se os juízes pedirem fidelidade visual; senão, da rodada de implementação.
- O painel v0 (`painel/index.html`) migra variável a variável (`--line` → `--borda` etc.) sem
  reescrever componentes de uma vez; as telas do 073 ficam em cinza até a decisão dos juízes.
- Capturas de referência (26/10): painel inicial, biblioteca de sugestões e o login da casca; os
  arquivos de imagem ficam fora do repositório (material de terceiro), só as medidas entram.
