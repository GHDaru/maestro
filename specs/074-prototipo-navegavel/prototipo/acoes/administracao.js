/* ============================================================================
   acoes/administracao.js — os efeitos de clique do contexto ADMINISTRAÇÃO (ciclo 074, fatia T05).

   Fronteira do Worker04 (T05). Este arquivo conhece SÓ as telas da Administração
   (catalogo.html · politicas.html · orcamento.html); o motor da casca está em app.js,
   que é do Worker02, e não é tocado aqui. Contrato do módulo (app.js, cabeçalho):

     window.Acoes074 = window.Acoes074 || {};
     window.Acoes074['administracao'] = function (botao, estado, api) { ... };

   O fragmento declara o módulo no elemento raiz (`data-acoes="acoes/administracao.js"`);
   sem o atributo, o efeito de `data-efeito` ainda aparece, mas este módulo não carrega.

   O que este módulo faz — e só isso:
     · "Propor regra"  (ask)  — a proposta VIRA pedido de decisão (propor NÃO executa) e o
                                link "ver na fila" aparece. O toast "simulado — …" e o aviso
                                de simulação são do motor (app.js), não daqui.
     · "Ajustar teto"         — a barra de consumo recalcula contra o teto novo, muda de cor
                                pela faixa e o histórico ganha uma linha nova (changed_by).
     · "estourar-teto" (irreversível) — a barra vai à faixa estourada (--erro) e o aviso do
                                medidor é endereçado à fila outbox (agregado `mensagem`).

   As demais ações das telas (abrir ficha/regra/perfil/modelo/mudança/teto) são de LEITURA:
   o efeito declarado em `data-efeito` já é exibido pelo motor, e não há estado a mudar —
   por isso não entram neste switch. Efeitos são SÓ em memória (FR4): recarregar a página
   restaura as fixtures. Nada aqui chama api.atualizar() — ele recarregaria o fragmento do
   disco e desfaria, em tela, o que a simulação acabou de mostrar.
   ============================================================================ */
(function () {
  'use strict';

  /* Faixas da barra de consumo (data-model 074 §7 · design-system §4):
     até 80 % → normal (--grafico-2) · de 80 % a 100 % → atenção (--primaria) · acima de 100 %
     → estourada (--erro). As classes são as de tokens.css. */
  var FAIXA_ATENCAO = 80;
  var FAIXA_ESTOURADA = 100;

  /* O "estourar" simulado leva o consumo um pouco acima do teto — o suficiente para a barra
     cair na faixa estourada e o aviso do medidor ser endereçado à fila outbox. */
  var MARGEM_ESTOURO = 2;   /* por cento acima do teto */

  window.Acoes074 = window.Acoes074 || {};

  window.Acoes074['administracao'] = function (botao, estado, api) {
    var acao = (botao.getAttribute('data-acao') || '').trim();
    if (acao === 'propor-regra') { proporRegra(estado, api); return; }
    if (acao === 'ajustar-teto') { ajustarTeto(estado, api); return; }
    if (acao === 'estourar-teto') { estourarTeto(estado, api); return; }
    /* Leitura: o motor já mostrou o efeito declarado em `data-efeito`. */
  };

  /* -------------------------------------------------------- Propor regra (ask) --- */

  /* A proposta vira PEDIDO DE DECISÃO — ela entra na fila de decisões e não muda a política.
     O pedido é acrescentado ao agregado `pedido-de-decisao` (em memória) e o link "ver na fila"
     aparece; a fila de decisões é `#/regencia/fila-de-decisoes`. */
  function proporRegra(estado, api) {
    var agregado = estado['pedido-de-decisao'];
    var pedido = {
      id: 'D-novo',
      pedido_por: 'Administração — proposta de regra (exemplo)',
      pergunta: 'declarar a regra proposta na política do projeto maestro? (exemplo)',
      opcoes: [
        { id: 'a', descricao: 'aprovar a regra proposta (exemplo)' },
        { id: 'b', descricao: 'adiar até a auditoria administrativa (exemplo)' }
      ],
      recomendacao: 'quem decide é o humano — propor não executa (exemplo)',
      destino: 'Gerente [31ee4d] · maestro',
      status: 'aguardando',
      rulings: []
    };

    if (agregado && Array.isArray(agregado.pedidos)) {
      agregado.pedidos.push(pedido);
    } else {
      estado['pedido-de-decisao'] = { projeto: 'maestro', pedidos: [pedido] };
    }

    var caixa = document.getElementById('efeito-propor-regra');
    var texto = document.getElementById('efeito-propor-regra-texto');
    var link = document.getElementById('efeito-propor-regra-link');
    if (texto) {
      texto.innerHTML = 'a proposta <strong>virou pedido de decisão</strong>: propor não executa — ela ' +
        'espera na fila de decisões, e quem decide é o humano (<em>exemplo</em>).';
    }
    if (link) {
      link.innerHTML = '<a href="#/regencia/fila-de-decisoes" ' +
        'data-fonte="fila de decisões do contexto de Regência (entrega da T03, rota #/regencia/fila-de-decisoes)">' +
        'ver na fila</a>';
    }
    if (caixa) { caixa.hidden = false; }

    api.avisar('simulado — a proposta virou pedido de decisão (propor não executa); ' +
      'recarregar restaura as fixtures (exemplo)');
  }

  /* ---------------------------------------------------------- Ajustar teto --- */

  /* Recalcula consumo ÷ teto contra o teto novo, pinta a barra pela faixa e acrescenta uma
     linha ao histórico de mudanças com o autor (`changed_by`). Não executa nada fora da
     memória: o teto novo vive em `estado.orcamento.teto`. */
  function ajustarTeto(estado, api) {
    var campo = document.getElementById('novo-teto');
    var digitado = campo ? String(campo.value || '').replace(/[^0-9]/g, '') : '';
    var novoTeto = parseInt(digitado, 10);

    if (!novoTeto || novoTeto <= 0) {
      api.avisar('— o teto novo não foi informado (motivo: o campo "novo teto" está vazio; ' +
        'sem número não há recálculo)');
      return;
    }

    var orcamento = estado['orcamento'];
    if (!orcamento || typeof orcamento !== 'object') {
      api.avisar('— sem o agregado orcamento (motivo: fixtures/orcamento.json não pousou nesta base)');
      return;
    }

    var consumo = Number(orcamento.consumo) || 0;
    orcamento.teto = novoTeto;

    var porcentagem = Math.round((consumo / novoTeto) * 100);
    pintarBarra(porcentagem);
    atualizarNumeros(consumo, novoTeto, porcentagem);
    acrescentarHistorico(
      'teto ajustado para ' + formatar(novoTeto) + ' tokens/mês (exemplo)',
      'Ana Exemplo',
      'teto do projeto maestro'
    );

    api.avisar('simulado — a barra recalcula contra o teto novo (' + porcentagem +
      ' %) e o histórico ganha a linha com changed_by: Ana Exemplo (exemplo)');
  }

  /* -------------------------------------------------------- Estourar o teto (irreversível) --- */

  /* A ação irreversível (ux-design 074 §5): o consumo passa a apontar acima do teto, a barra
     vai à faixa estourada e o aviso do medidor (painel/custo.py, D3) é endereçado à fila
     outbox. A confirmação com `data-perde`/`data-reverte` é aberta pelo motor (B-UX1). */
  function estourarTeto(estado, api) {
    var orcamento = estado['orcamento'];
    var teto = orcamento && Number(orcamento.teto) || 0;
    if (teto <= 0) {
      api.avisar('— sem teto declarado (motivo: o limite de orçamento ainda não existe nesta base)');
      return;
    }

    var consumo = Math.round(teto * (1 + MARGEM_ESTOURO / 100));
    var porcentagem = Math.round((consumo / teto) * 100);
    if (orcamento) { orcamento.consumo = consumo; }

    pintarBarra(porcentagem);
    atualizarNumeros(consumo, teto, porcentagem);
    acrescentarHistorico(
      'consumo passou do teto: ' + formatar(consumo) + ' contra ' + formatar(teto) + ' (exemplo)',
      'Ana Exemplo',
      'teto do projeto maestro'
    );
    enderecarAviso(estado, 'o teto do projeto maestro foi estourado (' + porcentagem +
      ' % do limite de orçamento) — aviso emitido pelo medidor (exemplo)');

    api.avisar('simulado — o teto estourou: a barra vai a --erro e o aviso vai para a fila outbox (exemplo)');
  }

  /* --------------------------------------------------------------- desenho --- */

  /* A barra é `consumo ÷ teto`. O preenchimento é limitado a 100 % (a largura não passa do
     trilho); o que a cor informa é a FAIXA. */
  function pintarBarra(porcentagem) {
    var barra = document.getElementById('barra-consumo');
    var preenchimento = document.getElementById('barra-preenchimento');
    if (preenchimento) { preenchimento.style.width = Math.min(porcentagem, 100) + '%'; }
    if (!barra) { return; }
    barra.className = 'barra' + (porcentagem > FAIXA_ESTOURADA
      ? ' barra-estourada'
      : (porcentagem > FAIXA_ATENCAO ? ' barra-atencao' : ''));
    barra.setAttribute('aria-label', 'consumo sobre o teto (exemplo: ' + porcentagem + ' %)');
  }

  function atualizarNumeros(consumo, teto, porcentagem) {
    var valor = document.getElementById('consumo-valor');
    var legenda = document.getElementById('consumo-legenda');
    var barra = document.getElementById('barra-legenda');
    if (valor) { valor.textContent = 'exemplo: ' + formatar(consumo); }
    if (legenda) { legenda.textContent = 'exemplo: de ' + formatar(teto) + ' tokens/mês (projeto maestro, escopo projeto)'; }
    if (barra) {
      barra.textContent = 'exemplo: ' + porcentagem + ' % do teto · faixa ' + rotuloFaixa(porcentagem) +
        ' · teto de ' + formatar(teto) + ' tokens/mês (limite de orçamento)';
    }
  }

  function rotuloFaixa(porcentagem) {
    if (porcentagem > FAIXA_ESTOURADA) { return 'estourada (acima de 100 %)'; }
    if (porcentagem > FAIXA_ATENCAO) { return 'atenção (80 % a 100 %)'; }
    return 'normal (até 80 %)';
  }

  /* Linha nova no histórico de mudanças (auditoria administrativa, ENTRA 12). A data é a do
     momento da simulação — declarada como "agora (exemplo)", nunca um instante inventado. */
  function acrescentarHistorico(mudanca, autor, objeto) {
    var corpo = document.querySelector('#historico-orcamento tbody');
    if (!corpo) { return; }
    var linha = document.createElement('tr');
    linha.setAttribute('data-adicionada', 'sim');
    linha.innerHTML =
      '<td><span class="exemplo" data-exemplo="true">exemplo: agora</span></td>' +
      '<td><span class="exemplo" data-exemplo="true">exemplo: ' + escapar(objeto) + '</span></td>' +
      '<td><span class="exemplo" data-exemplo="true">' + escapar(mudanca) + '</span></td>' +
      '<td>' + escapar(autor) + '</td>' +
      '<td><span class="vazio">—</span> motivo: linha criada agora, na simulação (recarregar restaura)</td>';
    corpo.insertBefore(linha, corpo.firstChild);
  }

  /* O aviso vai para a fila outbox (agregado `mensagem`), como qualquer mensagem endereçada —
     quem emite é o medidor (painel/custo.py), não a tela (D3). */
  function enderecarAviso(estado, texto) {
    var agregado = estado['mensagem'];
    var aviso = {
      de: 'Administração — medidor de orçamento (exemplo)',
      para: 'fila outbox',
      resumo: texto,
      status: 'na fila',
      criado_em: 'agora (exemplo)'
    };
    if (agregado && Array.isArray(agregado.mensagens)) {
      agregado.mensagens.push(aviso);
    } else {
      estado['mensagem'] = { projeto: 'maestro', mensagens: [aviso] };
    }
  }

  /* ---------------------------------------------------------------- apoio --- */

  /* Separador de milhar com ponto, como o resto do protótipo. */
  function formatar(numero) {
    return String(numero).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }

  function escapar(texto) {
    return String(texto == null ? '' : texto)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
})();
