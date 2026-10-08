"""Testes do esqueleto do servidor de entrada (T0-02).

Stdlib only: unittest, urllib, json, hmac, hashlib, threading.
Roda com: python -m painel.entrada.test_servidor
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from threading import Thread

from painel.entrada.servidor import WebhookHandler, _assina, _dentro_janela, _ip_permitido

_SEGREDO_TEST = "segredo-de-teste"
_IP_TEST = "127.0.0.1"
_PORTA_TEST = 18790


def _post(path: str, body: bytes, headers: dict[str, str]) -> tuple[int, dict]:
    req = urllib.request.Request(
        f"http://{_IP_TEST}:{_PORTA_TEST}{path}",
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        status = resp.status
        data = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        status = exc.code
        data = json.loads(exc.read())
    return status, data


def _get(path: str) -> tuple[int, dict]:
    req = urllib.request.Request(f"http://{_IP_TEST}:{_PORTA_TEST}{path}")
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        status = resp.status
        data = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        status = exc.code
        data = json.loads(exc.read())
    return status, data


class TestFuncoesPuras(unittest.TestCase):
    def test_assina_hex_sha256(self) -> None:
        body = b'{"evento_id":"e1"}'
        esperado = hmac.new(_SEGREDO_TEST.encode(), body, hashlib.sha256).hexdigest()
        self.assertEqual(_assina(body, _SEGREDO_TEST.encode()), esperado)

    def test_ip_permitido_sim(self) -> None:
        self.assertTrue(_ip_permitido("127.0.0.1", ["127.0.0.1"]))

    def test_ip_permitido_nao(self) -> None:
        self.assertFalse(_ip_permitido("10.0.0.5", ["127.0.0.1"]))

    def test_dentro_janela_sim(self) -> None:
        agora = 1000.0
        self.assertTrue(_dentro_janela(900.0, agora))

    def test_dentro_janela_nao(self) -> None:
        agora = 1000.0
        self.assertFalse(_dentro_janela(100.0, agora))


class TestServidorSkeleton(unittest.TestCase):
    server: ThreadingHTTPServer
    thread: Thread

    @classmethod
    def setUpClass(cls) -> None:
        os.environ["MAESTRO_WEBHOOK_SEGREDO"] = _SEGREDO_TEST
        cls.server = ThreadingHTTPServer((_IP_TEST, _PORTA_TEST), WebhookHandler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def test_saude_ok(self) -> None:
        status, data = _get("/saude")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "ok")

    def test_rota_inexistente(self) -> None:
        status, _ = _get("/nao-existe")
        self.assertEqual(status, 404)

    def test_webhook_sem_assinatura(self) -> None:
        body = json.dumps({"evento_id": "e1", "timestamp": time.time()}).encode()
        status, data = _post("/webhook/whatsapp/entrada", body, {})
        self.assertEqual(status, 401)
        self.assertIn("assinatura", data["erro"])

    def test_webhook_assinatura_invalida(self) -> None:
        body = json.dumps({"evento_id": "e1", "timestamp": time.time()}).encode()
        status, data = _post(
            "/webhook/whatsapp/entrada", body, {"X-Signature": "invalida"}
        )
        self.assertEqual(status, 401)

    def test_webhook_assinatura_valida(self) -> None:
        body = json.dumps(
            {"evento_id": "e1", "timestamp": time.time(), "mensagem": "oi"}
        ).encode()
        assinatura = _assina(body, _SEGREDO_TEST.encode())
        status, data = _post(
            "/webhook/whatsapp/entrada", body, {"X-Signature": assinatura}
        )
        self.assertEqual(status, 202)
        self.assertEqual(data["status"], "aceito")
        self.assertEqual(data["evento_id"], "e1")

    def test_webhook_sem_evento_id(self) -> None:
        body = json.dumps({"timestamp": time.time()}).encode()
        assinatura = _assina(body, _SEGREDO_TEST.encode())
        status, data = _post(
            "/webhook/whatsapp/entrada", body, {"X-Signature": assinatura}
        )
        self.assertEqual(status, 400)
        self.assertIn("evento_id", data["erro"])

    def test_webhook_json_invalido(self) -> None:
        body = b"nao e json"
        assinatura = _assina(body, _SEGREDO_TEST.encode())
        status, data = _post(
            "/webhook/whatsapp/entrada", body, {"X-Signature": assinatura}
        )
        self.assertEqual(status, 400)
        self.assertIn("json", data["erro"])

    def test_webhook_fora_janela(self) -> None:
        body = json.dumps(
            {"evento_id": "e2", "timestamp": time.time() - 3600}
        ).encode()
        assinatura = _assina(body, _SEGREDO_TEST.encode())
        status, data = _post(
            "/webhook/whatsapp/entrada", body, {"X-Signature": assinatura}
        )
        self.assertEqual(status, 408)


if __name__ == "__main__":
    unittest.main()
