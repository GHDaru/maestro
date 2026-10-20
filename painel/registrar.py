#!/usr/bin/env python3
"""Maestro painel: append a fact that lives in no file (append-only `eventos`).

Examples:
  python registrar.py projetos/exemplo.json status --sessao W04 --estado trabalhando --texto "painel Maestro" --autor Assistente
  python registrar.py projetos/exemplo.json deploy --estado SUCCESS --texto "railway: 603c44e" --evidencia '{"hash":"603c44e"}' --autor Office
  python registrar.py projetos/exemplo.json peca --peca P6 --estado "suites aceitas" --evidencia '{"hash":"bf2916c","runner2":"1646+775, vitest 621"}' --autor Gerente02
  python registrar.py projetos/exemplo.json incidente --peca D6 --texto "404 listas-mestras" --autor Office
"""
from __future__ import annotations

import argparse
import os
import sys

import ingest
import server


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projeto")
    ap.add_argument("tipo", choices=["status", "deploy", "incidente", "recuperacao", "peca", "nota"])
    ap.add_argument("--sessao")
    ap.add_argument("--estado")
    ap.add_argument("--peca")
    ap.add_argument("--texto")
    ap.add_argument("--evidencia")
    ap.add_argument("--autor", required=True)
    ap.add_argument("--ts")
    ap.add_argument("--db")
    a = ap.parse_args(argv)
    cfg = ingest.carrega_cfg(a.projeto)
    db_path = a.db or os.path.join(ingest.AQUI, "dados", f"{cfg.get('projeto', 'painel')}.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db = ingest.abre(db_path)
    try:
        server.grava_evento(db, {k: v for k, v in vars(a).items() if k not in ("projeto", "db")})
    except ValueError as e:
        print(f"recusado: {e}", file=sys.stderr)
        return 2
    finally:
        db.close()
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
