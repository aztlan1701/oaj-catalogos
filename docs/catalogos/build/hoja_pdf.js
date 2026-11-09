// Genera la hoja de valor en PDF etiquetado (accesible) desde su fuente HTML.
// Uso: node hoja_pdf.js [--png]   →  ../entregables/Hoja-de-valor.pdf  (y PNG de vista previa con --png)
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const raiz = path.resolve(__dirname, '..');
  const fuente = 'file://' + path.join(raiz, 'fuentes', 'Hoja-de-valor.html');
  const salida = path.join(raiz, 'entregables', 'Hoja-de-valor.pdf');
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage();
  await pagina.goto(fuente, { waitUntil: 'networkidle' });
  await pagina.evaluate(() => document.fonts.ready);
  await pagina.pdf({ path: salida, format: 'A4', printBackground: true, preferCSSPageSize: true, tagged: true, outline: true });
  console.log('PDF:', path.relative(raiz, salida));
  if (process.argv.includes('--png')) {
    const vista = await navegador.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1 });
    await vista.goto(fuente, { waitUntil: 'networkidle' });
    await vista.screenshot({ path: path.join(raiz, 'vista-previa', 'Hoja-de-valor.png'), fullPage: true });
  }
  await navegador.close();
})();
