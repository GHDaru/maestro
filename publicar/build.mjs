// Motor do site do Maestro — Markdown (docs/) -> site HTML navegável (site/).
// App próprio (não framework): markdown-it como biblioteca; o motor é nosso.
// Coerente com a tese do Maestro: a fonte é única (o Markdown); o site é um adapter.
// Uso: node build.mjs  (a partir de publicar/).  A capa (site/index.html) é mantida à mão.

import { readFileSync, writeFileSync, mkdirSync, cpSync, existsSync, readdirSync, rmSync } from "node:fs";
import { dirname, resolve, basename } from "node:path";
import path from "node:path";
import { fileURLToPath } from "node:url";
import MarkdownIt from "markdown-it";
import anchor from "markdown-it-anchor";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const SAIDA = resolve(RAIZ, "site");
const GITHUB_BASE = "https://github.com/GHDaru/maestro/blob/main/";

const sumario = JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8"));
const itens = sumario.partes.flatMap((p) => p.itens.map((i) => ({ ...i, parte: p.nome })));
// Slug do caminho (não só do nome): README.md/index.md usam o diretório pai, para que
// docs/handbook/README.md e docs/receitas/README.md não colidam em "readme.html".
const slugDe = (arq) => {
  const base = basename(arq).replace(/\.md$/i, "").toLowerCase();
  if (base !== "readme" && base !== "index") return base;
  const pai = basename(dirname(arq)).toLowerCase();
  return !pai || pai === "." || pai === "docs" ? base : pai;
};
itens.forEach((i) => (i.slug = slugDe(i.arquivo)));

// Fitness function: dois itens com o mesmo slug se sobrescreveriam em silêncio.
const vistos = new Map();
const colisoes = [];
for (const i of itens) {
  if (vistos.has(i.slug)) colisoes.push(`${i.slug}.html  ←  ${vistos.get(i.slug)}  +  ${i.arquivo}`);
  else vistos.set(i.slug, i.arquivo);
}
if (colisoes.length) {
  console.error(`✗ ${colisoes.length} colisão(ões) de slug (uma página sobrescreveria a outra):`);
  colisoes.forEach((c) => console.error("   " + c));
  process.exit(1);
}
const publicados = new Set(itens.map((i) => i.slug));

const md = new MarkdownIt({ html: true, linkify: false, typographer: false }).use(anchor, {
  permalink: anchor.permalink.ariaHidden({ symbol: "#", placement: "after" }),
  slugify: (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, ""),
});

// Reescrita de links internos: .md publicado -> .html; qualquer outro alvo do repo -> GitHub.
const defOpen = md.renderer.rules.link_open || ((t, i, o, e, s) => s.renderToken(t, i, o));
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  const href = tokens[idx].attrGet("href");
  if (href && !/^https?:|^#|^mailto:|^\/\//.test(href)) {
    const [alvo, hash] = href.split("#");
    const anc = hash ? "#" + hash : "";
    // resolve o caminho relativo à origem antes de derivar o slug (READMEs de pastas
    // diferentes têm slugs diferentes — ver slugDe).
    const rel = path.posix.normalize(path.posix.join(env.srcDir || ".", alvo)).replace(/^(\.\.\/)+/, "");
    const slug = slugDe(rel);
    if (/\.md$/i.test(alvo) && publicados.has(slug)) {
      tokens[idx].attrSet("href", slug + ".html" + anc);
    } else {
      tokens[idx].attrSet("href", GITHUB_BASE + rel + anc);
    }
  }
  return defOpen(tokens, idx, options, env, self);
};

// Callouts pedagógicos (didática): marca seções conhecidas para o CSS estilizar.
const TIPOS = [
  { re: /pergunta central|objetivos/i, cls: "c-obj", rot: "Objetivo" },
  { re: /^verifica/i, cls: "c-verif", rot: "Verificação" },
  { re: /o que roubar|recomenda[çc]/i, cls: "c-roubar", rot: "O que roubar" },
  { re: /na pr[áa]tica|m[ãa]o na massa/i, cls: "c-prat", rot: "Na prática" },
];
const marcarCallouts = (html) =>
  html.replace(/<h2([^>]*)>([\s\S]*?)<\/h2>/g, (full, attrs, tit) => {
    const limpo = tit.replace(/<[^>]+>/g, "").trim();
    const t = TIPOS.find((x) => x.re.test(limpo));
    return t ? `<h2${attrs} data-callout="${t.cls}">${tit}</h2>` : full;
  });

const navLateral = (atual) =>
  sumario.partes
    .map(
      (p) =>
        `<div class="nav-parte">${p.nome}${p.tipo ? `<em class="nav-tipo">${p.tipo}</em>` : ""}</div><ul>` +
        p.itens.map((i) => { const s = slugDe(i.arquivo); return `<li><a${s === atual ? ' class="ativo"' : ""} href="${s}.html">${i.titulo}</a></li>`; }).join("") +
        `</ul>`
    )
    .join("");

const btn = (item, dir) =>
  item ? `<a class="pg-${dir}" href="${item.slug}.html">${dir === "prev" ? "← " : ""}${item.titulo}${dir === "next" ? " →" : ""}</a>` : `<span></span>`;

function pagina({ tituloPagina, corpo, atual, prev, next, ehSumario }) {
  return `<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${tituloPagina} · ${sumario.titulo}</title>
<meta name="description" content="${sumario.subtitulo}">
<link rel="stylesheet" href="assets/estilo.css">
</head><body${ehSumario ? ' class="p-sumario"' : ""}>
<button id="alt-tema" aria-label="Alternar tema">◐</button>
<div class="layout">
  <aside class="sidebar">
    <a class="marca" href="index.html">${sumario.titulo}<small>Humano + IA</small></a>
    <a class="link-capa" href="index.html">↩ capa</a>
    ${navLateral(atual)}
  </aside>
  <main class="conteudo">
    <article class="markdown">${corpo}</article>
    <nav class="paginacao">${btn(prev, "prev")}${btn(next, "next")}</nav>
    <footer class="rodape">Maestro · gerado do Markdown pelo motor próprio · <a href="https://github.com/GHDaru/maestro">fonte no GitHub</a></footer>
  </main>
</div>
<script src="assets/app.js"></script>
</body></html>`;
}

// --- build ---
mkdirSync(resolve(SAIDA, "assets"), { recursive: true });
// limpa páginas geradas antigas (preserva a capa index.html, mantida à mão)
for (const f of readdirSync(SAIDA)) if (f.endsWith(".html") && f !== "index.html") rmSync(resolve(SAIDA, f));
cpSync(resolve(AQUI, "tema/estilo.css"), resolve(SAIDA, "assets/estilo.css"));
cpSync(resolve(AQUI, "tema/app.js"), resolve(SAIDA, "assets/app.js"));
writeFileSync(resolve(SAIDA, ".nojekyll"), "");

let gerados = 0;
for (let k = 0; k < itens.length; k++) {
  const item = itens[k];
  const caminho = resolve(RAIZ, item.arquivo);
  if (!existsSync(caminho)) { console.warn(`  aviso: ausente -> ${item.arquivo}`); continue; }
  const corpo = marcarCallouts(md.render(readFileSync(caminho, "utf8"), { srcDir: dirname(item.arquivo) }));
  writeFileSync(
    resolve(SAIDA, `${item.slug}.html`),
    pagina({ tituloPagina: item.titulo, corpo, atual: item.slug, prev: k === 0 ? { slug: "sumario", titulo: "Sumário" } : itens[k - 1], next: itens[k + 1] })
  );
  gerados++;
}

// sumario.html — o livro em cinco trilhas + a cadência educacional.
const cartao = (i) => `<a class="s-card" href="${slugDe(i.arquivo)}.html"><span class="s-ct">${i.titulo}</span>${i.teaser ? `<span class="s-cd">${i.teaser}</span>` : ""}</a>`;
const cardCadencia = (c) =>
  `<a class="s-cad" href="${slugDe(c.inicio)}.html"><span class="s-cad-n">${c.nome}</span><span class="s-cad-t">${c.tempo}</span><span class="s-cad-p">${c.percurso}</span></a>`;
const corpoSumario =
  `<h1>O livro</h1><p class="s-sub">${sumario.subtitulo}</p>` +
  (sumario.cadencia
    ? `<div class="s-parte">Por onde começar — escolha o seu tempo</div><div class="s-cad-grid">${sumario.cadencia.map(cardCadencia).join("")}</div>`
    : "") +
  sumario.partes
    .map(
      (p) =>
        `<div class="s-parte">${p.nome}${p.tipo ? `<em class="s-tipo">${p.tipo}</em>` : ""}</div>` +
        (p.descricao ? `<p class="s-desc">${p.descricao}</p>` : "") +
        `<div class="s-grid">${p.itens.map(cartao).join("")}</div>`
    )
    .join("");
writeFileSync(resolve(SAIDA, "sumario.html"), pagina({ tituloPagina: "Sumário", corpo: corpoSumario, atual: "sumario", prev: null, next: itens[0], ehSumario: true }));

// Portão de qualidade: link interno .html quebrado FALHA o build (e o CI).
const paginas = new Set(itens.map((i) => `${i.slug}.html`).concat("index.html", "sumario.html"));
const quebrados = [];
for (const f of readdirSync(SAIDA)) {
  if (!f.endsWith(".html")) continue;
  const html = readFileSync(resolve(SAIDA, f), "utf8");
  for (const m of html.matchAll(/href="([^"]+)"/g)) {
    const href = m[1];
    if (/^https?:|^#|^mailto:|^\/\//.test(href) || !/\.html(#|$)/.test(href)) continue;
    const alvo = basename(href.split("#")[0]);
    if (!paginas.has(alvo)) quebrados.push(`${f} -> ${href}`);
  }
}
if (quebrados.length) { console.error(`✗ ${quebrados.length} link(s) interno(s) quebrado(s):`); quebrados.forEach((q) => console.error("   " + q)); process.exit(1); }
console.log(`✓ Site gerado: ${gerados} páginas + sumário em site/ (links internos OK)`);
