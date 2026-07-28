# publicar/ — o motor do site do Maestro

App próprio (não framework) que gera o **site navegável** a partir do Markdown em `docs/`.
Coerente com a tese do Maestro (fonte única + adapter): a fonte é o Markdown; o site é um
adapter sobre ela. Didática emprestada de `harness_engineering` (callouts pedagógicos,
sidebar, tema claro/escuro, gate de link quebrado).

## Uso

```bash
cd publicar
npm install
npm run build     # gera ../site/ (páginas + sumário; a capa ../site/index.html é mantida à mão)
```

Abra `../site/index.html`.

## Como funciona

- `sumario.json` — ordem canônica (partes → itens com `arquivo`/`titulo`/`teaser`).
- `build.mjs` — converte cada `.md` (markdown-it + âncoras), marca callouts pedagógicos,
  reescreve links internos (`.md`→`.html`; o resto → GitHub), monta cada página (sidebar +
  anterior/próximo + tema) e o `sumario.html`. **Link interno quebrado falha o build.**
- `tema/estilo.css` + `app.js` — identidade Maestro + alternância de tema.
- Saída em `../site/` (deploy via GitHub Pages / `.github/workflows/pages.yml`).

## Deploy

GitHub Actions (`pages.yml`) builda e publica a cada push no `main` que toque `docs/`,
`publicar/` ou a capa. **Ativar uma vez**: Settings → Pages → Source = **GitHub Actions**.
Site: `https://ghdaru.github.io/maestro/`.
