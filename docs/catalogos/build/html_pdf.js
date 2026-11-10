// Convierte una pieza diseñada en HTML (fuentes/<Pieza>.html) en PDF etiquetado y accesible.
//
// Uso (desde docs/catalogos/build):
//   node html_pdf.js ../fuentes/<Pieza>.html            → ../entregables/<Pieza>.pdf
//   node html_pdf.js ../fuentes/<Pieza>.html --png      → además ../vista-previa/<Pieza>-<n>.png (una por página)
//   node html_pdf.js ../fuentes/<Pieza>.html --borrador → el PDF va a ../vista-previa/ en lugar de ../entregables/
//
// Encabezado y pie con número de página (modelo de flujo): la pieza los declara en su <head>
//   <meta name="pdf-encabezado" content="Registro de catálogos · Guía">
//   <meta name="pdf-pie" content="Borrador para revisión · no vigente">
// y este script agrega cajas de margen de @page («Página X de Y») con la tipografía del kit.
// Se usan cajas de margen CSS y no displayHeaderFooter porque estas respetan las páginas con
// nombre: no se dibujan sobre las páginas fijas (.page, margen 0) ni sobre .portada-flujo,
// mientras que displayHeaderFooter se encima a ellas. Sin las <meta>, no hay encabezado ni pie.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { generar: generarIconos } = require('./generar_iconos.js');

const RAIZ = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const fuenteArg = args.find((a) => !a.startsWith('--'));
if (!fuenteArg) {
  console.error('Uso: node html_pdf.js ../fuentes/<Pieza>.html [--png] [--borrador]');
  process.exit(2);
}
const fuente = path.resolve(process.cwd(), fuenteArg);
if (!fs.existsSync(fuente)) { console.error('No existe: ' + fuente); process.exit(2); }
const pieza = path.basename(fuente, path.extname(fuente));
const dirPdf = path.join(RAIZ, args.includes('--borrador') ? 'vista-previa' : 'entregables');
const salida = path.join(dirPdf, pieza + '.pdf');
const VISTA = path.join(RAIZ, 'vista-previa');

// Texto para content: "..." de CSS.
const cadenaCss = (s) => '"' + String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, ' ') + '"';

function cssEncabezadoPie(encabezado, pie) {
  const base = 'font-family: "Source Sans 3", "Segoe UI", sans-serif; font-size: 8pt; color: #575F71;';
  const sup = encabezado
    ? `@top-left { content: "Órgano de Administración Judicial · DGETD"; ${base} font-weight: 700; color: #161A1D; vertical-align: bottom; padding-bottom: 5mm; }
       @top-right { content: ${cadenaCss(encabezado)}; font-family: "Source Code Pro", Consolas, monospace; font-size: 7.5pt; letter-spacing: .08em; text-transform: uppercase; color: #2A7370; vertical-align: bottom; padding-bottom: 5mm; }`
    : '';
  const inf = `@bottom-left { content: ${cadenaCss(pie || '')}; ${base} vertical-align: top; padding-top: 5mm; }
       @bottom-right { content: "Página " counter(page) " de " counter(pages); ${base} vertical-align: top; padding-top: 5mm; }`;
  const vacio = '@top-left { content: none; } @top-right { content: none; } @bottom-left { content: none; } @bottom-right { content: none; }';
  return `@page { ${sup} ${inf} }\n@page fija { ${vacio} }\n@page portada { ${vacio} }`;
}

(async () => {
  generarIconos();
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage();
  const avisos = [];
  pagina.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') avisos.push('consola: ' + m.text()); });
  pagina.on('pageerror', (e) => avisos.push('error de script: ' + e.message));
  pagina.on('requestfailed', (r) => avisos.push('no se pudo cargar: ' + r.url()));

  await pagina.goto('file://' + fuente, { waitUntil: 'networkidle' });
  await pagina.emulateMedia({ media: 'print' });
  await pagina.evaluate(() => document.fonts.ready);

  const info = await pagina.evaluate(() => {
    const meta = (n) => { const m = document.querySelector(`meta[name="${n}"]`); return m ? m.content.trim() : ''; };
    const fuentesError = [...document.fonts].filter((f) => f.status === 'error').map((f) => `${f.family} ${f.weight} ${f.style}`);
    const desbordes = [...document.querySelectorAll('.page')].map((p, i) => ({ i: i + 1, sobra: p.scrollHeight - p.clientHeight })).filter((d) => d.sobra > 1);
    const h1 = document.querySelectorAll('h1').length;
    const saltos = [];
    let previo = 0;
    for (const h of document.querySelectorAll('h1, h2, h3, h4, h5, h6')) {
      const n = Number(h.tagName[1]);
      if (previo && n > previo + 1) saltos.push(`${h.tagName} «${h.textContent.trim().slice(0, 40)}» después de H${previo}`);
      previo = n;
    }
    return {
      titulo: document.title, idioma: document.documentElement.lang, encabezado: meta('pdf-encabezado'), pie: meta('pdf-pie'),
      fuentesError, desbordes, h1, saltos,
      iconosSinPoner: document.querySelectorAll('[data-icono]').length,
      marcadores: document.querySelectorAll('.ph').length,
      imgSinAlt: document.querySelectorAll('img:not([alt])').length,
    };
  });

  if (info.encabezado || info.pie) await pagina.addStyleTag({ content: cssEncabezadoPie(info.encabezado, info.pie) });

  const opciones = { path: salida, format: 'A4', printBackground: true, preferCSSPageSize: true, tagged: true, outline: true };
  fs.mkdirSync(dirPdf, { recursive: true });
  await pagina.pdf(opciones);
  await navegador.close();

  // Revisión del PDF resultante
  const pdfinfo = execFileSync('pdfinfo', [salida], { encoding: 'utf8' });
  const paginas = Number((pdfinfo.match(/^Pages:\s+(\d+)/m) || [])[1]);
  const etiquetado = /^Tagged:\s+yes/m.test(pdfinfo);
  console.log(`PDF: ${path.relative(RAIZ, salida)} · ${paginas} página(s) · etiquetado: ${etiquetado ? 'sí' : 'NO'} · marcadores resaltados: ${info.marcadores}`);
  if (!etiquetado) avisos.push('el PDF no quedó etiquetado (Tagged: no)');
  if (!info.titulo) avisos.push('falta <title>');
  if (info.idioma !== 'es-MX') avisos.push(`lang="${info.idioma}" (debe ser es-MX)`);
  if (info.h1 !== 1) avisos.push(`hay ${info.h1} <h1> (debe haber exactamente uno)`);
  for (const s of info.saltos) avisos.push('salto de encabezado: ' + s);
  for (const f of info.fuentesError) avisos.push('fuente que no cargó: ' + f);
  for (const d of info.desbordes) avisos.push(`la página fija ${d.i} desborda ${d.sobra}px: el contenido se corta`);
  if (info.iconosSinPoner) avisos.push(`${info.iconosSinPoner} ícono(s) sin insertar: ¿falta <script src="diseno/iconos.js">?`);
  if (info.imgSinAlt) avisos.push(`${info.imgSinAlt} <img> sin alt`);

  if (args.includes('--png')) {
    fs.mkdirSync(VISTA, { recursive: true });
    const patron = new RegExp('^' + pieza.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '-\\d+\\.png$');
    for (const f of fs.readdirSync(VISTA)) if (patron.test(f)) fs.unlinkSync(path.join(VISTA, f));
    const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'html_pdf-'));
    execFileSync('pdftoppm', ['-png', '-r', '80', salida, path.join(tmp, 'p')]);
    const pngs = fs.readdirSync(tmp).filter((f) => f.endsWith('.png')).sort();
    for (const f of pngs) {
      const n = Number(f.match(/-(\d+)\.png$/)[1]);
      fs.copyFileSync(path.join(tmp, f), path.join(VISTA, `${pieza}-${n}.png`));
      fs.unlinkSync(path.join(tmp, f));
    }
    fs.rmdirSync(tmp);
    console.log(`PNG: vista-previa/${pieza}-1.png … ${pieza}-${pngs.length}.png`);
  }

  for (const a of avisos) console.warn('AVISO: ' + a);
})().catch((e) => { console.error(e); process.exit(1); });
