// Portão de slop: marcas de escrita gerada por IA no livro.
//
// É o Princípio IV aplicado à prosa: "prove, não declare" — o trabalho é
// **transformar julgamento em checagem**. "Este capítulo soa gerado" era
// julgamento editorial, disponível só quando alguém lia com atenção. Aqui vira
// uma função de aptidão que roda a cada build.
//
// O `fight-the-pile-up` combate o amontoado (sigla órfã, tudo numa página só);
// este portão combate o registro genérico — "esta prática desempenha um papel
// crucial no cenário em evolução da engenharia" passa hoje com tudo verde,
// porque nenhum portão olha a prosa. `check-chapters.sh` mede as nove seções e a
// datação; `check-links.sh` mede link; `build.mjs` mede slug e imagem.
//
// Roda sobre a FONTE em Markdown, antes de virar site.
//
// Escopo: o livro em português — handbook, receitas, diagramas, docs/livro e
// docs/jornada. Fora, de propósito:
//
//   docs/governance/  — está em inglês (ADR 0014) e é norma, não prosa de livro.
//   docs/research/    — notas de pesquisa que CITAM fonte externa literalmente. A
//                       única ocorrência que o portão marcaria lá é "revisão
//                       humana permanece crucial", dentro de aspas, copiada de
//                       um paper. §373 do guia de origem isenta texto de segunda
//                       mão, e um portão não distingue citação de uso.
//   docs/adr/, docs/records/, docs/ecosystem/ — memória append-only. O CLAUDE.md
//                       proíbe reescrever ADR commitado e `decisoes.jsonl`, e um
//                       `PreToolUse` recusa a reescrita. Um portão que exigisse
//                       correção ali pediria exatamente o que o repositório
//                       impede: achado sem saída legítima.
//
// ---------------------------------------------------------------------------
// O QUE ESTE PORTÃO DELIBERADAMENTE NÃO MEDE: travessão (§14 do guia de origem).
//
// A regra manda cortar todos, como restrição dura. Ela vem do "Signs of AI
// writing" da Wikipédia EM INGLÊS, onde o em dash é ornamento opcional. Em
// português é pontuação: aposto explicativo, intercalação, fala. O guia se
// desarma sozinho nesse ponto — lista "em dashes alone" entre os falsos
// positivos conhecidos.
//
// Decisão herdada do livro Teoria das Restrições (ADR 0006 de lá) e do livro
// Engenharia de Harness (ADR 0009 de lá, que mediu também o efeito no idioma
// inglês). Aqui ela vale pelo mesmo motivo, e o registro fica no ADR desta
// rodada. Quem quiser acrescentar a contagem terá de argumentar contra isto.
//
// Também fora: §16 (listas que abrem com rótulo em negrito). Foi implementada e
// medida nos repositórios irmãos, e acusou notação legítima — lista de definição
// é o caso que o próprio guia isenta. Livro de método vive disso.
//
// E §18 (emoji), que aqui foi implementada, medida e removida. Acusou 90 vezes,
// com 15 símbolos distintos, e nenhum era decoração: ⭐ marca a seção 6 do
// esqueleto editorial (o `check-chapters.sh` a remove do título ao comparar), ✨
// marca capítulo migrado para a v2 (o README explica), 🔬 👁 ⛔ é a triagem do
// panorama de templates, 🟣 🟡 🟢 🔵 🟠 são a legenda dos diagramas, ✅ ❌ 🔄 são
// coluna de status em tabela comparativa, e 📄 🎼 📐 distinguem formatos de
// download. Cada um tem legenda no próprio documento em que aparece.
//
// Uma whitelist de 15 símbolos não é regra, é inventário — e precisaria de
// manutenção toda vez que um diagrama ganhasse uma cor. No livro de Harness a
// regra sobreviveu porque lá o vocabulário é menor e está centralizado no guia
// editorial; aqui ele é uma legenda por documento. Diferença medida, não
// suposta: os dois portões divergem neste ponto de propósito.
//
// O critério que une os dois: portão com falso positivo conhecido é portão que
// se aprende a ignorar. Zero achado no texto limpo é o que faz um achado futuro
// significar alguma coisa. (É o C13 aplicado a estilo: o portão relata fato; a
// memória de quem revisa relata intenção.)
// ---------------------------------------------------------------------------
//
// Calibragem (2026-08: 32 arquivos, 3.914 linhas, ~27.300 palavras): ZERO
// achados lexicais. Dois candidatos apareceram, e os dois eram falso positivo:
//
//   "robusto"  — na receita `escrever-criterio-verificavel.md`, dentro de
//        `"o script é robusto"`: é o EXEMPLO de critério vago que a receita
//        ensina a substituir. A palavra saiu da lista nos três livros; as outras
//        duas ocorrências, no livro de Harness, eram técnicas ("o modelo de
//        estado mais robusto", "atenção robusta").
//   os 90 emojis  — nenhum decorativo; ver a nota sobre §18, acima. Custaram a
//        regra inteira.
//
// Fronteira de palavra é Unicode, não `\b`. Em JS (como em grep no locale C)
// `\b` é ASCII: `/\brico/` casa dentro de "histórico", porque "ó" não é
// [A-Za-z0-9_] e vira fronteira.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { dirname, resolve, relative } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const ESCOPO = ["docs/handbook", "docs/receitas", "docs/diagramas", "docs/livro", "docs/jornada"];

// Fronteira Unicode-aware. Todo espaço literal vira `\s+`: em Markdown a linha
// quebra onde o parágrafo mandar, e "desempenha um papel\ncrucial" é o mesmo
// slop que "desempenha um papel crucial".
const entre = (corpo) =>
  new RegExp(`(?<![\\p{L}\\p{N}_])(?:${corpo.replace(/ /g, "\\s+")})(?![\\p{L}\\p{N}_])`, "giu");

// Cada padrão cita a seção do guia de origem — para a discussão "isso é mesmo
// slop?" acontecer contra um texto, e não contra gosto pessoal — e carrega uma
// AMOSTRA-CANÁRIO que tem obrigação de acusar. O autoteste roda todos a cada
// build: expressão afrouxada quebra na hora, não seis capítulos depois.
const P = (nome, corpo, canario) => [nome, entre(corpo), canario];
const PR = (nome, re, canario) => [nome, re, canario];

const PADROES = [
  P("§1 significância inflada",
    "desempenha(?:m|ndo)? um papel (?:crucial|fundamental|vital|central|essencial)" +
    "|marca(?:ndo)? um (?:momento|marco) (?:decisivo|crucial|histórico)" +
    "|é um testemunho d[aeo]|reflete (?:uma|a) tendência mais ampla" +
    "|deixando uma marca indelével|cenário em (?:constante )?evolução" +
    "|profundamente enraizad[oa]|(?:abrindo|pavimentando) o caminho para",
    "As práticas desempenham um papel crucial no cenário em constante evolução."),

  // O tell não é o gerúndio (comum e correto em português), é a oração
  // participial PENDURADA no fim da frase para simular profundidade.
  PR("§3 gerúndio de enfeite",
    /,\s+(?:destacando|ressaltando|enfatizando|garantindo|refletindo|simbolizando|contribuindo\s+para|promovendo|fomentando|abrangendo|demonstrando|evidenciando|consolidando)(?![\p{L}\p{N}_])/giu,
    "O método reduz o retrabalho, contribuindo para uma cultura mais forte."),

  P("§4 promocional",
    "vibrante|de tirar o fôlego|imperdível|deslumbrante|renomad[oa]" +
    "|revolucionári[oa]|inigualável|incomparável|no coração d[aeo]",
    "Uma abordagem revolucionária, no coração da engenharia moderna."),

  P("§5 atribuição vaga",
    "especialistas (?:afirmam|acreditam|apontam|dizem|sugerem)" +
    "|observadores (?:apontam|notam)|relatórios do setor|alguns críticos" +
    "|muitos acreditam|é amplamente reconhecido|é sabido que" +
    "|(?:estudos|pesquisas) (?:mostram|indicam|sugerem) que",
    "Especialistas afirmam que o ganho é imediato, e estudos mostram que funciona."),

  // "fundamental", "essencial" e "robusto" ficaram DE FORA: corretas e frequentes
  // em texto técnico português. Ver a nota de calibragem no topo.
  P("§7 vocabulário de IA",
    "crucial|mergulhar (?:fundo|mais fundo)|aprimorar|abrangente" +
    "|intrincad[oa]|tapeçaria|sublinhar|fomentar|alinhar-se com" +
    "|adicionalmente|multifacetad[oa]|holístic[oa]",
    "Adicionalmente, a solução é abrangente e vai aprimorar o fluxo."),

  PR("§9 paralelismo negativo",
    /(?<![\p{L}\p{N}_])(?:não\s+(?:apenas|só|somente)[^.!?]{0,80}mas\s+(?:também|sim)(?![\p{L}\p{N}_])|não\s+se\s+trata\s+apenas\s+de)/giu,
    "Não se trata apenas de medir: não é só uma técnica, mas também uma cultura."),

  P("§20 artefato de chat",
    "espero que (?:isso )?ajude|gostaria que eu|quer que eu" +
    "|me avise se|posso (?:detalhar|expandir) (?:qualquer|alguma)",
    "Espero que isso ajude! Me avise se quiser que eu detalhe algum ponto."),

  P("§21 disclaimer de corte",
    "até (?:a )?minha última atualização|com base n[ao]s informações disponíveis" +
    "|embora (?:os )?detalhes específicos sejam (?:limitados|escassos)" +
    "|não (?:está|estão) publicamente disponí(?:vel|veis)",
    "Até minha última atualização, os dados não estão publicamente disponíveis."),

  P("§22 bajulação",
    "ótima pergunta|excelente (?:ponto|observação)|ótimo ponto|você está absolutamente cert[oa]",
    "Ótima pergunta! Você está absolutamente certo nesse ponto."),

  P("§23 filler",
    "devido ao fato de que|neste momento em que|tem a capacidade de" +
    "|é importante (?:notar|ressaltar|destacar) que" +
    "|vale (?:a pena )?(?:notar|ressaltar|destacar) que" +
    "|cabe (?:notar|ressaltar|destacar) que",
    "É importante ressaltar que o agente tem a capacidade de replanejar."),

  P("§24 hedging empilhado",
    "poderia potencialmente|pode possivelmente|talvez possa|eventualmente poderia",
    "A mudança poderia potencialmente reduzir o custo do ciclo."),

  P("§25 conclusão genérica",
    "o futuro (?:é|parece) promissor|tempos empolgantes|um passo na direção certa" +
    "|jornada rumo à excelência",
    "O futuro é promissor, e este é um passo na direção certa."),

  P("§27 autoridade retórica",
    "a (?:verdadeira|real) (?:questão|pergunta) é|em sua essência" +
    "|o que (?:realmente|de fato) importa|o cerne da questão",
    "A verdadeira questão é outra: em sua essência, o que realmente importa é o gate."),

  P("§28 sinalização",
    "vamos (?:mergulhar|explorar|destrinchar|desvendar)" +
    "|veja o que você precisa saber|sem mais delongas",
    "Vamos mergulhar no assunto. Veja o que você precisa saber."),

  P("§32 fórmula de aforismo",
    "é a linguagem d[aeo]|é a moeda d[aeo]|torna-se uma armadilha",
    "A spec é a linguagem do time, e a automação torna-se uma armadilha."),

  PR("§33 abre-conversa teatral",
    /(?:^|\n)\s*(?:honestamente\?|sinceramente\?|olha,|vamos ser honestos|verdade seja dita)/giu,
    "\nHonestamente? Depende do ciclo."),
];


const falhas = [];
const semCodigo = (t) => t
  .replace(/^```[\s\S]*?^```/gm, (m) => m.replace(/[^\n]/g, " "))
  .replace(/`[^`\n]*`/g, (m) => " ".repeat(m.length));

const varrer = (dir, acc = []) => {
  for (const d of readdirSync(dir, { withFileTypes: true })) {
    const p = resolve(dir, d.name);
    if (d.isDirectory()) varrer(p, acc);
    else if (d.name.endsWith(".md")) acc.push(p);
  }
  return acc;
};

let arquivos = 0, linhasTotal = 0;

for (const escopo of ESCOPO) {
  const base = resolve(RAIZ, escopo);
  if (!existsSync(base)) { falhas.push(`${escopo}/ não existe — o escopo do portão saiu do lugar`); continue; }
  for (const arq of varrer(base)) {
    const rel = relative(RAIZ, arq).replace(/\\/g, "/");
    arquivos++;
    const bruto = readFileSync(arq, "utf8");
    const texto = semCodigo(bruto);
    const linhas = texto.split("\n");
    const linhasBrutas = bruto.split("\n");
    linhasTotal += linhas.length;

    // Escape por linha: `<!-- slop-ok: motivo -->` na anterior. Exige motivo
    // escrito — silenciar um achado tem de custar uma frase.
    const isenta = (i) => /<!--\s*slop-ok:\s*\S+.*-->/.test(linhasBrutas[i - 1] || "");
    const posLinha = (idx) => texto.slice(0, idx).split("\n").length - 1;

    for (const [nome, re] of PADROES) {
      re.lastIndex = 0;
      for (const m of texto.matchAll(re)) {
        const i = posLinha(m.index);
        if (isenta(i)) continue;
        falhas.push(`${rel}:${i + 1}: ${nome} — ${JSON.stringify(m[0].trim())}`);
      }
    }

  }
}

// ---------------------------------------------------------------------------
// Autoteste. Um portão que nunca acusa nada é indistinguível de um portão
// quebrado, e este passa limpo — então a única prova de que as expressões
// funcionam é rodá-las contra texto que DEVE falhar.
for (const [nome, re, canario] of PADROES) {
  if (!canario) { falhas.push(`AUTOTESTE: "${nome}" sem amostra-canário`); continue; }
  re.lastIndex = 0;
  if (!re.test(canario)) falhas.push(`AUTOTESTE: "${nome}" não acusou o próprio canário — expressão afrouxada`);
  // A quebra de linha não pode salvar o slop.
  const dobrado = canario.replace(/ /g, (m, i) => (i === Math.floor(canario.length / 2) ? "\n" : m));
  re.lastIndex = 0;
  if (dobrado !== canario && !re.test(dobrado)) falhas.push(`AUTOTESTE: "${nome}" perde o achado quando a frase quebra linha`);
}
if (arquivos < 25) falhas.push(`só ${arquivos} arquivos varridos — o portão não está medindo nada`);
if (linhasTotal < 2000) falhas.push(`só ${linhasTotal} linhas analisadas — o portão não está medindo nada`);
// ---------------------------------------------------------------------------

if (falhas.length) {
  console.error(`✗ marcas de escrita de IA: ${falhas.length} achado(s)`);
  falhas.forEach((f) => console.error("   " + f));
  console.error(`\n   Cada achado é um trecho que soa gerado. Reescreva, ou — se o uso for`);
  console.error(`   legítimo — declare na linha anterior: <!-- slop-ok: motivo -->`);
  process.exit(1);
}
console.log(`✓ prosa sem marcas de IA: ${arquivos} arquivos, ${linhasTotal} linhas, ${PADROES.length} padrões (travessão fora, por decisão — ver cabeçalho)`);
