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
7. Se existe linha Data: e o formato não é reconhecido, recusa.
8. Standalone/painel: hora do commit = author date de `git log -1 --format=%ai -- <arquivo>`.

Uso:
  pre-commit:  python veredito_hook.py --pre-commit
  standalone:   python veredito_hook.py <arquivo>
  test:         python -m pytest test_veredito_hook.py
"""
from __future__ import annotations

import argparse
import os
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

# Sentinel para formato não reconhecido
UNRECOGNIZED = "UNRECOGNIZED"

# Padrões de arquivo de veredito
VEREDITO_PATTERNS = ("veredito", "critica")

# Mapeamentos de meses
MESES_PT = {
    "jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
    "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12,
}
MESES_EN = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

# Regex para linha Objeto
RE_OBJETO = re.compile(r"^Objeto:\s*(.+?)\s+@\s+([0-9a-f]{7,40})\s*$", re.MULTILINE)

# Prefixo comum: aceita **Data:** e Data:
_DATA_PREFIX = r"\*{0,2}Data:\*{0,2}\s*"

# Regex para linha Data (vários formatos)
# "Data: 03/10/2026 13:19 -0300" ou "**Data:** 03/10/2026 13:19 -0300"
RE_DATA_DDMMYYYY_HHMM = re.compile(
    _DATA_PREFIX + r"(\d{2}/\d{2}/\d{4})\s+(\d{2}):(\d{2})(?:\s*([+-]\d{4}))?",
    re.MULTILINE,
)
# "Data: 03/10/2026" (só data, sem hora)
RE_DATA_DDMMYYYY_ONLY = re.compile(
    _DATA_PREFIX + r"(\d{2}/\d{2}/\d{4})\s*$",
    re.MULTILINE,
)
# "**Data:** 2026-10-03 14:04:08 BRT"
RE_DATA_ISO_BRT = re.compile(
    _DATA_PREFIX + r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+BRT",
    re.MULTILINE,
)
# "**Data:** Sat Oct 3 16:00:00 2026"
RE_DATA_ENGLISH = re.compile(
    _DATA_PREFIX + r"\w{3}\s+(\w{3})\s+(\d{1,2})\s+(\d{2}):(\d{2}):(\d{2})\s+(\d{4})",
    re.MULTILINE,
)
# "Data: sáb, 3 de out de 2026 13:19:15"
RE_DATA_EXTENSO = re.compile(
    _DATA_PREFIX + r"\w+,?\s+\d+\s+de\s+\w+\s+de\s+(\d{4})\s+(\d{2}):(\d{2}):(\d{2})",
    re.MULTILINE,
)
# Detecta qualquer linha Data: (para distinguir "sem Data:" de "Data: não reconhecido")
RE_DATA_ANY = re.compile(
    r"\*{0,2}Data:\*{0,2}\s*\S",
    re.MULTILINE,
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


def _parse_hora_texto(conteudo: str) -> datetime | None | str:
    """Extrai a hora do texto do veredito.

    Returns:
        datetime: se parseou com sucesso (tem hora).
        None: se não há linha Data:, ou há mas só com data (sem HH:MM).
        UNRECOGNIZED: se há linha Data: mas o formato não é reconhecido.
    """
    # Se não há nenhuma linha Data:, retorna None
    if not RE_DATA_ANY.search(conteudo):
        return None

    # Formato dd/mm/aaaa HH:MM [±ZZZZ]
    m = RE_DATA_DDMMYYYY_HHMM.search(conteudo)
    if m:
        dia, mes, ano = m.group(1).split("/")
        hh, mm = int(m.group(2)), int(m.group(3))
        tz_str = m.group(4)
        if tz_str:
            sign = 1 if tz_str[0] == "+" else -1
            tz = timezone(timedelta(
                hours=sign * int(tz_str[1:3]),
                minutes=sign * int(tz_str[3:5]),
            ))
        else:
            tz = BRT
        return datetime(int(ano), int(mes), int(dia), hh, mm, tzinfo=tz)

    # Formato ISO com BRT: "2026-10-03 14:04:08 BRT"
    m = RE_DATA_ISO_BRT.search(conteudo)
    if m:
        ano = int(m.group(1))
        mes = int(m.group(2))
        dia = int(m.group(3))
        hh = int(m.group(4))
        mm = int(m.group(5))
        ss = int(m.group(6))
        return datetime(ano, mes, dia, hh, mm, ss, tzinfo=BRT)

    # Formato inglês: "Sat Oct 3 16:00:00 2026"
    m = RE_DATA_ENGLISH.search(conteudo)
    if m:
        mes = MESES_EN.get(m.group(1).lower()[:3])
        if mes:
            dia = int(m.group(2))
            hh = int(m.group(3))
            mm = int(m.group(4))
            ss = int(m.group(5))
            ano = int(m.group(6))
            return datetime(ano, mes, dia, hh, mm, ss, tzinfo=BRT)

    # Formato extenso: "sáb, 3 de out de 2026 13:19:15"
    m = RE_DATA_EXTENSO.search(conteudo)
    if m:
        ano = int(m.group(1))
        hh = int(m.group(2))
        mm = int(m.group(3))
        ss = int(m.group(4))
        # Extrai o mês do texto
        idx = conteudo.index("Data:")
        m_mes = re.search(r"de\s+(\w+)\s+de", conteudo[idx:])
        mes = MESES_PT.get(m_mes.group(1)[:3].lower(), 10) if m_mes else 10
        # Extrai o dia
        m_dia = re.search(r"\*{0,2}Data:\*{0,2}\s*\w+,?\s+(\d+)\s+de", conteudo)
        dia = int(m_dia.group(1)) if m_dia else 1
        return datetime(ano, mes, dia, hh, mm, ss, tzinfo=BRT)

    # Formato dd/mm/aaaa só com data (sem hora) — reconhecido, usa commit
    if RE_DATA_DDMMYYYY_ONLY.search(conteudo):
        return None

    # Linha Data: existe mas formato não reconhecido
    return UNRECOGNIZED


def _autor_date(hash: str, cwd: Path | None = None) -> datetime:
    """Data do autor (%ai) de um commit."""
    out = _run_git(["log", "-1", "--format=%ai", hash], cwd=cwd)
    # Formato: 2026-10-03 13:19:15 -0300
    return datetime.fromisoformat(out)


def _autor_date_arquivo(arquivo: Path, git_cwd: Path) -> datetime | None:
    """Author date do commit que introduziu o arquivo.

    Usa `git log -1 --format=%ai -- <arquivo>`.
    Retorna None se o arquivo não está commitado.
    """
    try:
        if arquivo.is_absolute():
            rel = str(arquivo.relative_to(git_cwd)).replace("\\", "/")
        else:
            rel = str(arquivo).replace("\\", "/")
        out = _run_git(["log", "-1", "--format=%ai", "--", rel], cwd=git_cwd)
        if not out:
            return None
        return datetime.fromisoformat(out)
    except (RuntimeError, ValueError):
        return None


def _commit_existe(hash: str, cwd: Path | None = None) -> bool:
    """Verifica se um hash existe no repo."""
    try:
        _run_git(["cat-file", "-e", hash], cwd=cwd)
        return True
    except RuntimeError:
        return False


def _arquivo_mtime(caminho: Path) -> datetime:
    """Data de modificação do arquivo como datetime com tz BRT."""
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
                     Se None (standalone), usa author date do commit que
                     introduziu o arquivo; se não commitado, usa mtime.
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

    # 4. Hora do commit: standalone usa author date, pre-commit usa valor passado
    if hora_commit is None:
        # Standalone: author date do commit que introduziu o arquivo
        hora_commit = _autor_date_arquivo(arquivo, git_cwd)
        if hora_commit is None:
            # Arquivo não commitado (pré-commit) → usa mtime
            hora_commit = _arquivo_mtime(arquivo)

    # 5. Parse da hora no texto
    hora_texto = _parse_hora_texto(conteudo)

    # 5a. Formato não reconhecido → recusa
    if hora_texto == UNRECOGNIZED:
        return VereditoCheck(
            arquivo=nome,
            ok=False,
            motivo="Data em formato não reconhecido",
            hora_commit=hora_commit,
            objeto_caminho=objeto_caminho,
            objeto_hash=objeto_hash,
        )

    # 6. Hora do veredito: texto > commit/mtime
    hora_veredito = hora_texto if hora_texto else hora_commit

    # 7. Veredito tem de ser posterior ao objeto
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

    # 8. Hora no texto não pode ser > commit + 2 min
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
