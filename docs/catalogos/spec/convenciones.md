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
- Títulos: `#` capítulo, `##` sección, `###` subsección, `####` etiqueta pequeña. Numera capítulos y secciones en el texto («# 3. Políticas de operación», «## 3.1 …») en documentos normativos. En la guía y la circular no numeres.
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
