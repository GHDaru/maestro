# Longrun do ciclo 066 — estado e pendências do Darú

> Escrito em 19/10/2026 23:30 pela sessão MAESTRO, quando o Darú foi descansar. Regras do
> longrun: parar em **90 % do consumo semanal** (medido por `get_usage`; estava em 68 %);
> acordador **PACE** a cada 30 min (cron `db780fb2`, expira em 7 dias); nada que dependa do
> Darú é decidido por mim — vai para a lista abaixo. Toda decisão passa por especialistas em
> contexto fresco e é registrada em `docs/records/decisoes.jsonl`.

## 1. O que está feito

| Item | Estado |
|---|---|
| Ciclos 064 (capa) e 065 (livro de ponto) | promovidos à `main` `af6fd1b`, CI verde |
| 42 branches da linha paralela (`DriveD\maestro`) | **publicadas no GitHub** (autorizado pelo Darú) |
| Plano de integração da linha paralela (Opus) | pronto, em `plano-integracao-linha-paralela.md` |
| Jira como barra | site `ghdaru.atlassian.net`, projeto **Painel de Regencia (REG)**, quadro 2, colunas G0–G9 |
| Decisão "sessões via gateway" | `decisao-066-sessoes-via-gateway` (3 pareceres: guardião, segurança, guia) |
| Insumos do Hindiana (Assistente + agente explorador) | `insumo-hindiana.md` |

## 2. Pendências do Darú (nada disso é feito sem você)

1. **Token do gateway MaaS fora do repositório.** Ponha `ANTHROPIC_AUTH_TOKEN` no bloco `env`
   de `~/.claude/settings.json` (escopo de usuário). Eu não escrevo o token: o classificador
   bloqueou e os três pareceres concordam que é sua decisão (segredo = leitura sensível).
2. **Ids de modelo no gateway.** Confirme os nomes aceitos (o Hindiana usa `glm-5.3`, `glm-5.2`,
   `deepseek-v4.1-flash`; você pediu "deepseek 4.4 flash"). Eu não sondo o gateway.
3. **Aceitabilidade do gateway (ADR).** Residência `ap-southeast-1`, LGPD se dados da Hindiana
   passarem por ele; robustez a prompt injection desconhecida. Recomendação: aceitar para o
   painel do Maestro (código público), **não** para dados pessoais da Hindiana.
4. **Allowlist das 7 sessões.** Aprovar a lista mínima proposta em `pareceres-…md` §2
   (deny: git push, gh, rm -rf, Remove-Item, docs/records, docs/adr, .env, settings.local.json;
   uma worktree por Worker; só o Gerente faz push, e só após o seu gate).
5. **Plano de integração — decisões 1–5 e 9 do plano** (resumo): `painel/` e `.maestro/`
   entram no `boundary.json`? 068 e 069 (WhatsApp, receptor) vão para o repo da Hindiana?
   Trocar dados reais da Hindiana por fixture (o repo é público)? 066-custeio vira só insumo?
   Mover `scripts/hooks/workflow_*.py` para `painel/hooks/`? Apagar as branches remotas
   depois das tags `arquivo/paralela/*`?
6. **Numeração final.** O plano propõe 066 = painel v0 … 072 = painel de regência. O esqueleto
   local `specs/066-painel-de-regencia` será renumerado quando você aprovar o mapa.
7. **Jira:** o quadro REG está vazio; se quiser cartões de exemplo (um chamado por coluna),
   autorize — é escrita na sua conta.
8. **TAIL:gate** de cada ciclo integrado é seu, por ciclo.

## 3. O que eu faço sozinho no longrun (reversível, dentro do repositório)

- Spec, plan (Constitution Check) e tasks do **primeiro ciclo da integração** (painel v0 +
  ADR 0022 a partir do rascunho), em branch própria, **sem merge**.
- Tags `arquivo/paralela/<branch>` nas 42 pontas — **locais**, sem push.
- `ux-design.md` do painel de regência (agente `ux-semantics`), a partir dos insumos.
- Portões rodados e registrados; nada promovido.
- Respostas ao PACE a cada 30 min, com consumo medido.

## 4. Como retomar

Branch `066-painel-de-regencia`. Leia este arquivo, depois `plano-integracao-linha-paralela.md`
e `pareceres-sessoes-via-gateway.md`. Decida a seção 2 na ordem; a 1 e a 4 destravam as sessões.
