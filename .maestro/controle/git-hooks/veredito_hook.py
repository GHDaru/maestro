#!/usr/bin/env python3
"""Hook de veredito: valida hora e objeto de arquivos veredito*.md / critica*.md.

Desejo 004: a hora do veredito vem de fonte verificável.
Repo: maestro, branch painel-controle.

Regras:
1. O veredito tem linha `Objeto: <caminho> @ <hash>`. Sem ela, recusado.
2. O hash tem de existir e não ser posterior ao commit do veredito.
3. A hora no texto (`Data:`) não pode ser > hora do commit + 2 min (tolerância).
4. A hora do veredito tem de ser posterior à hora do commit do objeto (autor date %ai).
5. Sem hora no texto, usa a hora do commit (ou mtime do arquivo se pré-commit).
6. Cherry-pick: usa data do autor (%ai), não do committer.

Uso:
  pre-commit:  python veredito_hook.py --pre-commit
  standalone:   python veredito_hook.py <arquivo>
  test:         python -m pytest test_veredito_hook.py
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Tolerância: 2 minutos
TOLERANCIA = timedelta(minutes=2)

# Fuso BRT (-03:00)
BRT = timezone(timedelta(hours=-3))

# Padrões de arquivo de veredito
VEREDITO_PATTERNS = ("veredito", "critica")

# Regex para linha Objeto
RE_OBJETO = re.compile(r"^Objeto:\s*(.+?)\s+@\s+([0-9a-f]{7,40})\s*$", re.MULTILINE)

# Regex para linha Data (vários formatos)
# "Data: 03/10/2026 13:19 -0300" ou "Data: 03/10/2026 13:19" ou "Data: sáb, 3 de out de 2026 13:19:15"
RE_DATA_DDMMYYYY_HHMM = re.compile(
    r"Data:\s*(\d{2}/\d{2}/\d{4})\s+(\d{2}):(\d{2})(?:\s*([+-]\d{4}))?", re.MULTILINE
)
RE_DATA_EXTENSO = re.compile(
    r"Data:\s*\w+,?\s+\d+\s+de\s+\w+\s+de\s+(\d{4})\s+(\d{2}):(\d{2}):(\d{2})", re.MULTILINE
)


@dataclass
class VereditoCheck:
    """Resultado da verificação de um veredito."""
    arquivo: str
    ok: bool
    motivo: str = ""
    hora_texto: datetime | None = None
    hora_commit: datetime | None = None
    objeto_caminho: str = ""
    objeto_hash: str = ""


def _run_git(args: list[str], cwd: Path | None = None) -> str:
    """Roda git e retorna stdout. Erro vira exceção."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} falhou: {result.stderr}")
    return result.stdout.strip()


def _parse_hora_texto(conteudo: str) -> datetime | None:
    """Extrai a hora do texto do veredito. Retorna None se não houver."""
    # Formato dd/mm/aaaa HH:MM [±ZZZZ]
    m = RE_DATA_DDMMYYYY_HHMM.search(conteudo)
    if m:
        dia, mes, ano = m.group(1).split("/")
        hh, mm = int(m.group(2)), int(m.group(3))
        tz_str = m.group(4)
        if tz_str:
            sign = 1 if tz_str[0] == "+" else -1
            tz = timezone(timedelta(hours=sign * int(tz_str[1:3]), minutes=sign * int(tz_str[3:5])))
        else:
            tz = BRT
        return datetime(int(ano), int(mes), int(dia), hh, mm, tzinfo=tz)

    # Formato extenso: "sáb, 3 de out de 2026 13:19:15"
    m = RE_DATA_EXTENSO.search(conteudo)
    if m:
        ano = int(m.group(1))
        hh = int(m.group(2))
        mm = int(m.group(3))
        ss = int(m.group(4))
        # Mapeamento de meses em português
        meses = {
            "jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
            "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12,
        }
        # Extrai o mês do texto
        m_mes = re.search(r"de\s+(\w+)\s+de", conteudo[conteudo.index("Data:"):])
        mes = meses.get(m_mes.group(1)[:3].lower(), 10) if m_mes else 10
        # Extrai o dia
        m_dia = re.search(r"Data:\s*\w+,?\s+(\d+)\s+de", conteudo)
        dia = int(m_dia.group(1)) if m_dia else 1
        return datetime(ano, mes, dia, hh, mm, ss, tzinfo=BRT)

    return None


def _autor_date(hash: str, cwd: Path | None = None) -> datetime:
    """Data do autor (%ai) de um commit."""
    out = _run_git(["log", "-1", "--format=%ai", hash], cwd=cwd)
    # Formato: 2026-10-03 13:19:15 -0300
    return datetime.fromisoformat(out)


def _commit_existe(hash: str, cwd: Path | None = None) -> bool:
    """Verifica se um hash existe no repo."""
    try:
        _run_git(["cat-file", "-e", hash], cwd=cwd)
        return True
    except RuntimeError:
        return False


def _arquivo_mtime(caminho: Path) -> datetime:
    """Data de modificação do arquivo como datetime com tz BRT."""
    import os
    ts = os.path.getmtime(caminho)
    return datetime.fromtimestamp(ts, tz=BRT)


def verificar_veredito(
    arquivo: Path,
    hora_commit: datetime | None = None,
    git_cwd: Path | None = None,
) -> VereditoCheck:
    """Verifica um arquivo de veredito.

    Args:
        arquivo: caminho do arquivo veredito.
        hora_commit: hora do commit (para pre-commit, usar datetime.now(BRT)).
                     Se None, usa mtime do arquivo.
        git_cwd: diretório do repo git (default: cwd atual).
    """
    if git_cwd is None:
        git_cwd = Path.cwd()

    conteudo = arquivo.read_text(encoding="utf-8")
    nome = arquivo.name

    # 1. Linha Objeto é obrigatória
    m_obj = RE_OBJETO.search(conteudo)
    if not m_obj:
        return VereditoCheck(
            arquivo=nome,
            ok=False,
            motivo="veredito sem linha 'Objeto: <caminho> @ <hash>'",
        )
    objeto_caminho = m_obj.group(1)
    objeto_hash = m_obj.group(2)

    # 2. Hash tem de existir
    if not _commit_existe(objeto_hash, cwd=git_cwd):
        return VereditoCheck(
            arquivo=nome,
            ok=False,
            motivo=f"hash do objeto não existe: {objeto_hash}",
            objeto_caminho=objeto_caminho,
            objeto_hash=objeto_hash,
        )

    # 3. Hora do objeto (autor date)
    try:
        hora_objeto = _autor_date(objeto_hash, cwd=git_cwd)
    except RuntimeError as e:
        return VereditoCheck(
            arquivo=nome,
            ok=False,
            motivo=f"não foi possível ler a data do objeto: {e}",
            objeto_caminho=objeto_caminho,
            objeto_hash=objeto_hash,
        )

    # 4. Hora do veredito: texto > commit/mtime
    hora_texto = _parse_hora_texto(conteudo)
    if hora_commit is None:
        hora_commit = _arquivo_mtime(arquivo)

    hora_veredito = hora_texto if hora_texto else hora_commit

    # 5. Veredito tem de ser posterior ao objeto
    if hora_veredito < hora_objeto:
        return VereditoCheck(
            arquivo=nome,
            ok=False,
            motivo=(
                f"veredito anterior ao objeto: "
                f"veredito={hora_veredito:%d/%m/%Y %H:%M} < "
                f"objeto={hora_objeto:%d/%m/%Y %H:%M}"
            ),
            hora_texto=hora_texto,
            hora_commit=hora_commit,
            objeto_caminho=objeto_caminho,
            objeto_hash=objeto_hash,
        )

    # 6. Hora no texto não pode ser > commit + 2 min
    if hora_texto and hora_texto > hora_commit + TOLERANCIA:
        return VereditoCheck(
            arquivo=nome,
            ok=False,
            motivo=(
                f"hora no texto posterior ao commit + 2min: "
                f"texto={hora_texto:%d/%m/%Y %H:%M} > "
                f"commit={hora_commit:%d/%m/%Y %H:%M} + 2min"
            ),
            hora_texto=hora_texto,
            hora_commit=hora_commit,
            objeto_caminho=objeto_caminho,
            objeto_hash=objeto_hash,
        )

    return VereditoCheck(
        arquivo=nome,
        ok=True,
        hora_texto=hora_texto,
        hora_commit=hora_commit,
        objeto_caminho=objeto_caminho,
        objeto_hash=objeto_hash,
    )


def _eh_veredito(caminho: str) -> bool:
    """Verifica se o nome do arquivo é um veredito."""
    nome = Path(caminho).name.lower()
    return any(p in nome for p in VEREDITO_PATTERNS) and caminho.endswith(".md")


def run_pre_commit(git_cwd: Path | None = None) -> int:
    """Modo pre-commit: verifica arquivos staged. Retorna 0 (ok) ou 1 (rejeita)."""
    if git_cwd is None:
        git_cwd = Path.cwd()

    # Lista arquivos staged
    out = _run_git(["diff", "--cached", "--name-only", "--diff-filter=ACM"], cwd=git_cwd)
    if not out:
        return 0

    arquivos = [f for f in out.splitlines() if _eh_veredito(f)]
    if not arquivos:
        return 0

    agora = datetime.now(BRT)
    falhas = 0
    for arq in arquivos:
        caminho = git_cwd / arq
        if not caminho.exists():
            continue
        result = verificar_veredito(caminho, hora_commit=agora, git_cwd=git_cwd)
        if not result.ok:
            print(f"VEREDITO RECUSADO: {arq}", file=sys.stderr)
            print(f"  Motivo: {result.motivo}", file=sys.stderr)
            falhas += 1
        else:
            print(f"veredito ok: {arq}")

    return 1 if falhas else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Hook de veredito")
    parser.add_argument("--pre-commit", action="store_true", help="Modo pre-commit")
    parser.add_argument("arquivo", nargs="?", help="Arquivo de veredito para verificar")
    args = parser.parse_args()

    if args.pre_commit:
        return run_pre_commit()

    if args.arquivo:
        result = verificar_veredito(Path(args.arquivo))
        if result.ok:
            print(f"OK: {result.arquivo}")
            return 0
        else:
            print(f"RECUSADO: {result.arquivo}: {result.motivo}", file=sys.stderr)
            return 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
