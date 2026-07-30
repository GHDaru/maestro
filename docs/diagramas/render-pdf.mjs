// Renderiza os HTML de fontes/ em pdf/ usando o Chromium já presente (Playwright).
// Uso: (cd docs/diagramas && node render-pdf.mjs)
// Requer: playwright-core instalado; um Chromium em CHROME_PATH ou no caminho padrão pw.
import { chromium } from 'playwright-core';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CHROME = process.env.CHROME_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

// slides = 16:9 fixo; docs = largura fixa, altura medida (página única, sem clipe).
const JOBS = [
  { in: 'fontes/01-definicao.html',        out: 'pdf/01-definicao.pdf',        mode: 'slide', w: 1280, h: 720 },
  { in: 'fontes/02-problema-solucao.html', out: 'pdf/02-problema-solucao.pdf', mode: 'slide', w: 1280, h: 720 },
  { in: 'fontes/03-fluxo.html',            out: 'pdf/03-fluxo.pdf',            mode: 'doc',   w: 1240 },
  { in: 'fontes/04-sipoc.html',            out: 'pdf/04-sipoc.pdf',            mode: 'doc',   w: 1320 },
];

const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
for (const job of JOBS) {
  const ctx = await browser.newContext({
    colorScheme: 'dark',
    viewport: { width: job.w, height: job.mode === 'slide' ? job.h : 900 },
  });
  const page = await ctx.newPage();
  await page.emulateMedia({ media: 'screen', colorScheme: 'dark' });
  await page.goto('file://' + path.join(HERE, job.in), { waitUntil: 'networkidle' });
  await page.waitForTimeout(400); // deixa a animação de traço assentar no quadro final

  const h = job.mode === 'slide'
    ? job.h
    : await page.evaluate(() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight));

  await page.pdf({
    path: path.join(HERE, job.out),
    width: `${job.w}px`, height: `${h}px`,
    printBackground: true, pageRanges: '1',
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });
  console.log(`ok: ${job.out} (${job.w}x${h})`);
  await ctx.close();
}
await browser.close();
console.log('done');
