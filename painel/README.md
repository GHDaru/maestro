# Painel de coordenação do Maestro

Um painel leve (Python stdlib + um `index.html`, só em localhost) que mostra o que cada agente está fazendo, o fluxo das peças com evidência, specs, decisões, DORA, barra, desvios, tempo por fase, higiene do git, documentos do projeto e o estado derivado de cada sessão para a IA.

Os arquivos do projeto são a fonte de verdade. O SQLite é uma projeção reconstruível. Só os fatos que não existem em arquivo (status, transição de peça, deploy, incidente) entram direto, numa tabela que só aceita inclusão.

```
python painel/server.py painel/projetos/exemplo.json            # http://127.0.0.1:8765
python painel/ingest.py painel/projetos/exemplo.json            # reconstrói o cache
python painel/registrar.py painel/projetos/exemplo.json status --sessao W04 --estado trabalhando --texto "..." --autor Assistente
python painel/registrar.py painel/projetos/exemplo.json peca --peca P6 --estado "suites aceitas" --evidencia '{"hash":"…","runner2":"…"}' --autor Office
python painel/registrar.py painel/projetos/exemplo.json deploy --estado SUCCESS --evidencia '{"hash":"…"}' --autor Office
python -m unittest discover -s painel/tests
```

Para aplicar a outro projeto, copie `projetos/exemplo.json` e ajuste os caminhos.

### Regência: a fila de decisões

Três chaves da configuração alimentam a fila de decisões (a tela **Fila** e as rotas
`/api/regencia/fila`):

- **`regencia.pessoas`** — quem pode **assinar** um *ruling* (o autor humano). Autor fora da lista
  é recusado com HTTP 422, mesmo que outro agente registre por ele.
- **`fila_decisoes`** — o endereço do registro da fila, um `JSONL` (*JavaScript Object Notation
  Lines*: uma linha `JSON` — *JavaScript Object Notation* — por registro), que só cresce
  (*append-only*, com *backup* datado antes da primeira escrita do dia). Sem a chave, o padrão é
  `painel/dados/fila-<projeto>.jsonl`.
- **`frentes`** — mapa `frente → [pastas de spec]`: a frente de um chamado é a que lista a pasta
  dele. É publicado em `/api/meta` e alimenta o filtro do kanban.

> Nota: no despacho do 072 a chave `fila_decisoes` aparecia aninhada em `regencia`; o leitor
> (`painel/fila_registro.py`, `caminho()`) a lê no **topo** da configuração — por isso ela fica no
> topo. `frentes` é um mapa, não uma lista: é o formato que `/api/meta` e o filtro consomem.

- Proposta e documentos exigidos: `docs/proposta.md`
- ADR: `docs/adr-rascunho-painel.md`
- Roteiro do painel de especialistas: `docs/roteiro-painel.md`
