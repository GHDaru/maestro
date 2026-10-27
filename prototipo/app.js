/* ============================================================================
   app.js — a casca do protótipo navegável do painel de regência (ciclo 074, T02)

   Três coisas, e só: o ROTEADOR (`#/<contexto>/<tela>` → fragmento), o ESTADO em
   memória (inicializado das fixtures; recarregar restaura) e o MOTOR DE AÇÕES
   (botão de escrita → efeito declarado, simulado e visível).

   Fronteira do Worker02: os EFEITOS por contexto vivem em `acoes/<contexto>.js`,
   um arquivo por dono — este arquivo não conhece nenhuma tela. Contrato do módulo:

     window.Acoes074 = window.Acoes074 || {};
     window.Acoes074['<contexto>'] = function (botao, estado, api) { ... };

   - `<contexto>` é um dos cinco do mapa (FR2/B1);
   - `botao` é o elemento clicado (com `data-acao`, `data-efeito`, …);
   - `estado` é o estado em memória — as chaves são os oito agregados do mapa;
   - `api` oferece `api.avisar(texto)`, `api.toast(texto)` e `api.atualizar()`
     (recarrega o fragmento da rota corrente).

   Carregamento do módulo: o FRAGMENTO declara o seu, no elemento raiz —
   `data-acoes="acoes/<contexto>.js"`. A casca busca só o que foi declarado, nunca
   adivinha o caminho: procurar um arquivo que ainda não existe deixaria um 404 de
   subrecurso no console (é assim que o harness da T02 achou o defeito). Sem o atributo,
   o contexto simplesmente não tem efeitos próprios — o efeito declarado em
   `data-efeito` continua sendo exibido.

   Motor de ações (B-UX1). Todo botão de escrita — `<button>`/`<form>`/`[role=button]`
   sem `href="#/…"` e sem `data-vai-para` (definição fixa do ux-design 074 §5) —
   produz o efeito declarado em `data-efeito`, com aviso de simulação. O botão
   irreversível declara `data-irreversivel="sim"` e `data-confirma="<id>"`: o primeiro
   clique ABRE a confirmação (o elemento de `<id>`, que carrega `data-perde` e
   `data-reverte`); com ela aberta, o clique seguinte EXECUTA o efeito e fecha. É o
   mesmo par de atributos que a verificação (i) cobra — e sem o elemento de `<id>` o
   motor não inventa confirmação: declara a ausência.

   Zero dependência externa (FR6): nenhuma rede, nenhum framework, nenhum build. Este
   arquivo é servido por `python -m http.server` na própria pasta.
   ============================================================================ */

(function () {
  'use strict';

  /* Os cinco contextos do mapa de contextos delimitados (FR2/B1). A verificação (d) do
     `verifica-navegacao.py` aceita exatamente estes cinco valores. */
  var CONTEXTOS = ['chamados-e-gates', 'regencia', 'workflow-de-sessoes', 'administracao', 'mensageria'];

  /* A tela inicial (FR1) — destino de toda rota desconhecida. */
  var INICIAL = 'regencia/inicial';

  /* Um JSON por agregado do mapa (FR5). O contrato dos campos é
     `specs/074-prototipo-navegavel/data-model.md`. */
  var AGREGADOS = ['sessao', 'tarefa', 'chamado', 'pedido-de-decisao', 'mensagem', 'politica', 'orcamento', 'catalogo'];

  /* PROVISÓRIO (gate de UX 074): quebra da navegação — 768px. NÃO é variável consumível em
     @media (o valor literal está na media query de `tokens.css`); a forma (lateral acima,
     barra inferior abaixo) é do CSS. A captura do build real a 360px na jornada viva
     confirma ou move a constante, no mesmo commit. Aqui ela é declarada para o roteador
     poder dizer em que forma está. */
  var QUEBRA_NAVEGACAO = 768;

  /* ---------------------------------------------------------------- estado --- */

  var estado = {
    projeto: 'maestro',   // o valor de repos[0].nome de painel/projetos/exemplo.json (S6)
    carregadas: 0,
    ausentes: [],
    _fonte: 'prototipo/fixtures/*.json (um JSON por agregado do mapa)'
  };

  /* ------------------------------------------------------------------- api --- */

  var api = {
    avisar: avisarSimulacao,
    toast: mostrarToast,
    atualizar: function () { return navegar(); }
  };

  /* --------------------------------------------------------------- fixtures --- */

  function carregarFixtures() {
    var pedidos = AGREGADOS.map(function (nome) {
      return fetch('fixtures/' + nome + '.json', { cache: 'no-store' })
        .then(function (resposta) {
          if (!resposta.ok) { throw new Error('sem o arquivo'); }
          return resposta.json().then(function (dados) {
            estado[nome] = dados;
            estado.carregadas += 1;
          });
        })
        .catch(function () {
          /* Ausência é informação declarada, nunca valor padrão (regra F8 do 066): o
             agregado fica nulo e o motivo aparece na tela — e o console fica limpo. */
          estado[nome] = null;
          estado.ausentes.push(nome);
        });
    });
    return Promise.all(pedidos).then(declararFixtures);
  }

  function declararFixtures() {
    var alvo = document.getElementById('fixtures');
    if (!alvo) { return; }
    if (estado.ausentes.length === 0) {
      alvo.textContent = 'fixtures: ' + estado.carregadas + ' de ' + AGREGADOS.length +
        ' carregadas (exemplo) · fonte: ' + estado._fonte;
      return;
    }
    alvo.textContent = 'fixtures: ' + estado.carregadas + ' de ' + AGREGADOS.length +
      ' carregadas · — sem o arquivo: ' + estado.ausentes.join(', ') +
      ' (motivo: o agregado ainda não pousou nesta base; o caminho é fixtures/<agregado>.json)';
  }

  /* -------------------------------------------------------------- roteador --- */

  /* A rota BRUTA é o que está na barra de endereço — inclusive uma rota que não existe.
     É ela que o aviso da FR1 cita; `rotaDaBarra` devolve nulo justamente quando a rota é
     desconhecida, e era daí que vinha a queda na inicial SEM declarar o motivo. */
  function rotaBruta() {
    return (location.hash || '').replace(/^#\/?/, '').replace(/\/+$/, '').trim();
  }

  function rotaDaBarra() {
    var partes = rotaBruta().split('/').filter(Boolean);
    if (partes.length === 2 && CONTEXTOS.indexOf(partes[0]) !== -1) { return partes.join('/'); }
    return null;   // rota desconhecida: quem decide é `navegar` (FR1: cai na inicial, sem erro)
  }

  function contextoDaRota(rota) {
    return rota.split('/')[0];
  }

  function lerFragmento(rota) {
    return fetch('telas/' + rota + '.html', { cache: 'no-store' })
      .then(function (resposta) { return resposta.ok ? resposta.text() : null; })
      .catch(function () { return null; });
  }

  function navegar() {
    var bruta = rotaBruta();
    var pedida = rotaDaBarra();
    marcarMenu(pedida);
    return resolver(pedida || INICIAL, bruta).then(function (resultado) {
      var alvo = document.getElementById('tela');
      if (!alvo) { return resultado.rota; }
      alvo.innerHTML = resultado.html;
      alvo.setAttribute('data-contexto', contextoDaRota(resultado.rota));
      alvo.setAttribute('data-rota', resultado.rota);
      /* FR1 declarado na tela: a rota pedida não existe (ou o fragmento ainda não pousou) e
         a casca caiu na tela inicial — sem erro, e dizendo por quê. */
      if (bruta && bruta !== resultado.rota) {
        alvo.insertAdjacentHTML('afterbegin',
          '<p class="aviso-simulacao" data-referencia="true">rota <code>#/' + escapar(bruta) +
          '</code> não existe nesta base — a casca caiu na tela inicial sem erro (FR1).</p>');
      }
      carregarModulos(alvo);
      window.scrollTo(0, 0);
      return resultado.rota;
    });
  }

  /* Resolve a rota: o fragmento pedido; se ele ainda não existe (entregas T03–T06) ou a
     rota é desconhecida, a tela inicial (FR1); e, se nem ela existe, uma casca declarada —
     nunca um erro, nunca uma tela inventada. */
  function resolver(rota, pedida) {
    return lerFragmento(rota).then(function (html) {
      if (html !== null) { return { rota: rota, html: html }; }
      if (rota === INICIAL) { return { rota: rota, html: cascaSemFragmento(pedida || rota) }; }
      return lerFragmento(INICIAL).then(function (inicial) {
        return {
          rota: INICIAL,
          html: inicial !== null ? inicial : cascaSemFragmento(pedida || rota)
        };
      });
    });
  }

  /* A rota vem da barra de endereço — entra no DOM por innerHTML, então é escapada.
     Sem isto, uma rota com `<` ou aspas injetaria marcação na tela. */
  function escapar(texto) {
    return String(texto === null || texto === undefined ? '' : texto)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function cascaSemFragmento(pedida) {
    return '<div class="conteudo-interior">' +
      '<p class="migalha" data-referencia="true">Maestro · protótipo navegável · ciclo 074</p>' +
      '<h1 class="titulo-pagina">Tela inicial — o fragmento ainda não pousou</h1>' +
      '<p class="vazio">— o fragmento <code>telas/' + INICIAL + '.html</code> não existe nesta base ' +
      '(motivo: é entrega da T03 do ciclo 074). A casca não inventa tela: declara o caminho e espera.</p>' +
      '<p class="ajuda">Rota pedida: <code>#/' + escapar(pedida || INICIAL) + '</code> · ' +
      'contexto: <code>' + contextoDaRota(INICIAL) + '</code></p>' +
      '</div>';
  }

  function marcarMenu(pedida) {
    var itens = document.querySelectorAll('#menu a');
    var aceso = false;
    Array.prototype.forEach.call(itens, function (item) {
      var casa = (item.getAttribute('href') || '') === '#/' + pedida;
      item.setAttribute('aria-current', casa ? 'page' : 'false');
      aceso = aceso || casa;
    });
    if (!aceso && itens.length) { itens[0].setAttribute('aria-current', 'page'); }
  }

  /* -------------------------------------------------------------- módulos --- */

  var modulosCarregados = {};

  /* Os efeitos por contexto são de quem é dono do contexto (T03–T06). O fragmento declara
     o seu módulo no elemento raiz; a casca não adivinha o caminho (ver o cabeçalho). */
  function carregarModulos(raiz) {
    var declaracao = raiz ? raiz.querySelector('[data-acoes]') : null;
    if (!declaracao) { return; }
    var url = (declaracao.getAttribute('data-acoes') || '').trim();
    if (!url || modulosCarregados[url]) { return; }
    modulosCarregados[url] = true;
    var script = document.createElement('script');
    script.src = url;
    /* Um módulo declarado e ausente é defeito do fragmento, não da casca — e é declarado,
       nunca silenciado (e nunca um erro de console inventado por nós). */
    script.onerror = function () {
      avisarSimulacao('— o módulo declarado em data-acoes="' + url +
        '" não existe nesta base (motivo: é entrega do dono do contexto)');
    };
    document.head.appendChild(script);
  }

  /* ---------------------------------------------------------------- ações --- */

  /* A confirmação irreversível carrega os dois atributos que a verificação (i) cobra. */
  function temPerdeEReverte(confirmacao) {
    return !!confirmacao.querySelector('[data-perde]') && !!confirmacao.querySelector('[data-reverte]');
  }

  function ehBotaoDeEscrita(el) {
    if (!el || !el.matches) { return false; }
    if (!el.matches('button, form, [role="button"]')) { return false; }
    if (el.hasAttribute('href') || el.hasAttribute('data-vai-para')) { return false; }
    return true;
  }

  function tratarClique(evento) {
    var alvo = evento.target.closest ? evento.target.closest('[data-acao], [data-irreversivel="sim"]') : null;
    if (!alvo) { return; }

    /* B-UX1: o botão irreversível abre a confirmação; com ela aberta, o clique seguinte
       executa o efeito e fecha. */
    if (alvo.getAttribute('data-irreversivel') === 'sim' && alvo.hasAttribute('data-confirma')) {
      var confirmacao = document.getElementById(alvo.getAttribute('data-confirma'));
      if (!confirmacao) {
        /* A verificação (i) acusa a confirmação que não existe; o motor não a inventa. */
        avisarSimulacao('— confirmação declarada em data-confirma="' +
          alvo.getAttribute('data-confirma') + '" não existe nesta tela (motivo: o fragmento não a traz)');
        return;
      }
      if (confirmacao.hidden) {
        evento.preventDefault();
        confirmacao.hidden = false;
        confirmacao.setAttribute('data-aberta', 'sim');
        avisarSimulacao('ação irreversível: confirme para seguir — ' +
          (temPerdeEReverte(confirmacao)
            ? 'o que se perde e como reverter estão declarados na confirmação'
            : '— a confirmação não declara data-perde/data-reverte (motivo: o fragmento não os traz)'));
        return;
      }
      confirmacao.hidden = true;
      confirmacao.removeAttribute('data-aberta');
      executar(alvo);
      return;
    }

    if (ehBotaoDeEscrita(alvo)) {
      evento.preventDefault();
      executar(alvo);
    }
  }

  function executar(botao) {
    var efeito = botao.getAttribute('data-efeito') || 'o efeito declarado no botão';
    var tela = document.getElementById('tela');
    var contexto = tela ? tela.getAttribute('data-contexto') : null;
    var modulo = window.Acoes074 && contexto ? window.Acoes074[contexto] : null;

    if (typeof modulo === 'function') {
      modulo(botao, estado, api);
    }
    mostrarToast('simulado — ' + efeito);
    avisarSimulacao('simulado — recarregar restaura as fixtures (exemplo)');
  }

  /* -------------------------------------------------------------- avisos --- */

  var relogioAviso = null;
  var relogioToast = null;

  function avisarSimulacao(texto) {
    var alvo = document.getElementById('aviso-simulacao');
    if (!alvo) { return; }
    alvo.textContent = texto;
    alvo.hidden = false;
    window.clearTimeout(relogioAviso);
    relogioAviso = window.setTimeout(function () { alvo.hidden = true; }, 6000);
  }

  function mostrarToast(texto) {
    var alvo = document.getElementById('toast');
    if (!alvo) { return; }
    alvo.textContent = texto;
    alvo.hidden = false;
    window.clearTimeout(relogioToast);
    relogioToast = window.setTimeout(function () { alvo.hidden = true; }, 4000);
  }

  /* --------------------------------------------------------------- arranque --- */

  document.addEventListener('click', tratarClique);
  window.addEventListener('hashchange', navegar);

  carregarFixtures().then(function () {
    return navegar();
  }).then(function () {
    /* Superfície declarada para o verificador e para quem andar de fora: o estado em
       memória e o roteador, sem tocar no DOM de ninguém. */
    window.Prototipo074 = {
      estado: estado,
      contextos: CONTEXTOS.slice(),
      quebraNavegacao: QUEBRA_NAVEGACAO,
      rotaDaBarra: rotaDaBarra,
      navegar: navegar,
      inicial: INICIAL
    };
  });
})();
