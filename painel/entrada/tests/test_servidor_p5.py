"""Testes P5 do servidor: idempotência, contato, dois segredos (chamado 068).

Só dados sintéticos: segredos de teste, telefone de teste, nenhum dado real.
Run: python -m unittest painel.entrada.tests.test_servidor_p5
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from threading import Thread

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import contatos  # noqa: E402
from painel.entrada.servidor import WebhookHandler  # noqa: E402

SEGREDO_ATUAL = "segredo-teste-atual"
SEGREDO_ANTERIOR = "segredo-teste-anterior"
IP_TEST = "127.0.0.1"
PORTA_TEST = 18791
# Dados sintéticos
TEL_CADASTRADO = "559999900001"
TEL_DESCONHECIDO = "559999999999"


def _assina(body: bytes, segredo: str) -> str:
    return hmac.new(segredo.encode(), body, hashlib.sha256).hexdigest()


def _post(body: bytes, headers: dict[str, str]) -> tuple[int, dict]:
    req = urllib.request.Request(
        f"http://{IP_TEST}:{PORTA_TEST}/webhook/whatsapp/entrada",
        data=body, headers=headers, method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


class TestServidorP5(unittest.TestCase):
    server: ThreadingHTTPServer
    thread: Thread

    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        cls.db_path = os.path.join(cls.tmp.name, "entrada.db")
        # Cadastrar um contato de teste
        contatos.add(cls.db_path, telefone=TEL_CADASTRADO, nome="Teste", empresa="Empresa Teste")
        # Configurar env
        os.environ["MAESTRO_WEBHOOK_SEGREDO"] = SEGREDO_ATUAL
        os.environ["MAESTRO_WEBHOOK_SEGREDO.ANTERIOR"] = SEGREDO_ANTERIOR
        os.environ["MAESTRO_ENTRADA_DB"] = cls.db_path
        cls.server = ThreadingHTTPServer((IP_TEST, PORTA_TEST), WebhookHandler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.thread.join(timeout=2)
        cls.tmp.cleanup()
        os.environ.pop("MAESTRO_ENTRADA_DB", None)
        os.environ.pop("MAESTRO_WEBHOOK_SEGREDO.ANTERIOR", None)

    def _evento(self, evento_id="evt-1", telefone=None, texto="oi"):
        d = {"evento_id": evento_id, "timestamp": time.time(), "texto": texto}
        if telefone:
            d["telefone"] = telefone
        return json.dumps(d).encode()

    def test_idempotencia_mesmo_evento_id(self):
        """Mesmo evento_id duas vezes retorna a mesma resposta (P5-AC2)."""
        body = self._evento("evt-idem-1", telefone=TEL_CADASTRADO)
        sig = _assina(body, SEGREDO_ATUAL)
        s1, d1 = _post(body, {"X-Signature": sig})
        s2, d2 = _post(body, {"X-Signature": sig})
        self.assertEqual(s1, s2)
        self.assertEqual(d1, d2)

    def test_contato_desconhecido_resposta_fixa(self):
        """Número não cadastrado recebe resposta fixa, nada criado (P4-AC1)."""
        body = self._evento("evt-desc-1", telefone=TEL_DESCONHECIDO)
        sig = _assina(body, SEGREDO_ATUAL)
        status, data = _post(body, {"X-Signature": sig})
        self.assertEqual(status, 200)
        self.assertIn("cadastro", json.dumps(data, ensure_ascii=False).lower())

    def test_contato_cadastrado_nao_recebe_msg_desconhecido(self):
        """Número cadastrado não recebe a mensagem de desconhecido (P4-AC2)."""
        body = self._evento("evt-cad-1", telefone=TEL_CADASTRADO)
        sig = _assina(body, SEGREDO_ATUAL)
        status, data = _post(body, {"X-Signature": sig})
        self.assertEqual(status, 202)
        self.assertNotIn("cadastro", json.dumps(data, ensure_ascii=False).lower())

    def test_segredo_anterior_valida(self):
        """NFR-008: assinatura com o segredo anterior também valida."""
        body = self._evento("evt-ant-1", telefone=TEL_CADASTRADO)
        sig = _assina(body, SEGREDO_ANTERIOR)
        status, data = _post(body, {"X-Signature": sig})
        self.assertIn(status, (200, 202))


if __name__ == "__main__":
    unittest.main()
