# Spec 014 — Navegação do livro em cinco trilhas

- **Status**: Aprovada ("siga com o 014") · **Raia**: Plena · **Data**: 2026-08-01
- **Origem**: ADR 0011 (padrão editorial) — decisão 2: cinco trilhas, nenhum link de
  conteúdo saindo para o GitHub. O site era uma página de vendas com âncoras; os
  documentos existiam soltos, sem tipo declarado nem ordem de leitura.

## O quê e por quê

Transformar 25 páginas soltas em **livro navegável**: cada página declara seu tipo
(Diátaxis) e pertence a uma trilha; o leitor escolhe o percurso pelo **tempo que tem**.
Sem isso, capítulos migrados para o novo padrão continuariam ilhas.

## Requisitos funcionais

- **FR1 — Cinco trilhas** no sumário e na barra lateral, cada uma com **tipo** (tutorial ·
  explicação · como-fazer · referência) e **descrição** de quando usar.
- **FR2 — Trilha Receitas** (conteúdo novo): índice + instalar o Maestro + abrir um ciclo
  + escrever critério verificável + rodar a retrospectiva.
- **FR3 — Trilha A Jornada**: mapa da sequência de conhecimento (12 paradas com tensão,
  pergunta e regra nascida) ligando ao diário existente.
- **FR4 — Cadência educacional** no sumário: quatro percursos por tempo disponível
  (Entender ~20 min · Aprender ~2 h · Aplicar ~1 dia · Aprofundar contínuo).
- **FR5 — Capa entra no livro**: o "mapa de leitura" aponta para as cinco trilhas;
  nenhum link de conteúdo sai para o GitHub (o repositório fica em Bastidores).

## Fora de escopo

- Companion (backend + widget) — ciclo próprio.
- Migração dos capítulos 01–12 para o esqueleto v2 — um por ciclo.
- Reescrita da Jornada como diálogo longo — o mapa é a V1.

## Critérios de aceite (DoD)

- [ ] QUANDO o site for construído, O SISTEMA DEVE gerar ≥ 34 páginas com links internos OK.
- [ ] QUANDO dois itens do sumário resolverem para o mesmo slug, O SISTEMA DEVE falhar o
      build com código ≠ 0 e listar a colisão.
- [ ] `grep -c '"tipo"' publicar/sumario.json` = 5 (uma por trilha).
- [ ] `ls site/{jornada,handbook,receitas,adr,registro}.html` — cinco páginas distintas.
- [ ] Nenhum link de conteúdo da capa aponta para `github.com/.../blob/`.

## Clarify (resolvido)

1. **Jornada completa agora?** Não — o mapa é a V1 (o diálogo longo depende do companion).
2. **Onde fica o link do repositório?** Em Bastidores e no rodapé, como o Steward pediu
   ("pode ter em algum lugar um link para o git").
