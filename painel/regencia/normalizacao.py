"""Normalização tabela-dirigida do veredito e as formas de "sem fonte" e "defasado".

Regras **puras** (corte hexagonal do plano 072, §1): nada aqui importa `http.server`,
`sqlite3` nem `chamados`, e nada abre arquivo. O adaptador HTTP chama estas funções; elas não
sabem de rota, de banco nem de disco.

- FR10 — `normaliza(valor, erros=None)`: o veredito do arquivo de gate vira um canônico
  (`aprovado`/`devolvido`/`vermelho provado`/`em curso`/`inválido`) **ao lado** do original; o
  arquivo nunca é reescrito (anti-regra 6).
- FR22 — `sem_fonte(motivo, caminho="")`: a forma única de dizer "não há fonte" (nunca "0",
  nunca "n/a").
- FR25 — `aviso_ingestao(ingerido_em, agora=None)`: "defasado" quando a ingestão é antiga.
"""
from __future__ import annotations

import datetime as dt

# Tabela fixa (FR10). O valor é lido exatamente como está no cabeçalho do gate.
_TABELA = {
    "APPROVE": "aprovado",
    "OK": "aprovado",
    "PASSA": "aprovado",
    "PASSOU": "aprovado",
    "RETURN": "devolvido",
    "REPROVE": "devolvido",
    "FALHA": "devolvido",
    "FALHA_ESPERADA": "vermelho provado",
    "PENDENTE": "em curso",
    "REPRODUZIDO": "em curso",
}

# Selos de idade (FR23). `registro` = timestamp de registro/relógio; `declarada` = data digitada
# à mão em arquivo; `relogio` = lida do relógio do sistema agora.
SELO_REGISTRO = "registro"
SELO_RELOGIO = "relogio"
SELO_DECLARADA = "declarada"


def normaliza(valor, erros=None):
    """FR10: devolve `{canonico, original, motivo?}`.

    Cabeçalho reprovado pelo conferidor (`erros` não vazio) → `inválido`, com o original
    preservado. Qualquer valor fora da tabela cai em `inválido` **com o original visível**.
    """
    original = "" if valor is None else (valor if isinstance(valor, str) else str(valor))
    if erros:
        motivo = "; ".join(str(e) for e in erros) if isinstance(erros, (list, tuple)) else str(erros)
        return {"canonico": "inválido", "original": original,
                "motivo": f"cabeçalho reprovado pelo conferidor: {motivo}"}
    canonico = _TABELA.get(original.strip().upper())
    if canonico is None:
        return {"canonico": "inválido", "original": original,
                "motivo": f"veredito fora da tabela: {original!r}"}
    return {"canonico": canonico, "original": original}


def sem_fonte(motivo, caminho=""):
    """FR22: `"— (motivo: …, caminho: …)"`. Sempre com o motivo; nunca "0" nem "n/a"."""
    texto = f"— (motivo: {motivo}"
    if caminho:
        texto += f", caminho: {caminho}"
    return texto + ")"


def parse_instante(quando):
    """ISO-8601 tolerante (aceita o formato do cabeçalho de gate e o `-0300` colado)."""
    if isinstance(quando, dt.datetime):
        return quando
    if not quando or not isinstance(quando, str):
        return None
    s = quando.strip()
    try:
        return dt.datetime.fromisoformat(s)
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M %z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return dt.datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def aviso_ingestao(ingerido_em, agora=None):
    """FR25: "defasado …" quando a ingestão tem mais de 1 h; falsy (``""``) quando fresca."""
    t = parse_instante(ingerido_em)
    if not t:
        return ""
    agora = agora or dt.datetime.now(t.tzinfo) if t.tzinfo else (agora or dt.datetime.now())
    if t.tzinfo and not agora.tzinfo:
        agora = agora.replace(tzinfo=t.tzinfo)
    idade = agora - t
    if idade.total_seconds() > 3600:
        h, resto = divmod(int(idade.total_seconds()), 3600)
        m = resto // 60
        return f"defasado: ingestão de há {h} h {m} min"
    return ""
