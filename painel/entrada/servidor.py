"""Servidor de entrada de webhooks do WhatsApp (chamado 068).

Recebe webhooks do n8n (que vêm da Evolution API), valida assinatura
HMAC-SHA256, IP de origem e janela de tempo, e responde em menos de 2 s.
O processamento da conversa fica em conversa.py (P1/P3); aqui é só o
esqueleto (T0-02).

P5 (W02): dois segredos HMAC (NFR-008), idempotência por evento_id
e checagem de contato cadastrado (P4).

Stdlib only: http.server, hmac, json, os, time, urllib.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

try:
    from . import contatos, eventos
except ImportError:
    import contatos, eventos

# --- Configuração -----------------------------------------------------------

_JANELA_SEG = 300  # 5 min


def _carregar_config() -> dict:
    """Lê o bloco ``entrada`` de painel/projetos/hindiana.json."""
    caminho = Path(__file__).resolve().parent.parent / "projetos" / "hindiana.json"
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    return dados["entrada"]


def _segredo() -> bytes:
    """Lê o segredo HMAC da variável de ambiente configurada."""
    env_var = _carregar_config().get("segredo_env", "MAESTRO_WEBHOOK_SEGREDO")
    valor = os.environ.get(env_var, "")
    if not valor:
        raise RuntimeError(f"Variável {env_var} não definida")
    return valor.encode("utf-8")


def _segredos() -> list[bytes]:
    """Lê o segredo atual e o anterior (NFR-008 — rotação sem parar a entrada)."""
    env_var = _carregar_config().get("segredo_env", "MAESTRO_WEBHOOK_SEGREDO")
    segredos: list[bytes] = []
    valor = os.environ.get(env_var, "")
    if valor:
        segredos.append(valor.encode("utf-8"))
    # Segredo anterior (NFR-008)
    valor_ant = os.environ.get(f"{env_var}.ANTERIOR", "")
    if valor_ant:
        segredos.append(valor_ant.encode("utf-8"))
    if not segredos:
        raise RuntimeError(f"Variável {env_var} não definida")
    return segredos


def _db_path() -> str:
    """Caminho do banco de entrada (env ou default)."""
    return os.environ.get(
        "MAESTRO_ENTRADA_DB",
        str(Path(__file__).resolve().parent.parent / "dados" / "entrada.db"),
    )


# --- Validações ------------------------------------------------------------


def _assina(body: bytes, segredo: bytes) -> str:
    """Calcula HMAC-SHA256 do body e devolve em hex minúsculo."""
    return hmac.new(segredo, body, hashlib.sha256).hexdigest()


def _ip_permitido(ip_cliente: str, ips_autorizados: list[str]) -> bool:
    return ip_cliente in ips_autorizados


def _dentro_janela(timestamp_recebido: float, agora: float | None = None) -> bool:
    if agora is None:
        agora = time.time()
    return abs(agora - timestamp_recebido) <= _JANELA_SEG


# --- Handler ----------------------------------------------------------------


class WebhookHandler(BaseHTTPRequestHandler):
    """Handler para /saude e /webhook/whatsapp/entrada."""

    # http.server loga no stderr por padrão; silenciamos para não vazar
    # conteúdo do body no log.
    def log_message(self, fmt: str, *args: object) -> None:  # noqa: A003
        pass

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        rota = urlparse(self.path).path
        if rota == "/saude":
            self._json(200, {"status": "ok"})
            return
        self._json(404, {"erro": "rota nao encontrada"})

    def do_POST(self) -> None:
        rota = urlparse(self.path).path
        if rota != "/webhook/whatsapp/entrada":
            self._json(404, {"erro": "rota nao encontrada"})
            return

        config = _carregar_config()

        # 1. IP de origem
        ip_cliente = self.client_address[0]
        if not _ip_permitido(ip_cliente, config.get("ips_n8n", [])):
            self._json(403, {"erro": "ip nao autorizado"})
            return

        # 2. Body
        tamanho = int(self.headers.get("Content-Length", 0))
        if tamanho == 0 or tamanho > 1_000_000:
            self._json(400, {"erro": "body invalido"})
            return
        body = self.rfile.read(tamanho)

        # 3. Assinatura HMAC-SHA256 — dois segredos (NFR-008)
        assinatura_recebida = self.headers.get("X-Signature", "")
        try:
            segredos = _segredos()
        except RuntimeError as exc:
            self._json(500, {"erro": "configuracao incompleta", "detalhe": str(exc)})
            return
        assinatura_ok = False
        for segredo in segredos:
            if hmac.compare_digest(assinatura_recebida, _assina(body, segredo)):
                assinatura_ok = True
                break
        if not assinatura_ok:
            self._json(401, {"erro": "assinatura invalida"})
            return

        # 4. Parse JSON
        try:
            evento = json.loads(body)
        except json.JSONDecodeError:
            self._json(400, {"erro": "json invalido"})
            return

        # 5. Janela de tempo
        ts = evento.get("timestamp")
        if ts is not None:
            try:
                if not _dentro_janela(float(ts)):
                    self._json(408, {"erro": "evento fora da janela de tempo"})
                    return
            except (TypeError, ValueError):
                self._json(400, {"erro": "timestamp invalido"})
                return

        # 6. Idempotência (evento_id) — P5-AC2
        evento_id = evento.get("evento_id")
        if not evento_id:
            self._json(400, {"erro": "evento_id ausente"})
            return

        # 7. Processamento com idempotência e checagem de contato (P4 + P5)
        db = _db_path()

        def _processar() -> dict:
            # P4: checagem de contato cadastrado
            telefone = evento.get("telefone")
            if telefone:
                contato = contatos.lookup(db, telefone)
                if not contato:
                    return {
                        "status_code": 200,
                        "payload": {"responder": [{"texto": (
                            "Não encontramos seu cadastro. "
                            "Fale com o Escritório de Transformação da sua empresa."
                        )}]},
                    }
            # Skeleton — processamento vem em P1/P3 (conversa.py).
            return {"status_code": 202, "payload": {"status": "aceito", "evento_id": evento_id}}

        res = eventos.processa(db, evento_id, _processar)
        self._json(res["status_code"], res["payload"])


# --- Main -------------------------------------------------------------------


def main() -> None:
    config = _carregar_config()
    ip = config.get("ip", "127.0.0.1")
    porta = int(config.get("porta", 8790))
    servidor = ThreadingHTTPServer((ip, porta), WebhookHandler)
    print(f"Entrada ouvindo em {ip}:{porta}")  # noqa: T201
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.shutdown()


if __name__ == "__main__":
    main()
