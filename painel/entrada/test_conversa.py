"""Teste vermelho da maquina de estados conversa.py (T1-01).

Cobre o fluxo de abertura de chamado pelo WhatsApp:
  menu -> tipo -> descricao -> onde -> passos -> esperado_aconteceu
       -> anexos -> confirmacao -> criado

Para bug. Melhoria/sugestao pulam onde, passos e esperado_aconteceu.
Cancelar em qualquer passo. Expirar em 30 min.

Roda com: python -m painel.entrada.test_conversa
"""

from __future__ import annotations

import unittest

from painel.entrada.conversa import conversa, ESTADO_INICIO, TEMPO_EXPIRACAO_SEG


class TestConversaBugFluxoCompleto(unittest.TestCase):
    """Happy path: cliente cadastrado abre chamado de bug."""

    def _iniciar(self) -> tuple[str, dict]:
        estado, resposta, acao, dados = conversa(
            ESTADO_INICIO, "oi", {}
        )
        self.assertIsNone(acao)
        self.assertIn("Bug", resposta)
        return estado, dados

    def test_oi_mostra_menu(self) -> None:
        estado, resposta, acao, dados = conversa(ESTADO_INICIO, "oi", {})
        self.assertEqual(estado, "menu")
        self.assertIn("Bug", resposta)
        self.assertIn("Melhoria", resposta)
        self.assertIn("Sugestao", resposta)
        self.assertIsNone(acao)

    def test_fluxo_bug_completo(self) -> None:
        # 1. oi -> menu
        estado, _, _, dados = conversa(ESTADO_INICIO, "oi", {})
        self.assertEqual(estado, "menu")

        # 2. escolhe 1 (Bug) -> descricao
        estado, resp, _, dados = conversa(estado, "1", dados)
        self.assertEqual(estado, "descricao")
        self.assertEqual(dados["tipo"], "bug")

        # 3. descricao -> onde
        estado, resp, _, dados = conversa(estado, "tela trava ao salvar", dados)
        self.assertEqual(estado, "onde")
        self.assertEqual(dados["descricao"], "tela trava ao salvar")

        # 4. onde -> passos
        estado, resp, _, dados = conversa(estado, "Ficha > Salvar", dados)
        self.assertEqual(estado, "passos")
        self.assertEqual(dados["onde"], "Ficha > Salvar")

        # 5. passos -> esperado_aconteceu
        estado, resp, _, dados = conversa(
            estado, "1. Abri a Ficha 2. Cliquei Salvar", dados
        )
        self.assertEqual(estado, "esperado_aconteceu")
        self.assertEqual(dados["passos"], "1. Abri a Ficha 2. Cliquei Salvar")

        # 6. esperado_aconteceu -> anexos
        estado, resp, _, dados = conversa(
            estado, "Esperava salvar mas deu erro 500", dados
        )
        self.assertEqual(estado, "anexos")
        self.assertIn("esperado", dados)

        # 7. anexos -> confirmacao
        estado, resp, _, dados = conversa(estado, "pular", dados)
        self.assertEqual(estado, "confirmacao")

        # 8. confirmacao -> criado + acao criar
        estado, resp, acao, dados = conversa(estado, "sim", dados)
        self.assertEqual(estado, "criado")
        self.assertIsNotNone(acao)
        self.assertEqual(acao["tipo"], "criar")
        self.assertEqual(acao["dados"]["tipo"], "bug")
        self.assertEqual(acao["dados"]["descricao"], "tela trava ao salvar")
        self.assertIn("#", resp)  # tem o numero do chamado


class TestConversaMelhoriaFluxoCurto(unittest.TestCase):
    """Melhoria pula onde, passos e esperado_aconteceu."""

    def test_fluxo_melhoria(self) -> None:
        estado, _, _, dados = conversa(ESTADO_INICIO, "oi", {})
        estado, _, _, dados = conversa(estado, "2", dados)
        self.assertEqual(estado, "descricao")
        self.assertEqual(dados["tipo"], "melhoria")

        estado, _, _, dados = conversa(estado, "botao de exportar", dados)
        self.assertEqual(estado, "anexos")
        self.assertEqual(dados["descricao"], "botao de exportar")

        estado, _, _, dados = conversa(estado, "pular", dados)
        self.assertEqual(estado, "confirmacao")

        estado, _, acao, dados = conversa(estado, "sim", dados)
        self.assertEqual(estado, "criado")
        self.assertEqual(acao["tipo"], "criar")
        self.assertEqual(acao["dados"]["tipo"], "melhoria")


class TestConversaSugestaoFluxoCurto(unittest.TestCase):
    """Sugestao tambem pula onde, passos e esperado_aconteceu."""

    def test_fluxo_sugestao(self) -> None:
        estado, _, _, dados = conversa(ESTADO_INICIO, "oi", {})
        estado, _, _, dados = conversa(estado, "3", dados)
        self.assertEqual(estado, "descricao")
        self.assertEqual(dados["tipo"], "sugestao")

        estado, _, _, dados = conversa(estado, "dark mode", dados)
        self.assertEqual(estado, "anexos")

        estado, _, _, dados = conversa(estado, "pular", dados)
        self.assertEqual(estado, "confirmacao")

        estado, _, acao, _ = conversa(estado, "sim", dados)
        self.assertEqual(acao["tipo"], "criar")
        self.assertEqual(acao["dados"]["tipo"], "sugestao")


class TestConversaCancelar(unittest.TestCase):
    """Cancelar em qualquer passo volta a cancelado."""

    def test_cancelar_no_menu(self) -> None:
        estado, _, _, _ = conversa(ESTADO_INICIO, "oi", {})
        estado, resp, acao, _ = conversa(estado, "cancelar", {})
        self.assertEqual(estado, "cancelado")
        self.assertIsNone(acao)

    def test_cancelar_na_descricao(self) -> None:
        estado, _, _, dados = conversa(ESTADO_INICIO, "oi", {})
        estado, _, _, dados = conversa(estado, "1", dados)
        estado, resp, acao, _ = conversa(estado, "cancelar", dados)
        self.assertEqual(estado, "cancelado")
        self.assertIsNone(acao)

    def test_cancelar_nos_passos(self) -> None:
        estado, _, _, dados = conversa(ESTADO_INICIO, "oi", {})
        estado, _, _, dados = conversa(estado, "1", dados)
        estado, _, _, dados = conversa(estado, "travou", dados)
        estado, _, _, dados = conversa(estado, "Ficha", dados)
        estado, resp, acao, _ = conversa(estado, "cancelar", dados)
        self.assertEqual(estado, "cancelado")
        self.assertIsNone(acao)


class TestConversaExpirar(unittest.TestCase):
    """Conversa expira em 30 min sem resposta."""

    def test_tempo_expiracao_e_30_min(self) -> None:
        self.assertEqual(TEMPO_EXPIRACAO_SEG, 1800)

    def test_expirar_volta_inicio(self) -> None:
        estado, _, _, dados = conversa(ESTADO_INICIO, "oi", {})
        estado, resp, acao, dados = conversa(estado, "expirar", dados)
        self.assertEqual(estado, "expirado")
        self.assertIsNone(acao)


class TestConversaMensagensForaDoFluxo(unittest.TestCase):
    """Mensagens inesperadas nao quebram a conversa."""

    def test_mensagem_ignorada_no_inicio(self) -> None:
        """Qualquer mensagem no inicio inicia o menu."""
        estado, _, _, _ = conversa(ESTADO_INICIO, "qualquer coisa", {})
        self.assertEqual(estado, "menu")

    def test_opcao_invalida_no_menu_mantem_menu(self) -> None:
        estado, _, _, dados = conversa(ESTADO_INICIO, "oi", {})
        estado, resp, acao, dados = conversa(estado, "9", dados)
        self.assertEqual(estado, "menu")
        self.assertIsNone(acao)

    def test_confirmacao_nao_repete_acao(self) -> None:
        """Depois de criado, nova mensagem nao gera acao criar."""
        estado, _, _, dados = conversa(ESTADO_INICIO, "oi", {})
        estado, _, _, dados = conversa(estado, "1", dados)
        estado, _, _, dados = conversa(estado, "bug", dados)
        estado, _, _, dados = conversa(estado, "tela", dados)
        estado, _, _, dados = conversa(estado, "passos", dados)
        estado, _, _, dados = conversa(estado, "esperado", dados)
        estado, _, _, dados = conversa(estado, "pular", dados)
        estado, _, acao, dados = conversa(estado, "sim", dados)
        self.assertIsNotNone(acao)
        # apos criado, nova mensagem nao gera nova acao
        estado, _, acao2, _ = conversa(estado, "obrigado", dados)
        self.assertIsNone(acao2)


class TestConversaAnexos(unittest.TestCase):
    """Anexos sao acumulados ate pular."""

    def test_anexos_acumulados(self) -> None:
        estado, _, _, dados = conversa(ESTADO_INICIO, "oi", {})
        estado, _, _, dados = conversa(estado, "1", dados)
        estado, _, _, dados = conversa(estado, "travou", dados)
        estado, _, _, dados = conversa(estado, "Ficha", dados)
        estado, _, _, dados = conversa(estado, "passos", dados)
        estado, _, _, dados = conversa(estado, "esperado", dados)
        # anexos
        estado, _, _, dados = conversa(estado, "captura1.png", dados)
        self.assertEqual(estado, "anexos")
        self.assertIn("captura1.png", dados.get("anexos", []))
        estado, _, _, dados = conversa(estado, "captura2.png", dados)
        self.assertEqual(estado, "anexos")
        self.assertIn("captura2.png", dados.get("anexos", []))
        # pular vai a confirmacao
        estado, _, _, dados = conversa(estado, "pular", dados)
        self.assertEqual(estado, "confirmacao")


if __name__ == "__main__":
    unittest.main()
