# Spec 008 — Absorções do estudo maestro-02 (+ EARS do ciclo 007)

- **Status**: Aprovada ("pode incorporar todas as sugestões") · **Raia**: Plena · **Data**: 2026-07-31
- **Origem**: Apêndice A do handbook (estudo do `maestro-02`) + ADR 0008 aprovado pelo
  Steward. Cada absorção tinha destino nomeado; este ciclo os materializa.

## O quê e por quê

Transformar as ideias **absorvidas** (não adotadas por atacado) em artefatos do Maestro:
registro de decisões consultável por máquina, retro executável, catálogo de anti-padrões,
vocabulário de gates em nível de task, medição de economia de contexto — e fechar a
absorção EARS do ciclo 007. Valor: o método ganha memória estruturada e a retro (nossa
cerimônia de maior ROI) deixa de depender de memória humana.

## Requisitos funcionais

- **FR1 — Registro auditável consultável**: `docs/registro/decisoes.jsonl` (append-only,
  1 JSON/linha: id, data, titulo, status, registro) como **índice de máquina** dos ADRs
  (a prosa continua no ADR) + `docs/registro/README.md` (protocolo) +
  `scripts/registrar-decisao.sh` (append validado; não edita linhas passadas).
  Seed: ADRs 0004–0008.
- **FR2 — Retro executável**: `scripts/retro.sh` pré-computa o material da retro a partir
  dos artefatos: ciclos e vereditos (qa-reports), gates pendentes, últimas decisões,
  inventário (agentes/skills/scripts) + as perguntas-padrão da retro. Exit 0.
- **FR3 — Skill anti-padrões**: `skills/anti-padroes/SKILL.md` — catálogo executável do
  que NÃO fazer (nossas retros + "workflow slop" do maestro-02, adaptado com crédito);
  entra no catálogo `skills/README.md`.
- **FR4 — Gates em nível de task (wave)**: seção no handbook cap. 10 nomeando o padrão
  `audit → validate → apply → verify` intra-task, com crédito ao estudo.
- **FR5 — Economia de contexto medida**: subseção no handbook cap. 04 — reportar
  estimativa de tokens do contexto fatiado vs. integral (Princípio V com número).
- **FR6 — EARS (fecha 007)**: skill `dod-verificavel` ganha a sintaxe
  `QUANDO <condição> O SISTEMA DEVE <comportamento>` como forma recomendada de critério.
- **FR7 — Rastreabilidade**: ADR 0008 → **Aceito**; Apêndice A anota "incorporado
  (spec 008)"; entrada no CHANGELOG.

## Fora de escopo

- Telemetria de custo por invocação (veredito: observar — gatilho de medição).
- Adoção de qualquer código do maestro-02 (conceitos, não vendor).

## Critérios de aceite (DoD)

- [ ] `decisoes.jsonl` com ≥5 linhas, todas JSON válido (`python3 -c json.loads` ok).
- [ ] `registrar-decisao.sh` e `retro.sh`: `bash -n` ok, `+x`, e `retro.sh` exit 0.
- [ ] `skills/*/SKILL.md` = 4; `anti-padroes` com frontmatter e gatilho "Use quando".
- [ ] `grep -l "QUANDO" skills/dod-verificavel/SKILL.md` não-vazio (EARS).
- [ ] handbook cap. 04 e 10 mencionam "economia de contexto medida" / "wave".
- [ ] ADR 0008 status Aceito; CHANGELOG com entrada em [Unreleased].

## Clarify (resolvido)

1. **JSONL onde?** `docs/registro/` (vive junto das docs; gitignore não se aplica —
   diferente do maestro-02, nosso registro é versionado: é governança, não sessão).
2. **Retro.sh lê o quê?** Só artefatos já existentes (specs/, skills/, scripts/,
   registro/) — sem estado novo.
