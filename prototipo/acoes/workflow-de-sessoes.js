/* ============================================================================
   acoes/workflow-de-sessoes.js — os efeitos do contexto Workflow de sessões
   (ciclo 074, T06 — dono do contexto: Worker05)

   Um efeito por ação declarada nos fragmentos do contexto (`telas/workflow-de-sessoes/`).
   O módulo é carregado pela casca porque o ELEMENTO RAIZ de cada fragmento declara
   `data-acoes="acoes/workflow-de-sessoes.js"` (contrato do app.js) — sem o atributo, o
   `data-efeito` continua sendo exibido e este arquivo nunca é buscado.

   Contrato (app.js): `window.Acoes074['workflow-de-sessoes'] = function (botao, estado, api)`.
   `botao` é o elemento clicado; `estado` é o estado em memória (fixtures); `api` oferece
   `api.avisar(texto)`, `api.toast(texto)` e `api.atualizar()`.

   Efeitos, e o que cada um NÃO faz (o protótipo é honesto sobre o limite):

     reiniciar          — a mesma sessão volta com um REF NOVO (`data-alvo`); o antigo deixa
                          de resolver. O efeito é visível na linha e o aviso «o ref muda ao
                          reiniciar» acompanha. Só em memória: recarregar restaura as fixtures.
     derrubar           — a linha do alvo passa a CAÍDA (sem sinal). Nada é apagado de verdade;
                          a confirmação (`data-perde`/`data-reverte`) é da casca, não daqui.
     subir              — a sessão nova entraria na lista com um ref novo (simulado).
     periodo            — o segmento de período da tela de consumo: marca `aria-pressed` na
                          janela escolhida e reconsulta (aqui, reconsulta declarada).
     cancelar-tarefa / reatribuir / abrir-transcript — efeito declarado, simulado.

   Zero dependência externa (FR6). Sem estado global além do necessário; tudo defensivo:
   um alvo que não existe na tela não derruba o módulo — ele declara a ausência.
   ============================================================================ */

(function () {
  'use strict';

  /* O ref novo é derivado do antigo (soma fixa em hexadecimal), para o efeito ser
     determinístico: o mesmo reiniciar dá o mesmo ref — nada de aleatório na evidência. */
  function novoRef(ref) {
    var n = parseInt(ref, 16);
    if (isNaN(n)) { n = 0; }
    n = (n + 0x111111) % 0x1000000;
    var s = n.toString(16);
    while (s.length < 6) { s = '0' + s; }
    return s;
  }

  function refDe(alvo) {
    var achado = String(alvo || '').match(/\[([0-9a-fA-F]{6})\]/);
    return achado ? achado[1] : null;
  }

  function trocarRef(texto, novo) {
    return String(texto || '').replace(/\[[0-9a-fA-F]{6}\]/, '[' + novo + ']');
  }

  /* A linha (`<div class="linha-lista">`) que carrega o alvo. Os botões da linha
     declaram `data-alvo="<nome · ref · projeto>"` — é por ele que a linha se acha. */
  function linhaDe(alvo) {
    var candidatos = document.querySelectorAll('[data-alvo]');
    for (var i = 0; i < candidatos.length; i += 1) {
      if (candidatos[i].getAttribute('data-alvo') === alvo) {
        return candidatos[i].closest ? candidatos[i].closest('.linha-lista') : null;
      }
    }
    return null;
  }

  /* O estado em memória é o das fixtures (app.js): a chave é o agregado do mapa. */
  function sessaoDe(estado, alvo) {
    var lista = estado && estado.sessao && estado.sessao.sessoes;
    if (!lista || !lista.length) { return null; }
    var ref = refDe(alvo);
    for (var i = 0; i < lista.length; i += 1) {
      if (ref && lista[i].ref === ref) { return lista[i]; }
    }
    return null;
  }

  function reiniciar(botao, estado, api) {
    var alvo = botao.getAttribute('data-alvo') || '';
    var linha = linhaDe(alvo);
    var ref = refDe(alvo);
    if (!ref) {
      api.avisar('simulado — reiniciar sem ref no data-alvo: a tela não sabe qual endereço trocar ' +
        '(motivo: o botão não declara «nome · ref · projeto»)');
      return;
    }
    var novo = novoRef(ref);
    if (linha) {
      var titulo = linha.querySelector('.titulo');
      if (titulo) { titulo.textContent = trocarRef(titulo.textContent, novo); }
      linha.setAttribute('data-ref', novo);
      var nota = linha.querySelector('.fonte');
      if (nota) {
        nota.textContent = 'reiniciada (exemplo) — o ref novo é [' + novo +
          ']; o endereço [' + ref + '] deixou de resolver (aviso: o ref muda ao reiniciar).';
      }
    }
    var sessao = sessaoDe(estado, alvo);
    if (sessao) { sessao.ref = novo; sessao.ref_anterior = ref; sessao.estado = 'esperando'; }
    api.avisar('simulado — reiniciar: o ref muda ao reiniciar — de [' + ref + '] para [' + novo +
      ']; mensagens endereçadas ao ref antigo não chegam (exemplo).');
  }

  function derrubar(botao, estado, api) {
    var alvo = botao.getAttribute('data-alvo') || '';
    var linha = linhaDe(alvo);
    if (linha) {
      linha.classList.add('linha-caida');
      var ponto = linha.querySelector('.ponto');
      if (ponto) {
        ponto.className = 'ponto ponto-sem-sinal';
        ponto.setAttribute('aria-hidden', 'true');
      }
      var subtitulo = linha.querySelector('.subtitulo');
      if (subtitulo) {
        subtitulo.textContent = 'caída · sem sinal — o processo não responde e não pode ser acordado (exemplo)';
      }
    }
    var sessao = sessaoDe(estado, alvo);
    if (sessao) { sessao.estado = 'caída'; }
    api.avisar('simulado — derrubar: a linha de ' + (alvo || 'a sessão alvo') +
      ' passou a caída (sem sinal); o contexto vivo da sessão se perdeu (exemplo).');
  }

  function periodo(botao, api) {
    var escolhida = botao.getAttribute('data-periodo') || '';
    var segmento = botao.closest ? botao.closest('.segmento') : null;
    if (segmento) {
      var botoes = segmento.querySelectorAll('button');
      for (var i = 0; i < botoes.length; i += 1) {
        botoes[i].setAttribute('aria-pressed',
          botoes[i] === botao ? 'true' : 'false');
      }
    }
    api.avisar('simulado — janela do consumo: «' + escolhida +
      '»; os saldos são reconsultados no read-model e todo valor segue estimado (piso) (exemplo).');
  }

  window.Acoes074 = window.Acoes074 || {};
  window.Acoes074['workflow-de-sessoes'] = function (botao, estado, api) {
    if (!botao || !botao.getAttribute) { return; }
    var acao = (botao.getAttribute('data-acao') || '').trim().toLowerCase();
    var efeito = botao.getAttribute('data-efeito') || 'o efeito declarado no botão';
    switch (acao) {
      case 'reiniciar':
        reiniciar(botao, estado, api);
        return;
      case 'derrubar':
        derrubar(botao, estado, api);
        return;
      case 'subir':
        api.avisar('simulado — subir: a sessão nova entra na lista com um ref novo ' +
          '(as fixtures não ganham linha nova em memória; ' + efeito + ') (exemplo)');
        return;
      case 'periodo':
        periodo(botao, api);
        return;
      default:
        /* reatribuir, cancelar-tarefa, abrir-transcript e qualquer ação declarada depois:
           o efeito é o declarado no próprio botão — a casca já o anuncia no toast. */
        api.avisar('simulado — ' + efeito + ' (exemplo)');
    }
  };
})();
