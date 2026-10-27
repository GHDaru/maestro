/* ============================================================================
   acoes/mensageria.js — efeitos do contexto Mensageria (ciclo 074, T04)

   Contrato do módulo (ver o cabeçalho de `app.js`):

     window.Acoes074 = window.Acoes074 || {};
     window.Acoes074['mensageria'] = function (botao, estado, api) { ... };

   A casca só carrega este arquivo porque o fragmento o declara no elemento raiz
   (`data-acoes="acoes/mensageria.js"`); sem o atributo, o efeito declarado em
   `data-efeito` continua sendo exibido e este módulo não entra.

   Duas ações, as da jornada J5 do `ux-design.md` §3:

   - `drenar-outbox`  (J5 passo 2) — a leitura das mensagens não lidas é fechada
     (`lida_em`), os pontos somem e o contador de não lidas zera. A linha drenada
     NÃO sai da lista: a fila (outbox) é drenada, nunca esvaziada (append-only),
     e a mensagem permanece no livro de mensagens.
   - `enviar-endereco-ambiguo` (J5 passos 4–5) — a confirmação irreversível é
     aberta pela casca (o motor de B-UX1); o clique de confirmação chega aqui e
     revela a RECUSA com o pedido de desambiguação: a resolução é só pelo ref
     (`nome · ref · projeto`), nunca "o mais provável" (mapa §7.1).

   Todas as ações são SIMULADAS e só em memória: nada é escrito em disco — o
   `estado` é o das fixtures e recarregar a página restaura (FR4). Nenhum dado
   pessoal real; refs do roster de exemplo do 073.
   ============================================================================ */

(function () {
  'use strict';

  window.Acoes074 = window.Acoes074 || {};

  /* A mensagem do agregado `mensagem` pelo id da linha (`data-mensagem`). */
  function mensagemPorId(estado, id) {
    var agregado = estado && estado.mensagem;
    var lista = agregado && agregado.mensagens ? agregado.mensagens : [];
    for (var i = 0; i < lista.length; i++) {
      if (String(lista[i].id) === String(id)) { return lista[i]; }
    }
    return null;
  }

  /* Fecha a leitura de uma linha: grava `lida_em` em memória e ajusta o DOM
     (o ponto de não lida some; a linha passa a lida). */
  function fecharLeitura(linha, estado) {
    var mensagem = mensagemPorId(estado, linha.getAttribute('data-mensagem'));
    if (mensagem && !mensagem.lida_em) {
      mensagem.lida_em = new Date().toISOString();
    }
    linha.classList.remove('mensagem-nao-lida');
    linha.classList.add('mensagem-lida');
    var ponto = linha.querySelector('.ponto');
    if (ponto && ponto.parentNode) { ponto.parentNode.removeChild(ponto); }
    /* a célula do estado da leitura acompanha: a linha passa a "lida" */
    var celula = linha.querySelector('[data-estado-leitura]');
    if (celula) { celula.textContent = 'lida (exemplo)'; }
  }

  function drenarOutbox(estado) {
    var linhas = document.querySelectorAll('[data-mensagem]');
    for (var i = 0; i < linhas.length; i++) { fecharLeitura(linhas[i], estado); }
    var contador = document.querySelector('[data-contador-nao-lidas]');
    if (contador) { contador.textContent = '0 não lidas (exemplo)'; }
    var nota = document.querySelector('[data-nota-drenagem]');
    if (nota) { nota.hidden = false; }
  }

  function enviarEnderecoAmbiguo() {
    var recusa = document.querySelector('[data-recusa-ambiguo]');
    if (recusa) { recusa.hidden = false; }
  }

  /* As três chamadas MCP do protocolo (leitura/escrita governadas pela política
     de escopo `ferramenta MCP`): mostram um retorno SIMULADO — nenhuma escrita,
     nenhuma resposta que a fixture não tenha. Nunca um botão que finge. */
  function retornoFerramenta(acao) {
    var caixa = document.querySelector('[data-retorno-ferramenta]');
    if (!caixa) { return; }
    var retornos = {
      'chamar-estado-atual': 'estado_atual (simulado): a equipe, as decisões e a barra viriam da fixture — nada é escrito.',
      'registrar-status': 'registrar_status (simulado): acrescenta o status da sessão dona — só acrescenta, nunca reescreve.',
      'registrar-peca': 'registrar_peca (simulado): recusaria a transição sem a evidência exigida pelo portão do chamado.'
    };
    if (retornos[acao]) {
      caixa.textContent = retornos[acao];
      caixa.hidden = false;
    }
  }

  window.Acoes074['mensageria'] = function (botao, estado, api) {
    var acao = (botao && botao.getAttribute('data-acao')) || '';
    if (acao === 'drenar-outbox') { drenarOutbox(estado || {}); return; }
    if (acao === 'enviar-endereco-ambiguo') { enviarEnderecoAmbiguo(); return; }
    if (acao === 'chamar-estado-atual' || acao === 'registrar-status'
        || acao === 'registrar-peca') { retornoFerramenta(acao); return; }
  };
})();
