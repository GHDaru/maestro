/* Companion do livro Maestro — widget flutuante em JavaScript puro.
 *
 * Sem framework, sem build: é servido junto do site estático (GitHub Pages) e
 * conversa com o backend por HTTPS. A sessão é anônima e vive no localStorage;
 * o endpoint vem de window.MAESTRO_COMPANION_URL (injetado pelo motor do site).
 */
(function () {
  "use strict";

  var API = (window.MAESTRO_COMPANION_URL || "").replace(/\/$/, "");
  if (!API) return; // sem backend configurado, o widget nem aparece

  var CHAVE_SESSAO = "maestro.companion.sessao";
  var sessao = localStorage.getItem(CHAVE_SESSAO) || "";
  var ocupado = false;

  // --- montagem ---------------------------------------------------------
  var botao = document.createElement("button");
  botao.className = "cmp-botao";
  botao.type = "button";
  botao.setAttribute("aria-label", "Abrir o companion do livro");
  botao.innerHTML = "<span aria-hidden='true'>🎼</span>";

  var painel = document.createElement("section");
  painel.className = "cmp-painel";
  painel.hidden = true;
  painel.setAttribute("aria-label", "Companion do livro Maestro");
  painel.innerHTML =
    '<header class="cmp-cab">' +
      '<div><strong>Companion</strong><small>tutor do livro</small></div>' +
      '<button class="cmp-fechar" type="button" aria-label="Fechar">✕</button>' +
    "</header>" +
    '<div class="cmp-msgs" role="log" aria-live="polite"></div>' +
    '<form class="cmp-form">' +
      '<input class="cmp-entrada" type="text" autocomplete="off" ' +
        'placeholder="Pergunte sobre o método…" aria-label="Sua pergunta">' +
      '<button class="cmp-enviar" type="submit" aria-label="Enviar">→</button>' +
    "</form>" +
    '<p class="cmp-rodape">Respostas baseadas no livro, com a página citada. ' +
      "Pode errar — confira a fonte.</p>";

  document.body.appendChild(botao);
  document.body.appendChild(painel);

  var msgs = painel.querySelector(".cmp-msgs");
  var form = painel.querySelector(".cmp-form");
  var entrada = painel.querySelector(".cmp-entrada");

  // --- utilidades -------------------------------------------------------
  function escapar(t) {
    var d = document.createElement("div");
    d.textContent = t;
    return d.innerHTML;
  }

  function bolha(papel, texto, fontes) {
    var el = document.createElement("div");
    el.className = "cmp-msg cmp-" + papel;
    var html = escapar(texto).replace(/\n/g, "<br>");
    if (fontes && fontes.length) {
      html += '<div class="cmp-fontes"><span>no livro:</span> ' +
        fontes.map(function (f) {
          return '<a href="' + escapar(f.url) + '">' + escapar(f.pagina) + "</a>";
        }).join(" · ") + "</div>";
    }
    el.innerHTML = html;
    msgs.appendChild(el);
    msgs.scrollTop = msgs.scrollHeight;
    return el;
  }

  function sugestoes(lista) {
    var wrap = document.createElement("div");
    wrap.className = "cmp-sugestoes";
    lista.forEach(function (s) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "cmp-sug";
      b.textContent = s;
      b.addEventListener("click", function () {
        wrap.remove();
        perguntar(s);
      });
      wrap.appendChild(b);
    });
    msgs.appendChild(wrap);
  }

  // --- rede -------------------------------------------------------------
  function garantirSessao() {
    if (sessao) return Promise.resolve(sessao);
    return fetch(API + "/sessao", { method: "POST" })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        sessao = d.sessao;
        localStorage.setItem(CHAVE_SESSAO, sessao);
        return sessao;
      });
  }

  function perguntar(texto) {
    if (ocupado || !texto.trim()) return;
    ocupado = true;
    bolha("usuario", texto);
    var pensando = bolha("assistente", "…");
    garantirSessao()
      .then(function (s) {
        return fetch(API + "/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ sessao: s, mensagem: texto }),
        });
      })
      .then(function (r) {
        if (r.status === 429) throw new Error("Limite desta sessão atingido. Recarregue para começar outra.");
        if (!r.ok) throw new Error("O companion não respondeu (HTTP " + r.status + ").");
        return r.json();
      })
      .then(function (d) {
        pensando.remove();
        bolha("assistente", d.resposta, d.fontes);
      })
      .catch(function (e) {
        pensando.remove();
        bolha("erro", e.message || "Falha de rede. Tente de novo.");
      })
      .finally(function () { ocupado = false; entrada.focus(); });
  }

  // --- eventos ----------------------------------------------------------
  function abrir() {
    painel.hidden = false;
    botao.classList.add("aberto");
    entrada.focus();
    if (msgs.childElementCount === 0) {
      bolha("assistente",
        "Olá. Sou o companion deste livro — respondo sobre o método Maestro citando a " +
        "página. Por onde quer começar?");
      fetch(API + "/sugestoes-de-inicio")
        .then(function (r) { return r.json(); })
        .then(function (d) { sugestoes(d.sugestoes || []); })
        .catch(function () {});
    }
  }

  function fechar() {
    painel.hidden = true;
    botao.classList.remove("aberto");
    botao.focus();
  }

  botao.addEventListener("click", function () { painel.hidden ? abrir() : fechar(); });
  painel.querySelector(".cmp-fechar").addEventListener("click", fechar);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !painel.hidden) fechar();
  });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var t = entrada.value;
    entrada.value = "";
    perguntar(t);
  });
})();
