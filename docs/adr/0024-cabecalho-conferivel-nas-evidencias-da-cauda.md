# ADR 0024 — Cabeçalho conferível nas evidências da cauda

- **Status**: Aceito · **Data**: 2026-10-20 · **Ciclo**: 072 (implementa; decidido no fechamento do longrun do 066)
- **Supersede**: nada; complementa `docs/governance/artifacts.md` § cauda. **Superado por**: —
- **Origem**: decisão D5 do longrun de 20/10. Três pareceres em contexto fresco: guardião do
  processo (bloqueado pelo classificador antes de responder), segurança (reversível, baixa;
  superseder por ADR), voz do método (recomenda a opção b abaixo). Os dois que responderam
  concordam que **é mudança material de método, logo o veredito é do Darú** (§ Governance, A2).
  A sessão regente redigiu; o Darú aprovou a opção (b) em 20/10 ("sim").
- **Implementação**: ciclo 072, com mutação do portão obrigatória; até lá este ADR é a regra
  escrita, não a executada.

## Contexto

O ciclo 069 trouxe para dentro do Maestro a pasta `specs/070-conferidor-ordem-veredito/` no
padrão do Hindiana: um arquivo por veredito de gate, com cabeçalho YAML (`gate`, `papel`,
`objeto @ hash`, `veredito`, `por`, `autor_da_peca`, `data`, `data_objeto`) lido por um
conferidor que recusa autor = crítico, veredito anterior ao objeto, data depois do commit do
arquivo, e escolhe o vigente pela data. A cauda atual do Maestro (quatro caixas `TAIL:*` em
`tasks.md` mais prosa em `qa-report.md`) **não amarra** o veredito ao hash julgado, não prova
por máquina que quem revisou não executou, e deixa o `check-conformance.sh` ler prosa.

Dores medidas no Hindiana (`insumo-hindiana.md`): vocabulário de veredito não unificado;
"integrado = criticado" conferido à mão; 3 de 13 vereditos técnicos errados num chamado, pegos
só por um segundo verificador. Teorema T6: a correção que não vira regra se repete.

## Opções avaliadas

- **(a) adotar os dez arquivos G0–G9 por ciclo.** Paga-se só se as dores forem do Maestro;
  G4–G9 (VM, barra, tela, aceite do cliente, ordem, pospush) não existem no fluxo Maestro —
  cerimônia sem gatilho (C1, anti-padrão 17). Dez arquivos por ciclo (A3).
- **(b) complementar: cabeçalho conferível nas linhas de evidência do `qa-report.md`.** Um
  arquivo, não dez. Cada `TAIL:*` ganha `gate, objeto @ hash, veredito, por, data`, e
  `check-conformance.sh` passa a chamar `valida()` do conferidor. Cobre autor ≠ crítico,
  veredito@hash e data por máquina. Deriva de T2 + T4 + C7.
- **(c) não adotar.** Deixa as três dores sem executável; T6 diz que repetem.

## Decisão

**(b).** A partir do ciclo 072, as quatro linhas `TAIL:*` do `qa-report.md` carregam o
cabeçalho conferível; o conferidor (`painel/chamados.py` `valida`) é chamado pelo portão; os
G0–G9 ficam convenção do Hindiana; a pasta 070 fica registrada como exceção importada.
Reavaliar (a) se dois ciclos do Maestro precisarem de gate além dos quatro.

## Consequências

- `artifacts.md` § cauda e `qa-report-template.md` ganham o cabeçalho; `check-conformance.sh`
  ganha a chamada ao conferidor (mutação obrigatória no ciclo que o fizer).
- O modelo operacional sobe de versão (MINOR).
- Elimina a duplicação de formato que o 069 abriu (Princípio VI).

## Como desfazer

Reverter o template e o portão; os cabeçalhos escritos ficam como texto válido.
