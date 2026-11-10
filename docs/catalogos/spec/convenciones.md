# Convenciones para redactar los documentos de catálogos

Lo leen todas las personas (y agentes) que redactan piezas del paquete. Si algo aquí contradice a `registro.yaml`, manda `registro.yaml`.

## 1. Fuentes que hay que leer antes de escribir

| Archivo | Para qué |
|---|---|
| `/tmp/claude-0/-home-user-oaj-catalogos/08b8a074-abcc-5801-a910-3701b790cc2b/scratchpad/pdf/lineamientos.txt` | Texto íntegro de los Lineamientos Generales de Catálogos Institucionales (LGCI). Ignorar la cadena hash «z5Wpvq…» (sello de firma). |
| `docs/analisis-lineamientos-dgetd.md` | Obligaciones de la DGETD, vacíos (V1–V14) y entregables. |
| `docs/kit-registro/propuesta-kit-registro.html` | Narrativa, mensajes ancla, lo que se promete y lo que no, reglas de escritura. |
| `docs/catalogos/spec/registro.yaml` | Campos, preguntas, valores permitidos, claves, estatus y marcadores. **Fuente de verdad.** |

## 2. El paquete y sus códigos

| Código | Documento | Tipo |
|---|---|---|
| ET-CAT-01 | Estándar técnico de estructura, identificación, versionamiento y publicación de catálogos | Estándar técnico |
| ET-CAT-02 | Catálogo de indicadores y umbrales de calidad (ola 2) | Estándar técnico |
| PR-CAT-01 | Procedimiento de gestión del ciclo de vida de catálogos (ola 2) | Procedimiento |
| PR-CAT-02 | Procedimiento de medición y reporte de calidad (ola 2) | Procedimiento |
| PR-CAT-03 | Procedimiento simplificado para catálogos operativos o de alcance acotado (ola 3, requiere Comité) | Procedimiento |
| PR-CAT-04 | Procedimiento de registro de catálogos existentes (transitorio) | Procedimiento |
| F-CAT-01 | Registro de catálogo existente | Formato |
| F-CAT-02 | Propuesta de nuevo catálogo | Formato |
| F-CAT-03 | Diccionario de datos | Formato |
| F-CAT-04 | Dictamen técnico | Formato |
| F-CAT-05 | Solicitud de cambio estructural o retiro | Formato |
| F-CAT-06 | Bitácora de cambios menores | Formato |
| F-CAT-07 | Reporte de indicadores de calidad | Formato |
| F-CAT-08 | Plan de mejora y acciones correctivas | Formato |

Ola 1 (este paquete): ET-CAT-01 (capítulos del registro completos; el resto como estructura), PR-CAT-04, F-CAT-01 (Word y Excel), circular, guía de registro, lista de verificación para órganos jurisdiccionales y la especificación de implementación del formulario.

F-CAT-01 tiene además una versión imprimible diseñada (`fuentes/F-CAT-01-imprimible.html` → `entregables/F-CAT-01-imprimible.pdf`) que se genera desde `registro.yaml` y no se edita a mano: `cd docs/catalogos/build && python3 formato_html.py [--png]`. Sirve para preparar respuestas o para el registro acompañado; no es medio de captura. Las ayudas cortas de papel están en la tabla `AYUDA_CORTA` del script: si cambia una ayuda en `registro.yaml`, se revisa esa tabla. El script también comprueba la página del recuadro para órganos jurisdiccionales y corrige los títulos de los marcadores del PDF.

Cuando un documento cite otro que todavía no existe, se cita por su código y nombre igual.

## 3. Markdown que entiende el generador

Cada fuente es un `.md` en `docs/catalogos/fuentes/` con front matter:

```yaml
---
codigo: PR-CAT-04
titulo: Procedimiento de registro de catálogos existentes
subtitulo: Transitorio CUARTO de los Lineamientos Generales de Catálogos Institucionales
tipo: Procedimiento
version: "0.1"
fecha: "Noviembre de 2026"
estatus: Borrador para revisión · no vigente
responsable: Dirección General de Estrategia y Transformación Digital (DGETD)
fundamento: "LGCI, art. 14 fr. IX y Transitorios TERCERO y CUARTO"
portada: breve      # completa (salto de página tras la portada) · sin-ficha (sin tabla de datos: circular, lista de verificación)
---
```

- **No** escribas el título como `# Título`: la portada se genera con el front matter. Empieza con `# 1. …`.
- Títulos: `#` capítulo, `##` sección, `###` subsección, `####` etiqueta pequeña. Numera capítulos y secciones en el texto («# 3. Políticas de operación», «## 3.1 …») en documentos normativos. En la circular no numeres. (La guía de registro ya no es Markdown: es la pieza HTML `fuentes/Guia-registro.html`, §6.)
- Bloques de color (cada uno en su propio `:::`):
  - `::: {custom-style="Norma"}` lo que dice la norma (cita o paráfrasis con artículo).
  - `::: {custom-style="Compromiso"}` lo que la DGETD se compromete a hacer.
  - `::: {custom-style="Pendiente"}` decisión o dato por confirmar.
  - `::: {custom-style="Nota"}` aclaración.
  - `::: {custom-style="Alerta"}` advertencia.
  - `::: {custom-style="Pequeno"}` texto pequeño (notas al pie de tabla, fuentes).
  - `::: {custom-style="Firma"}` bloque de firma.
  - Empieza el bloque con una etiqueta en negritas: «**Lo que dice la norma.**», «**Compromiso DGETD.**», «**Por confirmar.**».
- Estilos de texto en línea:
  - `[viernes 15 de enero de 2027, por confirmar]{custom-style="Marcador"}` para todo marcador de `registro.yaml > marcadores`. Siempre resaltado, para que nadie lo publique por error.
  - `[CAT-0042]{custom-style="Clave"}` claves, folios y códigos de campo.
  - `[Obligatorio]{custom-style="Obligatorio"}` y `[Lo llena la DGETD]{custom-style="Dgetd"}` en formatos.
- Tablas: pipe tables. **El ancho de cada columna es proporcional a los guiones de la línea separadora**; reparte los guiones con intención (una columna «No.» necesita al menos 6 guiones; una de texto largo, 40 o más). Sin celdas combinadas. Agrega título con `: Título de la tabla` en la línea siguiente a la tabla, separado por una línea en blanco.
- Imágenes: `![Texto alternativo completo](img/archivo.png){width=100%}`. Toda imagen con texto alternativo que describa lo que muestra. Los diagramas llevan además, debajo, los mismos pasos en texto. Guárdalas en `docs/catalogos/fuentes/img/`. Para un diagrama, escribe un SVG o HTML y conviértelo a PNG con Playwright (`require('playwright')`, `deviceScaleFactor: 2`), usando la paleta y Source Sans 3.
- Nada de HTML crudo, ni `\n`, ni saltos de página manuales salvo `portada: completa`.

Construir y revisar:

```bash
cd docs/catalogos/build
python3 construir.py ../fuentes/PR-CAT-04.md --pdf      # docx en ../entregables, pdf en ../vista-previa
pdftoppm -jpeg -r 60 ../vista-previa/PR-CAT-04.pdf /tmp/claude-0/-home-user-oaj-catalogos/08b8a074-abcc-5801-a910-3701b790cc2b/scratchpad/PR-CAT-04
```

Mira las páginas (herramienta Read sobre los .jpg) y corrige lo que se vea mal: tablas apretadas, títulos huérfanos, bloques que no se distinguen.

## 4. Voz y estilo

- **Normativos (ET, PR, F):** registro institucional, impersonal pero claro. Oraciones de 15 a 25 palabras. Voz activa con sujeto visible: «La DGETD asigna…», «El área registra…». Nada de «se deberá proceder a la realización de». Citas: «artículo 8, fracción VII, de los Lineamientos» la primera vez en cada capítulo; después «art. 8 fr. VII».
- **Piezas para las áreas (circular, guía, lista de verificación):** «usted» y «su área» para quien lee; «nosotros» o «la DGETD» para la DGETD. Nunca tuteo. Lo importante primero; el fundamento al final o en una nota.
- Siempre: primero la palabra de todos los días y después el término normativo entre paréntesis («quién mantiene la lista (custodio)»). Fechas exactas con día de la semana, siempre como marcador mientras no se confirmen. Cifras con número arábigo. Desarrolla cada sigla la primera vez en cada documento. «Personas servidoras públicas», «la persona titular»; sin diagonales ni arrobas.
- Distingue tres tipos de afirmación y no las mezcles:
  1. **Lo que los Lineamientos obligan** (se cita como hecho, con artículo).
  2. **Lo que permiten pero no aseguran** («podrá», «preferentemente», «promoverá», o lo que depende de una Plataforma no verificada). Se dice como posibilidad.
  3. **Lo que la DGETD se compromete** (va en bloque «Compromiso»). Solo los de `propuesta-kit-registro.html` > «Lo que la DGETD firma»: acuse con folio, clave asignada, prellenado de lo que conoce, persona de contacto con nombre, no volver a pedir lo ya entregado (solo solicitudes de la DGETD), correcciones sin costo hasta el dictamen. Los plazos de la ficha de confirmación y de respuesta a dudas van como marcador «por definir».

### Frases prohibidas (no pasaron la revisión)

- «autoridad reconocida», «cifras que cuadran» como resultado del registro.
- «ningún cambio por sorpresa», «nunca se le pedirá dos veces» (solo: «la DGETD no le volverá a pedir lo que ya entregó»).
- «si no se registra, queda fuera del aviso».
- «no hay sanciones», «no se usará con fines punitivos» (solo: «el registro no es una auditoría; los errores se corrigen sin costo hasta el dictamen; en la transición la DGETD informará la calidad en cifras agregadas»).
- Cifras de consultoras (Gartner, etc.), X-Road, GOV.UK Registers como modelo.
- Tiempos de llenado («15 minutos») antes del piloto: usar «el tiempo se medirá en el piloto» o marcador.
- Adjetivos de folleto: robusto, integral, de vanguardia, sinergia, potenciar, empoderar.
- «La DGETD será custodio», «la DGETD mantendrá su lista» (es «preferentemente» y lo decide el Comité).

## 5. Datos y supuestos comunes

- Fechas (todas por confirmar, vacío V1): publicación supuesta 16/10/2026; entrada en vigor 17/10/2026; formatos (TERCERO) miércoles 16/12/2026; registro (CUARTO) viernes 15/01/2027; plan aprobado (QUINTO) domingo 14/02/2027.
- Propuesta: publicar F-CAT-01 y PR-CAT-04 antes del resto del paquete (fines de noviembre de 2026), para ampliar la ventana real de registro.
- Canales: formulario en línea (Microsoft Forms de grupo → lista de SharePoint «Inventario de catálogos»), plantilla de Excel para más de 5 listas (se sube a carpeta de SharePoint, no por correo) y registro acompañado por Teams o teléfono.
- Órganos jurisdiccionales: la comunicación llega por el conducto institucional del OAJ, no por oficio de la DGETD a personas juzgadoras. Si el órgano no lleva listas propias, no tiene que hacer nada más (confirmarlo es opcional, un clic, sin seguimiento).
- La «Plataforma de Acceso a la Información Institucional» no está verificada (vacío V2). No prometas nada que dependa de ella.
- Ejemplos: usa los del `registro.yaml` (inmuebles, órganos, tipos de documento, sentidos de resolución). Cualquier ejemplo de «el mismo órgano escrito de varias formas» se marca como ilustrativo.

## 6. Piezas diseñadas en HTML

**Cuándo.** Piezas para las áreas y resúmenes visuales: hoja de valor, guía visual, lista de verificación, carta, ficha de ejemplo, versión imprimible del formato. Los documentos normativos (ET, PR) siguen en Markdown (§3). Referencia visual: `fuentes/Hoja-de-valor.html`. Pieza de flujo con portada fija ya hecha: `fuentes/Guia-registro.html` (guía de registro, 8 páginas; sustituye a la antigua `Guia-registro.md` y a su `.docx`). Muestra de todos los componentes: `fuentes/diseno/galeria.html` (PDF en `vista-previa/galeria.pdf`).

**Archivos.** La pieza vive en `fuentes/<Pieza>.html`, enlaza el kit y carga los íconos al final del `<body>`:

```html
<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<title>Título de la pieza</title>
<meta name="pdf-encabezado" content="Registro de catálogos · Guía">   <!-- solo modelo de flujo; opcional -->
<meta name="pdf-pie" content="Borrador para revisión · no vigente">     <!-- solo modelo de flujo; opcional -->
<link rel="stylesheet" href="diseno/kit.css">
<style>/* CSS particular de la pieza */</style>
</head>
<body> … <script src="diseno/iconos.js"></script></body>
</html>
```

**Regla:** las piezas NO editan `diseno/kit.css` ni `diseno/iconos.js` (este se genera). Lo particular va en el `<style>` de la pieza, usando los tokens (`var(--mint-ink)`, `var(--t-chico)`…). Si falta un componente que servirá a varias piezas, se pide a quien mantiene el kit.

**Dos modelos de página (A4).**
- `<article class="page">`: página fija de 210 × 297 mm, sin márgenes de impresora. Para piezas de 1 o 2 páginas. Dentro: `.cabecera`, `.portada`, `.cuerpo`, `.pie`. Lo que no cabe se corta: el script avisa «la página fija N desborda».
- `<main class="flujo">`: texto continuo con márgenes de `@page` (22/18/20 mm), saltos controlados y encabezado y pie con «Página X de Y» si la pieza declara las `<meta>` `pdf-encabezado` o `pdf-pie`. Se pueden combinar: las páginas fijas y `.portada-flujo` nunca llevan encabezado ni pie.

**Clases** (ejemplos de uso en la galería):

| Clase | Uso |
|---|---|
| `.cabecera` · `.marca` | Barra superior de página fija: «Órgano de Administración Judicial · DGETD» con el cuadro menta. |
| `.portada` (`.sola`) | Portada de página fija: texto + figura a dos columnas (`.sola`: una columna). `h1 em` pinta el acento en verde. |
| `.portada-flujo` · `.titulo` · `dl.datos` | Portada de documento en flujo, en su propia página; `dl.datos` para versión, fecha y responsable. |
| `.cuerpo` · `.pie` · `.destacado` | Cuerpo y pie gris de página fija; `.destacado` agranda la fecha del pie. |
| `.etiqueta` (`.simple`, `.gris`) | Ceja en mayúsculas, mono, verde, con raya menta. |
| `.titulo-bloque` | Envoltura de `.etiqueta` + `h2` + `.entrada`; nunca se separa del contenido que sigue. |
| `.entrada` · `.atenuado` · `.pequeno` · `.nota-pie` · `.fuente` | Párrafo de entrada; texto gris; 8.5 pt; 7.5 pt para notas y fuentes. |
| `.termino` | Término normativo en pequeño después de la palabra de todos los días: «quién la mantiene `<span class="termino">(custodio)</span>`». |
| `.ref` | Chip gris discreto para artículo, fracción o código de campo (`art. 8 fr. V`, `C2`). Nunca encabeza una frase. |
| `.clave` | Clave o folio en mono: `CAT-0042`, `RC-2027-0118`. |
| `.ph` | Marcador por confirmar (ámbar, negritas). |
| `.estado` + `.obligatorio` / `.por-confirmar` / `.opcional` / `.dgetd` / `.listo` | Chip de estado con texto y forma distinta (círculo, rombo, aro, cuadro, palomita). |
| `.cifra` | Número grande + explicación (`<b>11</b><span>datos sobre la lista</span>`). |
| `.rejilla` (`.tres`, `.cuatro`, `.estirar`) · `.ancho-completo` | Rejilla de 2, 3 o 4 columnas; `.estirar` iguala alturas. |
| `.banda` (`.gris`) · `.pila` | Fondo menta tenue (o gris) para un bloque; `.pila` apila con separación estándar. |
| `.tarjeta` + `.si` / `.no` / `.neutra` / `.firme` / `.posible` / `.compromiso` · `.tarjeta-etiqueta` | Tarjeta de una idea; barra menta (sí) o gris (no); fondos de los tres tipos de afirmación. |
| `.trio` | Las tres tarjetas firme / posible / compromiso unidas, como el reverso de la Hoja de valor. |
| `ul.marcas-si` · `ul.marcas-no` | Lista con palomita verde o tache gris. |
| `ul.lista-iconos` | `li` = ícono (o `.ico-insignia`) + `<div><b>Título</b>texto</div>`. |
| `ul.razones` | Tres ideas en columnas con barra menta; `<b>` como título. |
| `ol.pasos` (`.vertical`) | Pasos numerados con círculo y conector; `li` = `<b>Título</b>` + texto. |
| `ol.linea-tiempo` (`.vertical`) · `li.hecho` · `li.limite` | Fechas: `li` = `<span class="fecha">…</span><div><b>Título</b>texto</div>`; `.hecho` punto lleno, `.limite` rombo ámbar. |
| `.recuadro` + `.nota` / `.norma` / `.compromiso` / `.pendiente` / `.alerta` / `.oj` · `.recuadro-titulo` | Recuadros. El título dice el tipo: «Nota», «Lo que dice la norma», «Compromiso DGETD», «Por confirmar», «Atención», «Órganos jurisdiccionales». |
| `.antes-despues` > `.antes` · `.flecha` · `.despues` | Comparación antes / después. |
| `.variantes` > `.fila` (`.buena`) · `.sistema` · `.valor` | Ejemplo «el mismo dato escrito de varias formas» (se rotula «Ejemplo ilustrativo»). |
| `.faq` > `div` > `h3` + `p` | Preguntas frecuentes en dos columnas con signo de pregunta. |
| `dl.glosario` | Glosario de dos columnas: `dt` (palabra común + `.termino`) y `dd`. |
| `figure.figura` > `.lienzo` · `.pasos-texto` · `figcaption` | Figura con marco y pie; `.pasos-texto` repite en texto los pasos de un diagrama. |
| `.ficha` · `.ficha-cabeza` · `.ficha-pie` | Ficha de catálogo (clave, datos, nota). |
| `.cierre` · `ul.contacto` | Bloque final de invitación con contacto (ícono + `<span><b>Etiqueta</b>dato</span>`). |
| `.para-saber-mas` | Sección final en tamaño menor para fundamento y detalles que no ayudan a actuar. |
| `.seccion-formato` > `.letra` + `h2/h3` | Encabezado de sección del formato (A, B, C…). |
| `.pregunta` > `.pregunta-num` + `.pregunta-cuerpo` | Bloque de pregunta. Dentro: `.pregunta-meta` (`.estado` + `.ref` con el código), `.pregunta-texto`, `.ayuda` (ícono + `<span>`), y el espacio de respuesta. `.pregunta.dgetd-campo` atenúa el número. |
| `.renglones` (`style="--n:3"`, `.amplios`) | Renglones para escribir; `--n` fija cuántos. |
| `.campos` (`.tres`) > `.campo` (`.ancho`) · `.respuesta` | Campos con etiqueta y línea (nombre, puesto, correo…); `.respuesta` para fichas ya llenas. |
| `ul.opciones` (`.unica`, `.dos`, `.tres`, `.cuatro`) · `li.marcada` · `<small>` · `.casilla` | Casillas: cuadro (varias) o círculo (`.unica`, «marque una»); en 1 a 4 columnas; `.casilla` es una sola casilla suelta. |
| `.zona-dgetd` · `.zona-dgetd-titulo` | Área «Lo llena la DGETD»: borde punteado y fondo menta; el título siempre dice «Lo llena la DGETD». |
| `.salto-antes` · `.salto-despues` · `.sin-corte` | Salto de página antes o después; impedir que un bloque se corte. |
| `.visualmente-oculto` | Texto solo para lectores de pantalla (por ejemplo, un `h2` que la página no muestra). |

**Íconos.** 40 íconos de línea (trazo de 2 px, esquinas redondeadas) en `fuentes/diseno/iconos/<nombre>.svg`, con `stroke="currentColor"`: toman el color del texto. Nombres: acuse, alerta, bandera, base-datos, buscar, calendario, candado, carpeta, check, check-circulo, ciclo, correo, cruz, documento, edificio, enlace, escudo, escudo-check, etiqueta, flecha-abajo, flecha-arriba, flecha-derecha, flecha-izquierda, foco, grupo, hoja-calculo, info, lapiz, libro, lista, mas, mensaje, nodos, ojo, pantalla, persona, pregunta, reloj, telefono, videollamada.
- Forma recomendada: `<span class="ico" data-icono="correo"></span>` y `<script src="diseno/iconos.js"></script>` al final del `<body>`. El script pone el SVG en línea con `aria-hidden="true"`. Si el ícono lleva significado propio, agregue `aria-label="…"` al `<span>`.
- Alternativa sin script: pegar el `<svg>` del archivo en línea, con `class="ico" aria-hidden="true" focusable="false"`.
- No funcionan en `file://` con Chromium: `<use href="iconos/x.svg#id">` y `mask-image`. `<img src>` funciona pero el ícono sale negro (no hereda el color).
- Tamaños: `.ico` (1.15 em, en línea), `.ico.grande` (7 mm), `.ico-insignia` (círculo menta; `.ambar`, `.coral`, `.verde`, `.gris`).
- Para agregar un ícono: nuevo `.svg` de 24 × 24 en `iconos/`; `iconos.js` se regenera solo al construir (o con `node build/generar_iconos.js`).

**Marcadores.** Todo marcador de `registro.yaml > marcadores` va con su texto literal, corchetes incluidos, dentro de `<span class="ph">`: `<span class="ph">[viernes 15 de enero de 2027, por confirmar]</span>`. El script informa cuántos hay.

**Accesibilidad.**
- `lang="es-MX"`, `<title>`, un solo `h1` por documento y encabezados sin saltos (h1 → h2 → h3). El script avisa si no se cumple.
- Listas reales (`ul`, `ol`, `dl`); tablas solo para datos tabulares, con `<th scope="col">` o `scope="row"`.
- Texto real, nunca imágenes de texto. Diagramas en HTML (pasos, línea de tiempo) o en SVG en línea con `role="img"` y `aria-label`, más los pasos en texto (`.pasos-texto`).
- Texto pequeño solo en `--ink`, `--ink-2`, `--mint-ink`, `--amber-ink`, `--coral-ink` o `--green-ink`. `--mint`, `--mint-2`, `--amber`, `--coral` y `--green` solo para fondos, bordes y adornos.
- Cuerpo ≥ 9.5 pt (`--t-chico` o mayor); notas y referencias ≥ 7.5 pt (`--t-min`).
- El color nunca es el único portador de significado: cada estado, recuadro y tarjeta lleva su texto.
- Íconos decorativos con `aria-hidden="true"` (el script lo pone).

**Construir y revisar.**

```bash
cd docs/catalogos/build
node html_pdf.js ../fuentes/<Pieza>.html --png        # PDF en ../entregables/, PNG por página en ../vista-previa/<Pieza>-<n>.png
node html_pdf.js ../fuentes/<Pieza>.html --borrador   # el PDF va a ../vista-previa/ en lugar de ../entregables/
pdftoppm -png -r 60 ../entregables/<Pieza>.pdf /tmp/…/<pieza>/p   # para revisar con la herramienta Read
```

El PDF sale A4, etiquetado (`tagged`) y con marcadores de navegación (`outline`). El script avisa de desbordes en páginas fijas, encabezados mal anidados, fuentes o íconos que no cargaron, `<img>` sin `alt` y PDF no etiquetado. Revise todas las páginas: cortes, huecos, títulos huérfanos, texto demasiado chico.
