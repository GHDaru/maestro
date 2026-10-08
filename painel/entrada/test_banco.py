"""Testes do banco de entrada (T0-03).

Stdlib only: unittest, sqlite3, tempfile.
Roda com: python -m painel.entrada.test_banco
"""

from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from painel.entrada.banco import inicializar, conectar

_TABELAS_ESPERADAS = {"contatos", "conversas", "eventos", "notificacoes", "saida"}


class TestBancoIdempotente(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.mkdtemp()
        self.db_path = Path(self._dir) / "teste.db"

    def tearDown(self) -> None:
        # Windows: arquivos podem estar locked; best-effort.
        try:
            self.db_path.unlink(missing_ok=True)
        except OSError:
            pass
        try:
            Path(self._dir).rmdir()
        except OSError:
            pass

    def _tabelas(self, conn: sqlite3.Connection) -> set[str]:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        return {r[0] for r in rows}

    def test_cria_todas_as_tabelas(self) -> None:
        inicializar(self.db_path)
        conn = sqlite3.connect(str(self.db_path))
        tabelas = self._tabelas(conn)
        conn.close()
        self.assertTrue(_TABELAS_ESPERADAS.issubset(tabelas))

    def test_idempotente_rodar_duas_vezes(self) -> None:
        inicializar(self.db_path)
        inicializar(self.db_path)  # nao deve dar erro
        conn = sqlite3.connect(str(self.db_path))
        tabelas = self._tabelas(conn)
        conn.close()
        self.assertIn("contatos", tabelas)

    def test_conectar_cria_e_conecta(self) -> None:
        conn = conectar(self.db_path)
        tabelas = self._tabelas(conn)
        self.assertIn("eventos", tabelas)
        conn.close()

    def test_contatos_pk_contato(self) -> None:
        inicializar(self.db_path)
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            "INSERT INTO contatos (contato, telefone) VALUES (?, ?)",
            ("c-0001", "5511999999999"),
        )
        conn.commit()
        row = conn.execute(
            "SELECT contato, telefone, ativo FROM contatos WHERE contato = ?",
            ("c-0001",),
        ).fetchone()
        conn.close()
        self.assertEqual(row[0], "c-0001")
        self.assertEqual(row[1], "5511999999999")
        self.assertEqual(row[2], 1)  # ativo default

    def test_eventos_idempotencia(self) -> None:
        inicializar(self.db_path)
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            "INSERT INTO eventos (evento_id) VALUES (?)",
            ("evt-001",),
        )
        conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO eventos (evento_id) VALUES (?)",
                ("evt-001",),
            )
        conn.close()

    def test_saida_default_pendente(self) -> None:
        inicializar(self.db_path)
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            "INSERT INTO saida (texto) VALUES (?)",
            ("Chamado #001 aberto",),
        )
        conn.commit()
        row = conn.execute(
            "SELECT estado, tentativas FROM saida WHERE id = 1"
        ).fetchone()
        conn.close()
        self.assertEqual(row[0], "pendente")
        self.assertEqual(row[1], 0)

    def test_notificacoes_unique_chamado_etapa(self) -> None:
        inicializar(self.db_path)
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            "INSERT INTO notificacoes (chamado, etapa) VALUES (?, ?)",
            ("001", "T0"),
        )
        conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO notificacoes (chamado, etapa) VALUES (?, ?)",
                ("001", "T0"),
            )
        conn.close()


if __name__ == "__main__":
    unittest.main()
