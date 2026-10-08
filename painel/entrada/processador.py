"""Processador de mensagens: liga servidor -> conversa -> repositorio (T1-05).

Stdlib only. A criacao do chamado roda em thread de trabalho;
a resposta sai em < 2 s.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Callable

from painel.entrada.banco import conectar
from painel.entrada.conversa import conversa, ESTADO_INICIO
from painel.entrada.repositorio import cria as repo_cria


def _carregar_conversa(conn: sqlite3.Connection, contato: str) -> tuple[str, dict]:
    """Carrega o estado e dados da conversa do contato, ou inicio vazio."""
    row = conn.execute(
        "SELECT estado, dados_json FROM conversas WHERE contato = ?",
        (contato,),
    ).fetchone()
    if row:
        return row[0], json.loads(row[1])
    return ESTADO_INICIO, {}


def _salvar_conversa(
    conn: sqlite3.Connection,
    contato: str,
    estado: str,
    dados: dict,
) -> None:
    """Salva (ou atualiza) o estado da conversa."""
    dados_json = json.dumps(dados, ensure_ascii=False)
    conn.execute(
        """INSERT INTO conversas (contato, estado, dados_json)
           VALUES (?, ?, ?)
           ON CONFLICT(contato) DO UPDATE SET
             estado = excluded.estado,
             dados_json = excluded.dados_json,
             atualizado_em = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
        """,
        (contato, estado, dados_json),
    )
    conn.commit()


def _criar_em_thread(
    repo_chamados: Path,
    repo_hindiana_specs: Path,
    dados: dict,
    contato: str,
    nome: str,
    empresa: str,
    callback: Callable[[dict], None] | None = None,
) -> threading.Thread:
    """Inicia a criacao do chamado em thread de trabalho."""

    def _trabalho() -> None:
        try:
            resultado = repo_cria(
                repo_chamados=repo_chamados,
                repo_hindiana_specs=repo_hindiana_specs,
                dados=dados,
                contato=contato,
                nome=nome,
                empresa=empresa,
            )
            if callback:
                callback(resultado)
        except Exception:
            # repositorio.cria ja salva em dados/pendentes/ se falhar.
            pass

    thread = threading.Thread(target=_trabalho, daemon=True)
    thread.start()
    return thread


def processar_mensagem(
    contato: str,
    nome: str,
    empresa: str,
    mensagem: str,
    db_path: Path,
    repo_chamados: Path,
    repo_hindiana_specs: Path,
) -> tuple[str, str | None, threading.Thread | None]:
    """Processa uma mensagem de um contato cadastrado.

    Returns:
        (resposta, numero_chamado_or_none, thread_or_none)
        - resposta: texto para devolver ao cliente.
        - numero_chamado: se o chamado foi confirmado (acao criar).
        - thread: thread de criacao, se disparada.
    """
    conn = conectar(db_path)
    try:
        estado, dados = _carregar_conversa(conn, contato)
        novo_estado, resposta, acao, novos_dados = conversa(estado, mensagem, dados)
        _salvar_conversa(conn, contato, novo_estado, novos_dados)
    finally:
        conn.close()

    numero_chamado: str | None = None
    thread: threading.Thread | None = None

    if acao and acao["tipo"] == "criar":
        # Reserva o numero sincronamente (rapido) para incluir na resposta.
        from painel.entrada.repositorio import _proximo_numero, _slug
        numero = _proximo_numero(repo_chamados, repo_hindiana_specs)
        slug = _slug(novos_dados.get("descricao", "chamado"))
        numero_chamado = numero
        # Substitui placeholder na resposta
        resposta = resposta.replace("#NNN", f"#{numero}")

        # Dispara criacao em thread
        thread = _criar_em_thread(
            repo_chamados=repo_chamados,
            repo_hindiana_specs=repo_hindiana_specs,
            dados=novos_dados,
            contato=contato,
            nome=nome,
            empresa=empresa,
        )

    return resposta, numero_chamado, thread
