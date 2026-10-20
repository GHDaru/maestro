# Painel de coordenação do Maestro

Um painel leve (Python stdlib + um `index.html`, só em localhost) que mostra o que cada agente está fazendo, o fluxo das peças com evidência, specs, decisões, DORA, barra, desvios, tempo por fase, higiene do git, documentos do projeto e o estado derivado de cada sessão para a IA.

Os arquivos do projeto são a fonte de verdade. O SQLite é uma projeção reconstruível. Só os fatos que não existem em arquivo (status, transição de peça, deploy, incidente) entram direto, numa tabela que só aceita inclusão.

```
python painel/server.py painel/projetos/hindiana.json            # http://127.0.0.1:8765
python painel/ingest.py painel/projetos/hindiana.json            # reconstrói o cache
python painel/registrar.py painel/projetos/hindiana.json status --sessao W04 --estado trabalhando --texto "..." --autor Assistente
python painel/registrar.py painel/projetos/hindiana.json peca --peca P6 --estado "suites aceitas" --evidencia '{"hash":"…","runner2":"…"}' --autor Office
python painel/registrar.py painel/projetos/hindiana.json deploy --estado SUCCESS --evidencia '{"hash":"…"}' --autor Office
python -m unittest discover -s painel/tests
```

Para aplicar a outro projeto, copie `projetos/hindiana.json` e ajuste os caminhos.

- Proposta e documentos exigidos: `docs/proposta.md`
- ADR: `docs/adr-rascunho-painel.md`
- Roteiro do painel de especialistas: `docs/roteiro-painel.md`
