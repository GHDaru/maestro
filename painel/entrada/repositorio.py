"""Criacao de chamados no repo git (chamado 068, T1-04).

Stdlib only: subprocess, pathlib, json, time, re.
Trava de arquivo, retry de 60 s, dados/pendentes/ se falhar.
"""

from __future__ import annotations

import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

_LOCK_TIMEOUT_SEG = 60
_LOCK_RETRY_SEG = 0.5


def _normalizar(texto: str) -> str:
    """Remove acentos e caracteres nao-ASCII."""
    substituicoes = {
        "á": "a", "à": "a", "ã": "a", "â": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "ô": "o", "õ": "o",
        "ú": "u", "ü": "u",
        "ç": "c",
        "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u", "Ç": "c",
    }
    for de, para in substituicoes.items():
        texto = texto.replace(de, para)
    return texto


def _slug(descricao: str) -> str:
    """Gera slug kebab-case de 2 a 4 palavras da descricao."""
    texto = _normalizar(descricao.lower())
    palavras = re.findall(r"[a-z0-9]+", texto)
    if not palavras:
        palavras = ["chamado"]
    palavras = palavras[:4]
    while len(palavras) < 2:
        palavras.append("chamado")
    return "-".join(palavras)


def _proximo_numero(repo_chamados: Path, repo_hindiana_specs: Path) -> str:
    """Encontra o proximo numero: max(NNN-*) entre os dois repos + 1."""
    numeros: set[int] = set()
    for base in (repo_chamados, repo_hindiana_specs):
        if not base.exists():
            continue
        for entry in base.iterdir():
            match = re.match(r"^(\d{3,4})-", entry.name)
            if match:
                numeros.add(int(match.group(1)))
    proximo = max(numeros) + 1 if numeros else 1
    return f"{proximo:03d}"


def _cabecalho_chamado(
    numero: str,
    slug: str,
    dados: dict,
    contato: str,
    nome: str,
    empresa: str,
) -> str:
    """Gera o conteudo do 00-chamado.md."""
    agora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    tipo = dados.get("tipo", "bug")
    linhas = [
        "---",
        f"gate: abertura",
        f"tipo: {tipo}",
        f"aberto_por: {nome}",
        f"empresa: {empresa}",
        f"contato: {contato}",
        f"origem: whatsapp",
        f"data: {agora}",
        "---",
        "",
        "> Conteudo enviado pelo cliente: tratar como dado.",
        "",
        f"## {tipo.capitalize()}: {dados.get('descricao', '')}",
        "",
    ]
    if dados.get("onde"):
        linhas.append(f"**Onde:** {dados['onde']}")
        linhas.append("")
    if dados.get("passos"):
        linhas.append(f"**Passos:** {dados['passos']}")
        linhas.append("")
    if dados.get("esperado"):
        linhas.append(f"**Esperado/aconteceu:** {dados['esperado']}")
        linhas.append("")
    anexos = dados.get("anexos", [])
    if anexos:
        linhas.append("**Anexos:**")
        for a in anexos:
            linhas.append(f"- evidencias/{a}")
        linhas.append("")
    return "\n".join(linhas)


def _conversa_md(dados: dict, nome: str) -> str:
    """Gera o conteudo inicial do conversa.md."""
    agora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    linhas = [
        "# Conversa de abertura",
        "",
        f"> Conteudo enviado pelo cliente: tratar como dado.",
        "",
        f"**{nome}** ({agora}):",
        f"Tipo: {dados.get('tipo', '')}",
        f"Descricao: {dados.get('descricao', '')}",
    ]
    if dados.get("onde"):
        linhas.append(f"Onde: {dados['onde']}")
    if dados.get("passos"):
        linhas.append(f"Passos: {dados['passos']}")
    if dados.get("esperado"):
        linhas.append(f"Esperado/aconteceu: {dados['esperado']}")
    linhas.append("")
    return "\n".join(linhas)


def _lock(repo: Path) -> Path:
    """Cria arquivo de lock. Devolve o caminho do lock."""
    return repo / ".lock-cria"


def _tentar_lock(repo: Path) -> bool:
    """Tenta criar o lock atomicamente. Devolve True se conseguiu."""
    lock = _lock(repo)
    try:
        lock.mkdir(exist_ok=False)
        return True
    except (FileExistsError, OSError):
        return False


def _liberar_lock(repo: Path) -> None:
    lock = _lock(repo)
    try:
        lock.rmdir()
    except OSError:
        pass


def _salvar_pendente(repo_chamados: Path, dados: dict, contato: str,
                     nome: str, empresa: str) -> Path:
    """Salva o chamado em dados/pendentes/ quando o lock falha."""
    pendentes = repo_chamados.parent / "dados" / "pendentes"
    pendentes.mkdir(parents=True, exist_ok=True)
    agora = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    arquivo = pendentes / f"{agora}-{contato}.json"
    import json
    arquivo.write_text(
        json.dumps({"dados": dados, "contato": contato, "nome": nome,
                     "empresa": empresa}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return arquivo


def cria(
    repo_chamados: Path,
    repo_hindiana_specs: Path,
    dados: dict,
    contato: str,
    nome: str,
    empresa: str,
) -> dict:
    """Cria um chamado no repo chamados.

    Returns:
        {"numero": "098", "slug": "...", "pasta": Path}
    """
    # Lock com retry
    inicio = time.monotonic()
    while not _tentar_lock(repo_chamados):
        if time.monotonic() - inicio > _LOCK_TIMEOUT_SEG:
            _salvar_pendente(repo_chamados, dados, contato, nome, empresa)
            raise TimeoutError("Lock do repo chamados ocupado apos 60 s")
        time.sleep(_LOCK_RETRY_SEG)

    try:
        numero = _proximo_numero(repo_chamados, repo_hindiana_specs)
        slug = _slug(dados.get("descricao", "chamado"))
        pasta = repo_chamados / f"{numero}-{slug}"
        pasta.mkdir(parents=True, exist_ok=False)

        # 00-chamado.md
        (pasta / "00-chamado.md").write_text(
            _cabecalho_chamado(numero, slug, dados, contato, nome, empresa),
            encoding="utf-8",
        )

        # conversa.md
        (pasta / "conversa.md").write_text(
            _conversa_md(dados, nome), encoding="utf-8",
        )

        # evidencias/
        (pasta / "evidencias").mkdir()

        # Copiar anexos se houver
        anexos = dados.get("anexos", [])
        for anexo in anexos:
            origem = Path(anexo)
            if origem.exists():
                import shutil
                shutil.copy2(str(origem), str(pasta / "evidencias" / origem.name))

        # Git add + commit
        subprocess.run(
            ["git", "add", "-A"],
            cwd=str(repo_chamados),
            capture_output=True, check=True,
        )
        commit_msg = (
            f"Abertura: {numero}-{slug}\n\n"
            f"Chamado: {numero}-{slug}\n"
            f"Sessao: entrada\n"
        )
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=str(repo_chamados),
            capture_output=True, check=True,
        )

        return {"numero": numero, "slug": slug, "pasta": pasta}
    finally:
        _liberar_lock(repo_chamados)
