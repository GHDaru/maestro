/* ============================================================================
   acoes/chamados-e-gates.js — efeitos do contexto `chamados-e-gates` (ciclo 074, T03 · FR4)

   Dono: Worker01 (T03). Contexto core domain (B1): a tela é SÓ LEITURA — ela não promove e
   não decide (anti-regra 1 do 066); as duas ações aqui são declaradamente simuladas e mudam
   só a VISÃO da tela, nunca o estado de um chamado:

   - `filtrar-frente` — só os cartões da frente escolhida ficam visíveis (J2 passo 2);
   - `detalhar` — o painel de detalhe abre na própria tela (expansão, B-UX2: o veredito
     normalizado e o original ao lado — J2 passo 3).

   Contrato da casca (ver `app.js`):

     window.Acoes074['chamados-e-gates'] = function (botao, estado, api) { ... };

   Efeito só em memória/DOM: recarregar restaura as fixtures (FR4).
   ============================================================================ */

(function () {
  'use strict';

  function filtrarFrente(botao, api) {
    var frente = botao.getAttribute('data-frente') || '';

    Array.prototype.forEach.call(
      document.querySelectorAll('[data-acao="filtrar-frente"]'),
      function (chip) {
        var ativo = chip === botao;
        chip.classList.toggle('chip-ativo', ativo);
        chip.setAttribute('aria-pressed', ativo ? 'true' : 'false');
      });

    var visiveis = 0;
    Array.prototype.forEach.call(document.querySelectorAll('[data-chamado]'), function (cartao) {
      var mostra = !frente || cartao.getAttribute('data-frente') === frente;
      cartao.hidden = !mostra;
      if (mostra) { visiveis += 1; }
    });

    api.avisar('simulado — filtro por frente: ' + (frente || 'todas as frentes') + ' · ' +
      visiveis + ' cartão(ões) visível(is); recarregar restaura as fixtures (exemplo)');
  }

  function detalhar(botao, api) {
    var id = botao.getAttribute('data-detalhe') || botao.getAttribute('data-chamado') || '';
    var painel = id ? document.getElementById('detalhe-' + id) : null;
    if (!painel) {
      api.avisar('— o detalhe do chamado ' + (id || '(sem id)') +
        ' não existe nesta tela (motivo: o fragmento não o traz)');
      return;
    }
    painel.hidden = !painel.hidden;
    botao.setAttribute('aria-expanded', painel.hidden ? 'false' : 'true');
    api.avisar('simulado — detalhe ' + (painel.hidden ? 'fechado' : 'aberto') +
      ': veredito normalizado e o original ao lado (exemplo); recarregar restaura as fixtures');
  }

  window.Acoes074 = window.Acoes074 || {};

  window.Acoes074['chamados-e-gates'] = function (botao, estado, api) {
    var acao = (botao.getAttribute('data-acao') || '').trim();
    if (acao === 'filtrar-frente') { filtrarFrente(botao, api); return; }
    if (acao === 'detalhar') { detalhar(botao, api); return; }
    /* Ação declarada que este módulo ainda não cobre: o efeito de `data-efeito` continua
       sendo exibido pela casca — a ausência é declarada, nunca silenciada. */
    api.avisar('simulado — "' + acao + '" declarada no fragmento; o efeito é o de data-efeito ' +
      '(exemplo); recarregar restaura as fixtures');
  };
})();
