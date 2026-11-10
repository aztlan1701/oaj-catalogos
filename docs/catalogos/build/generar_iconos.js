// Genera fuentes/diseno/iconos.js a partir de los SVG de fuentes/diseno/iconos/.
// Uso: node generar_iconos.js   (html_pdf.js lo llama solo antes de cada construcción)
//
// iconos.js sustituye cada <span class="ico" data-icono="nombre"></span> por el SVG en línea,
// con aria-hidden="true". Es necesario porque <use href="archivo.svg#id"> y mask-image con
// archivos externos no funcionan en file:// con Chromium.
const fs = require('fs');
const path = require('path');

const RAIZ = path.resolve(__dirname, '..');
const DIR = path.join(RAIZ, 'fuentes', 'diseno', 'iconos');
const SALIDA = path.join(RAIZ, 'fuentes', 'diseno', 'iconos.js');

function generar() {
  const iconos = {};
  for (const f of fs.readdirSync(DIR).filter((n) => n.endsWith('.svg')).sort()) {
    const svg = fs.readFileSync(path.join(DIR, f), 'utf8');
    const m = svg.match(/<svg[^>]*>([\s\S]*?)<\/svg>/);
    if (!m) throw new Error('SVG sin contenido: ' + f);
    iconos[f.replace(/\.svg$/, '')] = m[1].trim();
  }
  const js = `// ARCHIVO GENERADO por build/generar_iconos.js a partir de fuentes/diseno/iconos/*.svg. No lo edite a mano.
// Uso en una pieza: <span class="ico" data-icono="correo"></span> y, al final del <body>,
// <script src="diseno/iconos.js"></script>. Para un ícono con significado (no decorativo),
// agregue aria-label="..." al <span>: el SVG queda con role="img" y esa etiqueta.
(function () {
  var ICONOS = ${JSON.stringify(iconos, null, 2)};
  var NS = 'http://www.w3.org/2000/svg';
  function poner() {
    var marcas = document.querySelectorAll('[data-icono]');
    for (var i = 0; i < marcas.length; i++) {
      var el = marcas[i], nombre = el.getAttribute('data-icono');
      if (!ICONOS[nombre]) { console.error('Ícono desconocido: ' + nombre); continue; }
      var svg = document.createElementNS(NS, 'svg');
      svg.setAttribute('viewBox', '0 0 24 24');
      svg.setAttribute('fill', 'none');
      svg.setAttribute('stroke', 'currentColor');
      svg.setAttribute('stroke-width', '2');
      svg.setAttribute('stroke-linecap', 'round');
      svg.setAttribute('stroke-linejoin', 'round');
      svg.setAttribute('focusable', 'false');
      svg.setAttribute('class', ('ico ' + (el.getAttribute('class') || '')).replace(/\\bico\\b\\s*/, 'ico ').trim());
      var etiqueta = el.getAttribute('aria-label');
      if (etiqueta) { svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', etiqueta); }
      else { svg.setAttribute('aria-hidden', 'true'); }
      if (el.getAttribute('style')) svg.setAttribute('style', el.getAttribute('style'));
      svg.innerHTML = ICONOS[nombre];
      el.parentNode.replaceChild(svg, el);
    }
  }
  window.ICONOS_OAJ = ICONOS;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', poner);
  else poner();
})();
`;
  const previo = fs.existsSync(SALIDA) ? fs.readFileSync(SALIDA, 'utf8') : '';
  if (previo !== js) {
    const tmp = SALIDA + '.' + process.pid + '.tmp';
    fs.writeFileSync(tmp, js);
    fs.renameSync(tmp, SALIDA); // escritura atómica: varias construcciones pueden correr a la vez
  }
  return Object.keys(iconos);
}

module.exports = { generar };
if (require.main === module) console.log('Íconos:', generar().join(', '));
