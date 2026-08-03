# ADR 0011 — Livro Maestro: padrão editorial, navegação e companion com backend

- **Status**: Aceito · **Data**: 2026-08-01 · **Ciclo**: 013 · **Decisor**: Steward

## Contexto

O site publicado (V0) era uma página de vendas com âncoras: os capítulos eram documentos
de **referência**, não de ensino, e seis links da capa saíam para arquivos `.md` no
GitHub. O Steward apontou: *"quase um PPT; quero algo parecido com o livro
harness_engineering, com o chat no ar, e que seguindo o livro se entenda o que o Maestro
faz"*. Faltava projeto pedagógico, trilha de leitura e o companion.

## Decisão

1. **Padrão editorial** (`docs/livro/guia-editorial.md`): Backward Design + Diátaxis +
   carga cognitiva + 4C/ID; **esqueleto de capítulo em 9 seções**, com duas obrigatórias
   que são nossa marca — *§6 exemplo de ciclo real* e *§8 verificação*. Iron Law:
   nenhum capítulo publica sem objetivos, exemplo real e verificação.
2. **Cinco trilhas de navegação** no site (Jornada · Capítulos · Receitas · Referência ·
   Bastidores); **nenhum link de conteúdo sai para o GitHub** — resta um único link
   externo deliberado, nos Bastidores.
3. **Migração gradual**: capítulos 01–12 permanecem na anatomia v1; migram um por ciclo.
   O capítulo **13 (decisões de engenharia)** é o piloto do v2.
4. **Companion com backend** (opção "c" escolhida pelo Steward): front estático em HTML
   puro no GitHub Pages + serviço próprio segurando a chave. Modelo por **NVIDIA NIM**
   (cota gratuita do Steward, demanda baixa) e persistência em **Postgres (Neon)** —
   sem `DATABASE_URL`, cai para memória. Arquitetura de referência: o `chat-companion` do
   `harness_engineering` (FastAPI hospedado em Railway).
5. **Instalação do método**: `scripts/install-maestro.sh` — instala agentes, skills,
   scripts, comandos, templates e governança em outro repositório, sem sobrescrever.

## Alternativas consideradas

- **Companion navegável sem modelo** (opção "a"): custo zero e estático, mas não é chat —
  o Steward já dispõe de cota e banco, então a fricção não se justificava.
- **Chave do leitor por requisição** (opção "b"): estático, porém fricção alta para o
  público-alvo (executivos e times avaliando o método).
- **Reescrever os 12 capítulos de uma vez**: lote grande, revisão impossível de fazer bem;
  contraria diffs pequenos e o gate por entrega.

## Consequências

- (+) O livro passa a **ensinar** (objetivos → evidência → conteúdo), não só documentar.
- (+) O item §6 (ciclo real) transforma nossa rastreabilidade em didática — diferencial
  que ninguém copia sem ter operado o método.
- (+) O instalador torna o Maestro **um harness instalável**, não um repositório de leitura.
- (−) Backend implica hospedagem e operação (custo baixo, mas não zero) — e chave em
  variável de ambiente, nunca no repositório.
- (−) Dois padrões editoriais coexistem durante a migração; mitigado por nota no índice.

## Registro

`docs/livro/guia-editorial.md` · `docs/handbook/13-decisoes-de-engenharia.md` (piloto) ·
`scripts/install-maestro.sh` · ciclo `specs/013-livro-guia-editorial-piloto/`.
