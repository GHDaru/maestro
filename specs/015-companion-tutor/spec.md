# Spec 015 — Companion: o tutor do livro

- **Status**: Aprovada ("bora") · **Raia**: Plena · **Data**: 2026-08-01
- **Origem**: ADR 0011, decisão 4 — o Steward escolheu a opção (c): backend real, com
  cota gratuita do NVIDIA NIM e banco Neon disponíveis.

## O quê e por quê

O livro ensina, mas não responde. O companion é o **tutor**: responde sobre o método a
partir do próprio livro, citando a página — o que fecha o ciclo pedagógico (o leitor tira
a dúvida sem sair do site) e aplica ao serviço as regras que o livro prega (citar fonte,
sigla por extenso, não inventar).

## Requisitos funcionais

- **FR1 — Busca no livro**: corpus gerado do sumário (uma entrada por seção), busca
  lexical com peso para título; sem embeddings (YAGNI).
- **FR2 — Tutor**: prompt que obriga responder a partir dos trechos, **citar a página**,
  expandir sigla na primeira ocorrência (Princípio VIII) e admitir quando o livro não cobre.
- **FR3 — Porta do modelo**: adaptador compatível com OpenAI (NVIDIA NIM por padrão) +
  `echo` sem chave; BYOK usado só na requisição, nunca persistido nem logado.
- **FR4 — Persistência**: Postgres (Neon) quando houver `DATABASE_URL`; memória sem ele —
  e banco fora do ar **não derruba** o serviço.
- **FR5 — API**: `/health`, `/sessao`, `/chat`, `/historico`, `DELETE /sessao/{id}`,
  `/sugestoes-de-inicio`; CORS restrito, limite por sessão e por tamanho de mensagem.
- **FR6 — Widget**: HTML/JavaScript puro, injetado no site **apenas** quando
  `MAESTRO_COMPANION_URL` estiver definida; fontes clicáveis; sessão anônima em
  `localStorage`; legível nos temas claro e escuro.
- **FR7 — Documentação**: `companion/README.md` (arquitetura, rodar local, publicar,
  segurança, manter o corpus fresco).

## Fora de escopo

- Ferramentas (tool-calling) no companion — o tutor só lê o livro.
- Painel de administração e telemetria de custo (segue em observar, ADR 0008).
- Publicação do serviço num provedor — depende de conta do Steward.

## Critérios de aceite (DoD)

- [ ] QUANDO `MAESTRO_COMPANION_URL` não estiver definida, O SISTEMA DEVE gerar o site
      sem nenhuma referência ao companion.
- [ ] QUANDO a mensagem exceder o limite, O SISTEMA DEVE responder 413 sem processar.
- [ ] QUANDO o leitor perguntar algo coberto pelo livro, O SISTEMA DEVE devolver ao menos
      uma fonte com página e URL.
- [ ] `pytest` verde (≥8 testes, com caso feliz e caso de falha).
- [ ] `/health` não expõe segredo.
- [ ] Widget legível em tema claro e escuro (evidência: capturas).

## Clarify (resolvido)

1. **Busca vetorial?** Não — lexical basta para dezenas de páginas; trocar só quando doer.
2. **Sem chave o que acontece?** Modo `echo`: fluxo e fontes reais, redação sintética.
