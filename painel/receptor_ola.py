"""Receptor HTTPS das mensagens do grupo Ola, enviadas pelo n8n (spec 069).

    python painel/receptor_ola.py projetos/hindiana.json

POST /webhook/ola/mensagens  (Bearer, JSON)  ->  202 nova | 200 duplicada | 400 | 401 | 403 | 413 | 429
GET  /saude                                   ->  {"ok": true}

O texto recebido é conteúdo externo: é guardado literal e nunca interpretado nem executado.
O token vem da variável de ambiente do usuário Windows OLA_WEBHOOK_TOKEN (e OLA_WEBHOOK_TOKEN_ANTERIOR
durante a troca); ele não é lido de arquivo, não é impresso e não vai para o log.
"""
from __future__ import annotations

import collections
import datetime as dt
import hmac
import json
import os
import queue
import re
import sqlite3
import ssl
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROTA = "/webhook/ola/mensagens"
CAMPOS = {"grupo": str, "remetente": str, "nome": str, "texto": str, "message_id": str, "tipo": str,
          "instancia": str, "fromMe": bool, "data_hora": str}
RE_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?(Z|[+-]\d{2}:\d{2})$")
ESQUEMA = """
CREATE TABLE IF NOT EXISTS mensagens (
  instancia TEXT NOT NULL, message_id TEXT NOT NULL, grupo TEXT, remetente TEXT, nome TEXT, texto TEXT,
  tipo TEXT, from_me INTEGER, data_hora TEXT, recebido_em TEXT NOT NULL, estado TEXT NOT NULL, bruto TEXT,
  PRIMARY KEY (instancia, message_id));
"""


def valida(dados) -> str | None:
    """Devolve o motivo do 400, ou None se o corpo está no formato."""
    if not isinstance(dados, dict):
        return "corpo deve ser um objeto JSON"
    for campo, tipo in CAMPOS.items():
        if campo not in dados:
            return f"campo obrigatório ausente: {campo}"
        if type(dados[campo]) is not tipo:  # bool não passa por str e vice-versa
            return f"campo {campo} deve ser {'booleano' if tipo is bool else 'texto'}"
    if not 1 <= len(dados["message_id"]) <= 200:
        return "message_id deve ter de 1 a 200 caracteres"
    if not 1 <= len(dados["tipo"]) <= 60:
        return "tipo deve ter de 1 a 60 caracteres"
    if not RE_DATA.match(dados["data_hora"]):
        return "data_hora deve ser ISO 8601 com fuso (ex.: 2026-10-06T17:11:25.000Z)"
    return None


class Servidor(ThreadingHTTPServer):
    daemon_threads = True


def _log(cfg, **campos):
    os.makedirs(cfg["log_dir"], exist_ok=True)
    campos["ts"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    with open(os.path.join(cfg["log_dir"], f"receptor-ola-{dt.date.today():%Y%m%d}.log"), "a", encoding="utf-8") as f:
        f.write(json.dumps(campos, ensure_ascii=False) + "\n")


def _enfileira(srv):
    while True:
        item = srv.fila.get()
        if item is None:
            return
        try:
            with sqlite3.connect(srv.cfg["db"], timeout=30) as db:
                db.execute("UPDATE mensagens SET estado='enfileirada' WHERE instancia=? AND message_id=? AND estado='pendente'", item)
        except sqlite3.Error as e:
            _log(srv.cfg, evento="erro_fila", erro=type(e).__name__)


def cria_servidor(cfg: dict) -> Servidor:
    os.makedirs(os.path.dirname(os.path.abspath(cfg["db"])), exist_ok=True)
    with sqlite3.connect(cfg["db"]) as db:
        db.executescript(ESQUEMA)
    if not [t for t in cfg["tokens"] if t]:
        raise SystemExit("nenhum token configurado (OLA_WEBHOOK_TOKEN)")

    class H(BaseHTTPRequestHandler):
        server_version = "receptor-ola"
        sys_version = ""

        def log_message(self, *a):  # o log padrão traria o caminho e o IP sem controle; usamos o nosso
            pass

        def _responde(self, status, corpo, extra=None, inicio=None, **log):
            dados = json.dumps(corpo, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(dados)))
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(dados)
            _log(srv.cfg, ip=self.client_address[0], rota=self.path[:60], status=status,
                 ms=int((time.time() - (inicio or time.time())) * 1000), **log)

        def do_GET(self):
            if self.path == "/saude":
                return self._responde(200, {"ok": True})
            return self._responde(404, {"accepted": False, "erro": "rota inexistente"})

        def do_POST(self):
            inicio = time.time()
            c = srv.cfg
            if self.path != ROTA:
                return self._responde(404, {"accepted": False, "erro": "rota inexistente"}, inicio=inicio)
            ip = self.client_address[0]
            if ip not in c["ips"]:
                return self._responde(403, {"accepted": False, "erro": "origem não permitida"}, inicio=inicio)
            tam = int(self.headers.get("Content-Length") or 0)
            if tam > c["max_bytes"]:
                return self._responde(413, {"accepted": False, "erro": f"corpo maior que {c['max_bytes']} bytes"}, inicio=inicio)
            with srv.trava:
                janela = srv.chamadas[ip]
                while janela and janela[0] < inicio - 60:
                    janela.popleft()
                if len(janela) >= c["limite_por_min"]:
                    espera = max(1, int(61 - (inicio - janela[0])))
                    return self._responde(429, {"accepted": False, "erro": "limite de frequência"},
                                          extra={"Retry-After": str(espera)}, inicio=inicio)
                janela.append(inicio)
            aut = self.headers.get("Authorization", "")
            recebido = aut[7:].encode() if aut.startswith("Bearer ") else b""
            if not recebido or not any(hmac.compare_digest(recebido, t.encode()) for t in c["tokens"] if t):
                return self._responde(401, {"accepted": False, "erro": "autenticacao"}, inicio=inicio)
            corpo = self.rfile.read(tam)
            try:
                dados = json.loads(corpo.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return self._responde(400, {"accepted": False, "erro": "JSON inválido"}, inicio=inicio)
            erro = valida(dados)
            if not erro and dados["grupo"] not in c["grupos"]:
                erro = "grupo não permitido"
            if not erro and dados["instancia"] not in c["instancias"]:
                erro = "instancia não permitida"
            if erro:
                return self._responde(400, {"accepted": False, "erro": erro}, inicio=inicio)
            chave = (dados["instancia"], dados["message_id"])
            with sqlite3.connect(c["db"], timeout=30) as db:
                cur = db.execute("INSERT OR IGNORE INTO mensagens VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                                 (*chave, dados["grupo"], dados["remetente"], dados["nome"], dados["texto"], dados["tipo"],
                                  int(dados["fromMe"]), dados["data_hora"],
                                  dt.datetime.now().astimezone().isoformat(timespec="seconds"), "pendente",
                                  json.dumps(dados, ensure_ascii=False)))
                nova = cur.rowcount == 1
            if nova:
                srv.fila.put(chave)
                return self._responde(202, {"accepted": True, "message_id": dados["message_id"]}, inicio=inicio,
                                      instancia=chave[0], message_id=chave[1], resultado="nova")
            return self._responde(200, {"accepted": True, "message_id": dados["message_id"], "duplicada": True},
                                  inicio=inicio, instancia=chave[0], message_id=chave[1], resultado="duplicada")

    srv = Servidor((cfg["host"], cfg["porta"]), H)
    srv.cfg = cfg
    srv.trava = threading.Lock()
    srv.chamadas = collections.defaultdict(collections.deque)
    srv.fila = queue.Queue()
    srv.trabalhador = threading.Thread(target=_enfileira, args=(srv,), daemon=True)
    srv.trabalhador.start()
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_cert_chain(cfg["cert"], cfg["key"])
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    return srv


def zera_limites(srv):
    with srv.trava:
        srv.chamadas.clear()


def para(srv):
    srv.fila.put(None)


def _token_do_ambiente(nome):
    v = os.environ.get(nome, "")
    if v or os.name != "nt":
        return v
    import winreg  # a variável pode ter sido criada com setx depois de abrir este terminal
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, nome)[0]
    except OSError:
        return ""


def main(argv=None):
    aqui = os.path.dirname(os.path.abspath(__file__))
    caminho = (argv or sys.argv[1:] or [os.path.join(aqui, "projetos", "hindiana.json")])[0]
    bruto = json.load(open(caminho, encoding="utf-8"))
    rc = bruto.get("receptor_ola", bruto)  # aceita o hindiana.json do painel ou o config.json do LXC
    dados = rc.get("dados", os.path.join(aqui, "dados"))  # no LXC: /var/lib/receptor-ola
    cfg = {"host": rc.get("host", "192.168.15.12"), "porta": int(rc.get("porta", 8793)),
           "db": os.path.join(dados, "ola_grupo.db"), "log_dir": os.path.join(dados, "logs"),
           "ips": rc.get("ips", ["192.168.15.9"]), "grupos": rc.get("grupos", ["120363413483485664@g.us"]),
           "instancias": rc.get("instancias", ["whatsapp-daru"]), "max_bytes": int(rc.get("max_bytes", 65536)),
           "limite_por_min": int(rc.get("limite_por_min", 120)),
           "cert": rc.get("cert", os.path.join(dados, "tls", "servidor.crt")),
           "key": rc.get("key", os.path.join(dados, "tls", "servidor.key")),
           "tokens": [_token_do_ambiente("OLA_WEBHOOK_TOKEN"), _token_do_ambiente("OLA_WEBHOOK_TOKEN_ANTERIOR")]}
    srv = cria_servidor(cfg)
    print(f"receptor do grupo Ola em https://{cfg['host']}:{cfg['porta']}{ROTA} (origens {', '.join(cfg['ips'])})")
    srv.serve_forever()


if __name__ == "__main__":
    main()
