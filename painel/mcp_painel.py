#!/usr/bin/env python3
"""Maestro painel as an MCP server (stdio, JSON-RPC 2.0, stdlib only).

Tools:
  estado_atual(sessao?)          -> the derived active context (what the agent reads at session start)
  registrar_status(sessao, estado, texto, autor)   -> append a status event (heartbeat)
  registrar_peca(peca, estado, evidencia, autor, sessao?) -> append a piece transition (evidence required)

Claude Code config (.mcp.json):
  {"mcpServers": {"painel": {"command": "python",
     "args": ["<maestro>/painel/mcp_painel.py", "<maestro>/painel/projetos/exemplo.json"]}}}
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ingest  # noqa: E402
import server  # noqa: E402

FERRAMENTAS = [
    {"name": "estado_atual",
     "description": "Estado atual derivado do projeto (equipe, decisões recentes, barra, desvios, riscos de git, DORA). "
                    "Com 'sessao', inclui o seu estado, peça, worktree, último hash, próximo passo e os seus desvios. "
                    "Chame no início de cada sessão em vez de confiar no 'Estado atual' escrito à mão.",
     "inputSchema": {"type": "object", "properties": {"sessao": {"type": "string", "description": "ex.: W04, Gerente02"}}}},
    {"name": "registrar_status",
     "description": "Registra o seu status (só acrescenta). Use ao mudar de estado e ao menos a cada 60 min.",
     "inputSchema": {"type": "object", "required": ["sessao", "estado", "texto", "autor"], "properties": {
         "sessao": {"type": "string"}, "estado": {"type": "string", "enum": list(server.ESTADOS_SESSAO)},
         "texto": {"type": "string", "description": "o que está fazendo, ou esperando o quê de quem"},
         "peca": {"type": "string"}, "autor": {"type": "string"}}}},
    {"name": "registrar_peca",
     "description": "Registra a transição de uma peça. Recusado sem a evidência exigida pelo estado "
                    + json.dumps(server.EVIDENCIA_EXIGIDA, ensure_ascii=False),
     "inputSchema": {"type": "object", "required": ["peca", "estado", "evidencia", "autor"], "properties": {
         "peca": {"type": "string"}, "estado": {"type": "string", "enum": list(server.ESTADOS_PECA)},
         "evidencia": {"type": "object"}, "texto": {"type": "string"}, "sessao": {"type": "string"},
         "autor": {"type": "string"}}}},
]


def chama(db_path, nome, args):
    if nome == "estado_atual":
        db = server.conecta(db_path)
        try:
            return server.v_estado_ia(db, args.get("sessao"))
        finally:
            db.close()
    db = ingest.abre(db_path)
    try:
        if nome == "registrar_status":
            server.grava_evento(db, {"tipo": "status", **args})
        elif nome == "registrar_peca":
            ev = dict(args)
            ev["evidencia"] = json.dumps(ev.get("evidencia") or {}, ensure_ascii=False)
            server.grava_evento(db, {"tipo": "peca", **ev})
        else:
            raise ValueError(f"ferramenta inexistente: {nome}")
    finally:
        db.close()
    return {"ok": True}


def responde(req, db_path):
    m, rid = req.get("method"), req.get("id")
    if m == "initialize":
        return {"protocolVersion": req.get("params", {}).get("protocolVersion", "2024-11-05"),
                "capabilities": {"tools": {}}, "serverInfo": {"name": "maestro-painel", "version": "0.1"}}
    if m == "tools/list":
        return {"tools": FERRAMENTAS}
    if m == "tools/call":
        p = req.get("params", {})
        try:
            r = chama(db_path, p.get("name"), p.get("arguments") or {})
            return {"content": [{"type": "text", "text": json.dumps(r, ensure_ascii=False, default=str)}]}
        except ValueError as e:
            return {"content": [{"type": "text", "text": f"recusado: {e}"}], "isError": True}
    if m == "ping":
        return {}
    if rid is None:
        return None
    raise LookupError(m)


def main():
    cfg = ingest.carrega_cfg(sys.argv[1])
    db_path = os.path.join(ingest.AQUI, "dados", f"{cfg.get('projeto', 'painel')}.db")
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        ingest.ingere(cfg, db_path)
    for linha in sys.stdin:
        if not linha.strip():
            continue
        req = json.loads(linha)
        try:
            res = responde(req, db_path)
            if req.get("id") is None:
                continue
            out = {"jsonrpc": "2.0", "id": req["id"], "result": res}
        except LookupError as e:
            out = {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32601, "message": f"método desconhecido: {e}"}}
        sys.stdout.write(json.dumps(out, ensure_ascii=False, default=str) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
