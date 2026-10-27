/* ============================================================================
   acoes/regencia.js — efeitos do contexto `regencia` (ciclo 074, T03 · FR4)

   Dono: Worker01 (T03). Fronteira: a casca (`app.js`, do Worker02) é quem roteia e quem
   chama este módulo; aqui vivem SÓ os efeitos declarados nos fragmentos da Regência.

   Contrato da casca (ver o cabeçalho de `app.js`):

     window.Acoes074['regencia'] = function (botao, estado, api) { ... };

   - `botao` é o elemento clicado (com `data-acao`, `data-efeito`, …);
   - `estado` é o estado em memória — as chaves são os oito agregados das fixtures;
   - `api.avisar(texto)` mostra o aviso de simulação, `api.toast(texto)` o toast e
     `api.atualizar()` recarrega o fragmento da rota corrente.

   Regra do protótipo (ux-design 074 §0): SIMULAR NÃO É AUTORIZAR. Todo efeito é só em
   memória — recarregar restaura as fixtures (FR4). As ações:

   - `escolher-opcao` — o chip da opção escolhida fica ativo (--primaria); a resposta passa
     a ser a escolhida (J1 passo 4);
   - `registrar-ruling` — o pedido sai da fila de decisões, o contador de decisões da
     frase-chave recua e o pedido marcado como respondido na tela (J1 passos 5–6).

   Nenhuma tela é conhecida aqui por nome: os ganchos são os atributos das fixtures e do
   próprio fragmento (`[data-pedido]`, `[data-opcoes]`, `[data-contador-decisoes]`).
   ============================================================================ */

(function () {
  'use strict';

  function limparIrmaos(pai) {
    if (!pai) { return; }
    Array.prototype.forEach.call(pai.querySelectorAll('.chip'), function (outro) {
      outro.classList.remove('chip-ativo');
      outro.setAttribute('aria-pressed', 'false');
    });
  }

  function escolherOpcao(botao, estado) {
    limparIrmaos(botao.parentNode);
    botao.classList.add('chip-ativo');
    botao.setAttribute('aria-pressed', 'true');
    var pedido = botao.getAttribute('data-pedido') || '';
    estado.ruling = { pedido: pedido, opcao: botao.getAttribute('data-opcao') || '' };
    return pedido;
  }

  function registrarRuling(botao, estado, api) {
    var pedido = botao.getAttribute('data-pedido') || '';
    estado.rulings = estado.rulings || {};
    estado.rulings[pedido] = {
      opcao: (estado.ruling && estado.ruling.opcao) || null,
      registrado: 'simulado (exemplo)'
    };

    /* O pedido responde não volta a esperar: a fila perde uma decisão pendente. */
    var respondidos = Object.keys(estado.rulings).length;
    estado.decisoesPendentes = Math.max(0, 3 - respondidos);

    /* Efeito na tela: o pedido marcado como respondido (quando ele está nesta tela)… */
    var cartao = pedido ? document.querySelector('[data-pedido="' + pedido + '"]') : null;
    if (cartao) {
      cartao.setAttribute('data-respondido', 'sim');
      cartao.classList.add('vazio');
    }

    /* …e os contadores de decisões da frase-chave recuam, onde quer que estejam. */
    Array.prototype.forEach.call(document.querySelectorAll('[data-contador-decisoes]'), function (el) {
      var n = parseInt(el.getAttribute('data-contador-decisoes'), 10);
      if (!isNaN(n) && n > 0) {
        el.setAttribute('data-contador-decisoes', String(n - 1));
        el.textContent = String(n - 1);
      }
    });

    var saida = document.getElementById('saida-ruling');
    if (saida) {
      saida.hidden = false;
      saida.textContent = 'ruling registrado para ' + (pedido || 'o pedido') +
        ' (exemplo) — o pedido saiu da fila de decisões e o contador da frase-chave passa a ' +
        estado.decisoesPendentes + ' ao voltar à tela inicial';
    }
    api.avisar('simulado — o ruling de ' + (pedido || 'o pedido') +
      ' entrou no livro de mensagens; recarregar restaura as fixtures (exemplo)');
  }

  window.Acoes074 = window.Acoes074 || {};

  window.Acoes074['regencia'] = function (botao, estado, api) {
    var acao = (botao.getAttribute('data-acao') || '').trim();
    if (acao === 'escolher-opcao') {
      var pedido = escolherOpcao(botao, estado);
      api.avisar('simulado — a opção escolhida vale para o pedido ' + (pedido || '') +
        '; recarregar restaura as fixtures (exemplo)');
      return;
    }
    if (acao === 'registrar-ruling') {
      registrarRuling(botao, estado, api);
      return;
    }
    /* Uma ação declarada neste contexto que este módulo ainda não cobre: o efeito de
       `data-efeito` continua sendo exibido pela casca — a ausência é declarada, nunca
       silenciada (mesma disciplina da casca com o módulo ausente). */
    api.avisar('simulado — "' + acao + '" declarada no fragmento; o efeito é o de data-efeito ' +
      '(exemplo); recarregar restaura as fixtures');
  };
})();
