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
// Endpoint do companion; vazio -> widget não é injetado (site funciona igual).
const COMPANION_URL = process.env.MAESTRO_COMPANION_URL || "";

const sumario = JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8"));
const itens = sumario.partes.flatMap((p) => p.itens.map((i) => ({ ...i, parte: p.nome })));

// MATERIAL (ciclo 054): página HTML autocontida que o livro publica e indexa, mas não
// renderiza no próprio molde — uma apresentação de tela cheia não cabe dentro do miolo de
// uma página. O arquivo de origem NÃO é alterado: o livro continua sendo adapter de uma
// fonte só, e a volta para o sumário é injetada na publicação.
const materiais = (sumario.materiais || []).map((m) => ({
  ...m,
  slug: basename(m.arquivo).replace(/\.html?$/i, "").toLowerCase(),
}));
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
// Material disputa o MESMO espaço de nomes em site/, então entra no mesmo mapa — senão a
// checagem valeria para metade das páginas e a outra metade sumiria calada.
// `index` (capa, mantida à mão) e `sumario` (gerado no fim) NUNCA foram itens, então nunca
// entraram aqui. Com material eles passaram a ser alcançáveis — um material chamado
// `index.html` sobrescrevia a capa versionada com o build verde, e um `sumario.html` era
// escrito e depois sobrescrito, publicado só na contagem. Achado da revisão do ciclo 054:
// o mapa de colisão tem de conter TODA página que existe em site/, não só as declaradas.
const vistos = new Map([
  ["index", "site/index.html (a capa, mantida à mão)"],
  ["sumario", "site/sumario.html (gerado pelo motor)"],
]);
const colisoes = [];
for (const i of [...itens, ...materiais]) {
  if (vistos.has(i.slug)) colisoes.push(`${i.slug}.html  ←  ${vistos.get(i.slug)}  +  ${i.arquivo}`);
  else vistos.set(i.slug, i.arquivo);
}
if (colisoes.length) {
  console.error(`✗ ${colisoes.length} colisão(ões) de slug (uma página sobrescreveria a outra):`);
  colisoes.forEach((c) => console.error("   " + c));
  console.error("   → renomeie o arquivo de origem: o nome do arquivo é o nome da página no site.");
  process.exit(1);
}

// Material declarado e ausente do disco FALHA o build. Publicar 38 páginas e omitir a
// única que não existe é indistinguível de publicar tudo — entrada faltando é reprovação,
// nunca silêncio (anti-padrão 16).
const ausentes = materiais.filter((m) => !existsSync(resolve(RAIZ, m.arquivo)));
if (ausentes.length) {
  console.error(`✗ ${ausentes.length} material declarado em sumario.json e ausente do disco:`);
  ausentes.forEach((m) => console.error(`   ${m.arquivo}  (declarado como "${m.titulo}")`));
  console.error("   → corrija o caminho em publicar/sumario.json, ou remova a declaração.");
  process.exit(1);
}

const publicados = new Set(itens.map((i) => i.slug));
// Caminho de origem -> página publicada, para que um link do livro para o material aponte
// para dentro do livro em vez de escapar para o GitHub (onde HTML aparece como fonte).
const materialPorCaminho = new Map(materiais.map((m) => [m.arquivo, m.slug]));

const md = new MarkdownIt({ html: true, linkify: false, typographer: false }).use(anchor, {
  permalink: anchor.permalink.ariaHidden({ symbol: "#", placement: "after" }),
  slugify: (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, ""),
});

// Reescrita de links internos: .md publicado -> .html; qualquer outro alvo do repo -> GitHub.
function resolverHref(href, srcDir) {
  if (!href || /^https?:|^#|^mailto:|^\/\//.test(href)) return href;
  const [alvo, hash] = href.split("#");
  const anc = hash ? "#" + hash : "";
  // resolve o caminho relativo à origem antes de derivar o slug (READMEs de pastas
  // diferentes têm slugs diferentes — ver slugDe).
  const rel = path.posix.normalize(path.posix.join(srcDir || ".", alvo)).replace(/^(\.\.\/)+/, "");
  if (materialPorCaminho.has(rel)) return materialPorCaminho.get(rel) + ".html" + anc;
  const slug = slugDe(rel);
  return /\.md$/i.test(alvo) && publicados.has(slug) ? slug + ".html" + anc : GITHUB_BASE + rel + anc;
}

const defOpen = md.renderer.rules.link_open || ((t, i, o, e, s) => s.renderToken(t, i, o));
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  const href = tokens[idx].attrGet("href");
  if (href) tokens[idx].attrSet("href", resolverHref(href, env.srcDir));
  return defOpen(tokens, idx, options, env, self);
};

// Bloco de HTML embutido no Markdown (ex.: o BPMN navegável) passa direto pelo
// renderer — nenhuma regra de link o toca. Reescreve os `<a href="...md">` dele
// com a MESMA regra, para o link valer no GitHub e no livro (ciclo 020).
const resolverHtmlBruto = (html, srcDir) =>
  html.replace(/(<a\b[^>]*\bhref=")([^"]+?\.md(?:#[^"]*)?)(")/gi, (_, ini, href, fim) => ini + resolverHref(href, srcDir) + fim);

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
${COMPANION_URL ? '<link rel="stylesheet" href="assets/companion.css">' : ""}
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
${COMPANION_URL ? `<script>window.MAESTRO_COMPANION_URL=${JSON.stringify(COMPANION_URL)};</script><script src="assets/companion.js"></script>` : ""}
</body></html>`;
}

// --- build ---
mkdirSync(resolve(SAIDA, "assets"), { recursive: true });
// limpa páginas geradas antigas (preserva a capa index.html, mantida à mão)
for (const f of readdirSync(SAIDA)) if (f.endsWith(".html") && f !== "index.html") rmSync(resolve(SAIDA, f));
cpSync(resolve(AQUI, "tema/estilo.css"), resolve(SAIDA, "assets/estilo.css"));
// assets do companion: copiados só quando há endpoint; removidos quando não há
// (senão ficam órfãos de um build anterior e vão para o site publicado).
for (const f of ["companion.css", "companion.js"]) {
  const destino = resolve(SAIDA, "assets", f);
  if (COMPANION_URL) cpSync(resolve(RAIZ, "companion/widget", f), destino);
  else if (existsSync(destino)) rmSync(destino);
}
cpSync(resolve(AQUI, "tema/app.js"), resolve(SAIDA, "assets/app.js"));
writeFileSync(resolve(SAIDA, ".nojekyll"), "");

let gerados = 0;
const imagens = new Set();
for (let k = 0; k < itens.length; k++) {
  const item = itens[k];
  const caminho = resolve(RAIZ, item.arquivo);
  if (!existsSync(caminho)) { console.warn(`  aviso: ausente -> ${item.arquivo}`); continue; }
  const fonte = readFileSync(caminho, "utf8");
  const corpo = marcarCallouts(resolverHtmlBruto(md.render(fonte, { srcDir: dirname(item.arquivo) }), dirname(item.arquivo)));
  // Copia as imagens que a página referencia (relativas à origem do markdown).
  for (const m of fonte.matchAll(/!\[[^\]]*\]\(([^)\s]+)\)/g)) {
    const alvo = m[1];
    if (/^https?:|^data:/.test(alvo)) continue;
    const origem = resolve(RAIZ, dirname(item.arquivo), alvo);
    if (existsSync(origem)) { cpSync(origem, resolve(SAIDA, basename(alvo))); imagens.add(basename(alvo)); }
  }
  writeFileSync(
    resolve(SAIDA, `${item.slug}.html`),
    pagina({ tituloPagina: item.titulo, corpo, atual: item.slug, prev: k === 0 ? { slug: "sumario", titulo: "Sumário" } : itens[k - 1], next: itens[k + 1] })
  );
  gerados++;
}

// Material: publicado do arquivo de ORIGEM, envolvido num documento mínimo. O fragmento
// traz o próprio <style>/<script> e não é tocado — a única coisa injetada é a volta para o
// livro, porque quem chega aqui pelo sumário precisa de caminho de volta (FR5).
for (const m of materiais) {
  const fonte = readFileSync(resolve(RAIZ, m.arquivo), "utf8");
  // O nome do material tem UMA fonte: o `titulo` do sumario.json. Ler também o <title> do
  // arquivo dava duas, já divergentes na primeira tentativa — cartão dizendo uma coisa e
  // aba do navegador dizendo outra, sem nada para notar (achado da revisão do ciclo 054).
  writeFileSync(
    resolve(SAIDA, `${m.slug}.html`),
    `<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${m.titulo} · ${sumario.titulo}</title>
<meta name="description" content="${(m.teaser || sumario.subtitulo).replace(/"/g, "&quot;")}">
<style>
  /* Chrome próprio do material: ele NÃO carrega assets/estilo.css — é autocontido por
     definição —, então o estilo da volta vive aqui. Sem opacidade: 12px a .55 dava 3.8:1
     no tema claro, abaixo de AA (achado da revisão do ciclo 054). */
  .volta-ao-livro { position: fixed; left: 16px; top: 14px; z-index: 60; font: 500 12px/1
    ui-monospace, SFMono-Regular, Menlo, monospace; letter-spacing: .08em; text-decoration: none;
    color: currentColor; padding: 7px 11px; border: 1px solid currentColor; border-radius: 8px;
    background: transparent; }
  .volta-ao-livro:hover { text-decoration: underline; }
  @media print { .volta-ao-livro { display: none; } }
</style>
</head><body>
<a class="volta-ao-livro" href="sumario.html">↩ livro</a>
${fonte}
</body></html>`
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
    .join("") +
  (materiais.length
    ? `<div class="s-parte">Material<em class="s-tipo">apresentação</em></div>` +
      `<p class="s-desc">Peças de tela cheia — abrem fora do molde do livro, com volta para cá.</p>` +
      `<div class="s-grid">${materiais
        .map((m) => `<a class="s-card" href="${m.slug}.html"><span class="s-ct">${m.titulo}</span>${m.teaser ? `<span class="s-cd">${m.teaser}</span>` : ""}</a>`)
        .join("")}</div>`
    : "");
writeFileSync(resolve(SAIDA, "sumario.html"), pagina({ tituloPagina: "Sumário", corpo: corpoSumario, atual: "sumario", prev: null, next: itens[0], ehSumario: true }));

// Portão de qualidade: link interno .html quebrado FALHA o build (e o CI).
const paginas = new Set(
  itens.map((i) => `${i.slug}.html`)
    .concat(materiais.map((m) => `${m.slug}.html`))   // material É página do livro (FR2)
    .concat("index.html", "sumario.html")
);
const quebrados = [];
for (const f of readdirSync(SAIDA)) {
  if (!f.endsWith(".html")) continue;
  const html = readFileSync(resolve(SAIDA, f), "utf8");
  for (const m of html.matchAll(/href="([^"]+)"/g)) {
    const href = m[1];
    if (/^https?:|^#|^mailto:|^\/\//.test(href)) continue;
    // .md que sobrou no HTML publicado = link não reescrito (some no site).
    if (/\.md(#|$)/.test(href)) { quebrados.push(`${f} -> [md cru] ${href}`); continue; }
    if (!/\.html(#|$)/.test(href)) continue;
    const alvo = basename(href.split("#")[0]);
    if (!paginas.has(alvo)) quebrados.push(`${f} -> ${href}`);
  }
  // Imagens também são links: <img src> quebrado é página quebrada (ciclo 020).
  for (const m of html.matchAll(/<img[^>]+src="([^"]+)"/g)) {
    const src = m[1];
    if (/^https?:|^data:|^\/\//.test(src)) continue;
    if (!imagens.has(basename(src)) && !existsSync(resolve(SAIDA, src))) {
      quebrados.push(`${f} -> [img] ${src}`);
    }
  }
}
if (quebrados.length) {
  console.error(`✗ ${quebrados.length} link(s) interno(s) quebrado(s):`);
  quebrados.forEach((q) => console.error("   " + q));
  console.error("   → publique o alvo (item em `partes` ou entrada em `materiais` no");
  console.error("     publicar/sumario.json), ou aponte o link para outro lugar.");
  process.exit(1);
}
console.log(`✓ Site gerado: ${gerados} páginas + sumário em site/ (links internos OK)`);
