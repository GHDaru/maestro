"""StorePort — persistência das conversas.

Dois adaptadores: memória (dev e testes) e Postgres (Neon, produção). Sem
`DATABASE_URL`, cai para memória — o serviço sobe igual, só não lembra depois de
reiniciar. Nada de credencial no código.
"""

from __future__ import annotations

import time
from typing import Optional, Protocol

import config


class StorePort(Protocol):
    def anexar(self, sessao: str, papel: str, conteudo: str) -> None: ...
    def historico(self, sessao: str, limite: int = 20) -> list[dict]: ...
    def contar(self, sessao: str) -> int: ...
    def apagar(self, sessao: str) -> None: ...


class MemoriaStore:
    def __init__(self) -> None:
        self._dados: dict[str, list[dict]] = {}

    def anexar(self, sessao: str, papel: str, conteudo: str) -> None:
        self._dados.setdefault(sessao, []).append(
            {"papel": papel, "conteudo": conteudo, "em": time.time()}
        )

    def historico(self, sessao: str, limite: int = 20) -> list[dict]:
        return self._dados.get(sessao, [])[-limite:]

    def contar(self, sessao: str) -> int:
        return len(self._dados.get(sessao, []))

    def apagar(self, sessao: str) -> None:
        self._dados.pop(sessao, None)


class PostgresStore:
    """Neon (ou qualquer Postgres). Tabela criada na primeira subida."""

    def __init__(self, url: str) -> None:
        import psycopg  # importado só quando há banco

        self._psycopg = psycopg
        self._url = url
        with self._conectar() as con:
            con.execute(
                """CREATE TABLE IF NOT EXISTS companion_mensagens (
                       id BIGSERIAL PRIMARY KEY,
                       sessao TEXT NOT NULL,
                       papel TEXT NOT NULL,
                       conteudo TEXT NOT NULL,
                       em TIMESTAMPTZ NOT NULL DEFAULT now()
                   )"""
            )
            con.execute(
                "CREATE INDEX IF NOT EXISTS idx_companion_sessao ON companion_mensagens (sessao, id)"
            )
            con.commit()

    def _conectar(self):
        return self._psycopg.connect(self._url)

    def anexar(self, sessao: str, papel: str, conteudo: str) -> None:
        with self._conectar() as con:
            con.execute(
                "INSERT INTO companion_mensagens (sessao, papel, conteudo) VALUES (%s, %s, %s)",
                (sessao, papel, conteudo),
            )
            con.commit()

    def historico(self, sessao: str, limite: int = 20) -> list[dict]:
        with self._conectar() as con:
            linhas = con.execute(
                "SELECT papel, conteudo FROM companion_mensagens WHERE sessao = %s "
                "ORDER BY id DESC LIMIT %s",
                (sessao, limite),
            ).fetchall()
        return [{"papel": p, "conteudo": c} for p, c in reversed(linhas)]

    def contar(self, sessao: str) -> int:
        with self._conectar() as con:
            (n,) = con.execute(
                "SELECT count(*) FROM companion_mensagens WHERE sessao = %s", (sessao,)
            ).fetchone()
        return int(n)

    def apagar(self, sessao: str) -> None:
        with self._conectar() as con:
            con.execute("DELETE FROM companion_mensagens WHERE sessao = %s", (sessao,))
            con.commit()


def obter(url: Optional[str] = None) -> StorePort:
    url = config.DATABASE_URL if url is None else url
    if not url:
        return MemoriaStore()
    try:
        return PostgresStore(url)
    except Exception as e:  # banco fora do ar não derruba o serviço
        print(f"[store] Postgres indisponível ({type(e).__name__}); usando memória.")
        return MemoriaStore()
