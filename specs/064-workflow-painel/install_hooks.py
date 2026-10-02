#!/usr/bin/env python3
"""Installer para os hooks do workflow 064.

Copia os hooks scripts para scripts/hooks/ e mescla as entradas de hook
no .claude/settings.json do projeto alvo. NÃO sobrescreve hooks existentes —
apenas adiciona os que faltam.

Uso: python install_hooks.py /caminho/para/projeto

A instalação deve ser feita pela Assistente após APPROVE e ordem do Gilsiley.
"""
from __future__ import annotations

import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO_RAIZ = os.path.join(AQUI, "..", "..")
HOOKS_SRC = os.path.join(REPO_RAIZ, "scripts", "hooks")
EXAMPLE = os.path.join(AQUI, "settings.example.json")

HOOK_FILES = ["workflow_session_start.py", "workflow_stop.py"]


def instalar(projeto_dir: str) -> None:
    projeto_dir = os.path.abspath(projeto_dir)
    hooks_dir = os.path.join(projeto_dir, "scripts", "hooks")
    settings_path = os.path.join(projeto_dir, ".claude", "settings.json")

    # 1. Copia os scripts de hook
    os.makedirs(hooks_dir, exist_ok=True)
    for f in HOOK_FILES:
        src = os.path.join(HOOKS_SRC, f)
        dst = os.path.join(hooks_dir, f)
        shutil.copy2(src, dst)
        print(f"  ✓ copiado: scripts/hooks/{f}")

    # 2. Mescla hooks no settings.json
    with open(EXAMPLE) as f:
        example = json.load(f)

    if os.path.exists(settings_path):
        with open(settings_path) as f:
            current = json.load(f)
    else:
        current = {"hooks": {}}

    current.setdefault("hooks", {})
    for event, entries in example["hooks"].items():
        current["hooks"].setdefault(event, [])
        existing_cmds = {
            h["command"]
            for entry in current["hooks"][event]
            for h in entry.get("hooks", [])
        }
        for entry in entries:
            new_cmds = [h["command"] for h in entry.get("hooks", [])]
            if any(c not in existing_cmds for c in new_cmds):
                current["hooks"][event].append(entry)
                print(f"  ✓ hook adicionado: {event}")

    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    with open(settings_path, "w") as f:
        json.dump(current, f, indent=2)
        f.write("\n")
    print(f"  ✓ settings.json atualizado: {settings_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python install_hooks.py /caminho/para/projeto")
        sys.exit(1)
    instalar(sys.argv[1])
