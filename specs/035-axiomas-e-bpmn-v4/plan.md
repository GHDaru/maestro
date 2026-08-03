# Plan 035 — Axiomas e BPMN v4

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-03

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes do documento; requisitos em EARS |
| II. Orquestração humano-governada | ✅ os axiomas foram pedidos e são aprovados pelo Steward |
| III. Reversibilidade / gates de risco | ✅ documento e imagem, reversíveis por revert |
| IV. Test-First / DoD verificável | ✅ cada teorema exige evidência; portões verdes antes do gate |
| V. Economia de contexto / fronteira | ✅ cinco axiomas, não quinze — o menor conjunto que sustenta |
| VI. Artefatos vivos | ✅ o BPMN é atualizado no mesmo ciclo em que a norma mudou |
| VII. Governança leve / YAGNI | ✅ a camada existe para **podar**, não para inchar |
| VIII. Comunicação inteligível | ✅ BPMN e siglas por extenso na primeira ocorrência |

## Como

1. **Derivar dos fatos, não do desejo**: cada teorema sai de algo que este repositório já
   mostrou — inclusive o que nos desabona (nove defeitos escapados com portão verde entra em
   T4 como evidência, não como nota de rodapé).
2. **Teste de independência em cada axioma** — o que quebra se ele sair. É o que separa
   axioma de slogan.
3. **Corolários amarrados a artefatos existentes** (skill, script, seção do modelo): se um
   corolário não aponta para nada, ele é retórica.
4. **BPMN**: atualizar as duas versões a partir da mesma mudança — bloco navegável no
   Markdown e fonte HTML da imagem — e regenerar o PNG com navegador real, recortando na
   altura real do conteúdo.

## Verificação (DoD)

```bash
scripts/check-language.sh   # axioms.md é instalável e está em inglês
scripts/check-links.sh      # o BPMN aponta para páginas que existem
scripts/check-cycle.sh      # raia justificada + elo do commit
node publicar/build.mjs     # 36 páginas (axiomas publicado)
node scratchpad/render-bpmn.mjs   # imagem regenerada do fonte versionado
```
