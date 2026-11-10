"""Genera la versión imprimible diseñada de F-CAT-01 (Registro de catálogo existente).

Uso (desde docs/catalogos/build):
    python3 formato_html.py            # escribe ../fuentes/F-CAT-01-imprimible.html y ../entregables/F-CAT-01-imprimible.pdf
    python3 formato_html.py --png      # además, una imagen por página en ../vista-previa/F-CAT-01-imprimible-<n>.png
    python3 formato_html.py --sin-pdf  # solo escribe el HTML

Lee ../spec/registro.yaml (fuente de verdad) y arma el HTML con el kit de diseño
(../fuentes/diseno/kit.css). Las preguntas, ayudas, opciones, estatus y marcadores salen del YAML,
así que esta versión no se separa del formulario en línea, del Word ni del Excel. Si cambia
registro.yaml, se vuelve a ejecutar este script. El PDF lo produce html_pdf.js (etiquetado y con
marcadores de navegación).

Reglas de presentación que aplica a cada pregunta (secciones A a F):
    · número consecutivo grande; el código del campo (A1, B2…) va como referencia discreta;
    · estado con texto: «Obligatoria», «Acepta «por confirmar»» u «Opcional»;
    · ayuda corta = primera oración de la ayuda del YAML; lo demás va a una nota pequeña;
      la oración «Ejemplo: «…»» se muestra aparte, con su rótulo;
    · «En los Lineamientos se llama «X».» se convierte en el término normativo pequeño junto a la pregunta;
    · «(art. N …)» y «(Transitorio …)» se convierten en chip de referencia;
    · espacio de respuesta según el tipo (renglones, campos, casillas).
"""
import html
import os
import re
import subprocess
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

# Lógica compartida con la plantilla de Excel: valores permitidos, subcampos y marcadores.
from plantilla_excel import (  # noqa: E402
    COMPLEMENTOS,
    SUBCAMPOS,
    marcadores_de,
    normalizar_obligatorio,
    valores_campo,
)

SPEC = os.path.join(RAIZ, "spec", "registro.yaml")
SALIDA_HTML = os.path.join(RAIZ, "fuentes", "F-CAT-01-imprimible.html")
FECHA = "Noviembre de 2026"

# Ayudas que el papel no puede seguir al pie de la letra (en papel no hay lista desplegable).
# Mismo texto que la versión de Word (fuentes/F-CAT-01.md).
AYUDA_IMPRESO = {
    "A1": ("Escríbala completa, sin siglas, como aparece en la lista oficial de áreas y órganos. "
           "Así evitamos que la misma área aparezca escrita de varias formas."),
}

# Campos de G con la forma de su clave (registro.yaml > claves)
FORMA_CLAVE = {"G1": "folio_registro", "G2": "catalogo"}

ABREVIATURAS = {"art", "arts", "fr", "frs", "núm"}


# -----------------------------------------------------------------------------
# Texto
# -----------------------------------------------------------------------------
def esc(texto):
    return html.escape(str(texto), quote=False)


def oraciones(texto):
    """Parte un texto en oraciones sin cortar en «art.», «fr.» y similares."""
    texto = " ".join(str(texto).split())
    partes, inicio = [], 0
    for m in re.finditer(r"[.?!]»?\s+(?=[«¿¡A-ZÁÉÍÓÚÑ])", texto):
        palabra = re.search(r"(\w+)$", texto[inicio:m.start()])
        if palabra and palabra.group(1).lower() in ABREVIATURAS:
            continue
        previo = texto[:m.start() + 1]
        if previo.count("«") > previo.count("»"):
            continue        # no se corta dentro de una cita «…»
        partes.append(texto[inicio:m.end()].strip())
        inicio = m.end()
    resto = texto[inicio:].strip()
    if resto:
        partes.append(resto)
    return partes


class Texto:
    """Convierte texto plano del YAML en HTML: marcadores, referencias y claves."""

    def __init__(self, marcadores):
        self.marcadores = sorted(set(marcadores.values()), key=len, reverse=True)

    def __call__(self, texto):
        t = esc(texto)
        # Marcadores: texto literal, resaltado
        if self.marcadores:
            patron = "(" + "|".join(re.escape(esc(m)) for m in self.marcadores) + ")"
            t = re.sub(patron, r'<span class="ph">\1</span>', t)
        # Referencias normativas entre paréntesis → chip discreto
        t = re.sub(r"\s*\(((?:arts?\.|Transitorio )[^)]*)\)", r' <span class="ref">\1</span>', t)
        # Claves y folios de ejemplo
        t = re.sub(r"\b(CAT-\d{4}|RC-\d{4}-\d{4})\b", r'<span class="clave">\1</span>', t)
        return t


def renglones(n):
    """Renglones para escribir de 8 mm, con trazo vectorial (el degradado de .renglones del kit
    deja una línea fantasma al imprimir)."""
    return '<div class="lineas" aria-hidden="true">' + "<span></span>" * n + "</div>"


def ico(nombre, extra=""):
    return f'<span class="ico{(" " + extra) if extra else ""}" data-icono="{nombre}"></span>'


# -----------------------------------------------------------------------------
# Preguntas
# -----------------------------------------------------------------------------
def estado_de(campo):
    ob = normalizar_obligatorio(campo.get("obligatorio"))
    if campo.get("quien") == "dgetd":
        return "dgetd", "Lo llena la DGETD"
    if ob == "si":
        return "obligatorio", "Obligatoria"
    if ob == "por_confirmar":
        return "por-confirmar", "Acepta «por confirmar»"
    return "opcional", "Opcional"


def preparar_ayuda(campo):
    """Devuelve (término, ayuda corta, ejemplo, nota) a partir de la ayuda del YAML."""
    texto = AYUDA_IMPRESO.get(campo["id"]) or campo.get("ayuda") or ""
    termino = None
    m = re.search(r"\s*En los Lineamientos se llama «([^»]+)»\.", texto)
    if m:
        termino = m.group(1)
        texto = (texto[:m.start()] + texto[m.end():]).strip()
    frases = oraciones(texto) if texto else []
    if campo["tipo"] == "persona" and len(frases) > 1:
        frases = frases[1:]          # la primera oración enumera los datos, que ya son los campos
    ejemplo = None
    for i, f in enumerate(frases):
        em = re.match(r"Ejemplo:\s*(.+?)\.?$", f)
        if em:
            ejemplo = em.group(1)
            frases = frases[:i] + frases[i + 1:]
            break
    corta = frases[0] if frases else ""
    nota = " ".join(frases[1:])
    return termino, corta, ejemplo, nota


def columnas_opciones(items):
    """Elige 1 a 4 columnas según el largo de las opciones."""
    if any(d for _, d in items):
        return "dos"
    largo = max(len(t) for t, _ in items)
    n = len(items)
    if largo <= 16:
        return "cuatro" if n >= 4 else "tres"
    if largo <= 32:
        return "tres"
    if largo <= 55:
        return "dos"
    return ""


def valores_campo_g(spec, campo):
    ref = campo.get("valores_ref")
    if ref:
        return [v["valor"] if isinstance(v, dict) else v for v in (spec["valores"].get(ref) or spec[ref])]
    return list(campo.get("valores") or [])


def items_opciones(spec, campo):
    """Lista de (texto principal HTML, texto pequeño HTML) para un campo de opción."""
    items = []
    if campo.get("valores_ref"):
        ref = campo["valores_ref"]
        for v in spec["valores"].get(ref) or spec[ref]:   # estatus_* están en la raíz del YAML
            if not isinstance(v, dict):
                items.append((esc(v), ""))
            elif "pregunta" in v:          # clasificación
                principal = esc(v["pregunta"])
                if v.get("art5"):
                    principal += f' <span class="termino">({esc(v["valor"].lower())})</span>'
                    peq = f"Por ejemplo: {esc(v['ejemplo'])}." if v.get("ejemplo") else ""
                else:
                    peq = esc(v["valor"])
                items.append((principal, peq))
            elif "descripcion" in v and campo["valores_ref"] == "nivel_acceso":
                items.append((f"<b>{esc(v['valor'])}</b>", esc(v["descripcion"])))
            else:
                items.append((esc(v["valor"]), ""))
    else:
        for v in valores_campo(spec, campo):
            items.append((esc(v), ""))
    return items


def html_opciones(spec, campo, unica=True, columnas=None, cortas=False):
    items = items_opciones(spec, campo)
    if cortas:          # sección G: solo el valor (la DGETD conoce los términos)
        items = [(esc(v), "") for v in valores_campo_g(spec, campo)]
    cols = columnas if columnas is not None else columnas_opciones(
        [(re.sub(r"<[^>]+>", "", t), d) for t, d in items])
    clases = " ".join(c for c in ["opciones", "unica" if unica else "", cols] if c)
    lis = []
    for t, d in items:
        otro = ' class="otro"' if re.sub(r"<[^>]+>", "", t) == "Otro" else ""
        peq = f"<small>{d}</small>" if d else ""
        lis.append(f"<li{otro}>{t}{peq}</li>")
    return f'<ul class="{clases}">' + "".join(lis) + "</ul>"


def html_respuesta(spec, campo, tx):
    fid, tipo = campo["id"], campo["tipo"]
    ob = normalizar_obligatorio(campo.get("obligatorio"))
    partes = []
    comp = COMPLEMENTOS.get(fid, [])
    if tipo == "persona":
        subs = SUBCAMPOS.get(fid, [("nombre completo", ""), ("puesto", "")])
        campos = "".join(f'<p class="campo">{esc(s[0].capitalize())}</p>' for s in subs)
        partes.append(f'<div class="campos">{campos}</div>')
    elif tipo == "area" and comp:
        sub = comp[0][0]
        partes.append('<div class="campos"><p class="campo ancho">Área</p>'
                      f'<p class="campo ancho">{esc(sub.capitalize())} '
                      '<span class="campo-pista">(nombre, puesto, correo y extensión)</span></p></div>')
        comp = []
    elif tipo == "area":
        partes.append(renglones(2))
    elif tipo == "texto":
        n = 2 if ob == "si" else 1
        partes.append(renglones(n))
    elif tipo == "texto_largo":
        n = 3 if ob != "no" else 2
        partes.append(renglones(n))
    elif tipo == "fecha_mes":
        partes.append('<div class="campos fecha"><p class="campo">Mes</p><p class="campo">Año</p></div>')
    elif tipo in ("opcion", "opciones_multiples"):
        partes.append(html_opciones(spec, campo, unica=(tipo == "opcion")))
    for _, preg, _, _, _ in comp:
        partes.append(f'<div class="campos"><p class="campo ancho">{esc(preg)}</p></div>')
    if campo.get("casilla"):
        partes.append(f'<p class="casilla">{tx(campo["casilla"])}</p>')
    elif ob == "por_confirmar" and tipo in ("area", "texto", "texto_largo", "persona", "fecha_mes"):
        partes.append('<p class="casilla">Por confirmar</p>')
    return "\n".join(partes)


def html_pregunta(spec, campo, numero, tx):
    clase, etiqueta = estado_de(campo)
    termino, corta, ejemplo, nota = preparar_ayuda(campo)
    pregunta = re.sub(r"^\(Opcional\)\s*", "", campo["pregunta"])
    marque = ""
    if campo["tipo"] == "opcion":
        marque = '<span class="marque">Marque una</span>'
    term = f' <span class="termino">({esc(termino)})</span>' if termino else ""
    h = [f'<div class="pregunta" id="p-{campo["id"]}">',
         f'<span class="pregunta-num" aria-hidden="true">{numero}</span>',
         '<div class="pregunta-cuerpo">',
         f'<div class="pregunta-meta"><span class="estado {clase}">{etiqueta}</span>{marque}'
         f'<span class="ref codigo">{esc(campo["id"])}</span></div>',
         f'<h3 class="pregunta-texto"><span class="visualmente-oculto">Pregunta {numero}. </span>'
         f'{tx(pregunta)}{term}</h3>']
    if corta:
        h.append(f'<p class="ayuda">{ico("info")}<span>{tx(corta)}</span></p>')
    if ejemplo:
        h.append(f'<p class="ejemplo"><span class="ejemplo-etq">Ejemplo</span><span>{tx(ejemplo)}</span></p>')
    if nota:
        h.append(f'<p class="nota-pregunta">{tx(nota)}</p>')
    h.append(html_respuesta(spec, campo, tx))
    h.append("</div></div>")
    return "\n".join(h)


def html_aviso_dgetd(campo, tx):
    """Campo que llena la DGETD dentro de A–F (hoy, B1): aviso sin número."""
    ayuda = " ".join(oraciones(campo.get("ayuda", "")))
    return (f'<div class="aviso-dgetd" id="p-{campo["id"]}">'
            f'<span class="ico-insignia">{ico("etiqueta")}</span>'
            f'<p class="aviso-texto"><b>{tx(campo["pregunta"])}</b> {tx(ayuda)}</p>'
            f'<div class="aviso-meta"><span class="estado dgetd">Lo llena la DGETD</span>'
            f'<span class="ref codigo">{esc(campo["id"])}</span></div></div>')


def resumen_seccion(campos):
    resp = [c for c in campos if c.get("quien") != "dgetd"]
    n = len(resp)
    cuenta = {"obligatorio": 0, "por-confirmar": 0, "opcional": 0}
    for c in resp:
        cuenta[estado_de(c)[0]] += 1
    palabra = "pregunta" if n == 1 else "preguntas"
    if cuenta["obligatorio"] == n:
        return f"{n} {palabra}" + (", obligatoria" if n == 1 else f", las {n} obligatorias")
    if cuenta["opcional"] == n:
        return f"{n} {palabra}" + (", opcional" if n == 1 else f", las {n} opcionales")
    trozos = []
    if cuenta["obligatorio"]:
        trozos.append(f"{cuenta['obligatorio']} obligatoria" + ("s" if cuenta["obligatorio"] > 1 else ""))
    if cuenta["por-confirmar"]:
        k = cuenta["por-confirmar"]
        trozos.append(f"{k} acepta{'n' if k > 1 else ''} «por confirmar»")
    if cuenta["opcional"]:
        k = cuenta["opcional"]
        trozos.append(f"{k} opcional" + ("es" if k > 1 else ""))
    return f"{n} {palabra}: " + ", ".join(trozos[:-1]) + (" y " if len(trozos) > 1 else "") + trozos[-1]


def titulo_amable(titulo):
    """«Para entender mejor su lista (opcional)» → título y aclaración por separado."""
    m = re.match(r"^(.*?)\s*\(([^)]+)\)$", titulo)
    return (m.group(1), m.group(2)) if m else (titulo, None)


# -----------------------------------------------------------------------------
# Sección G
# -----------------------------------------------------------------------------
def html_seccion_g(spec, seccion, tx):
    titulo, aclaracion = titulo_amable(seccion["titulo"])
    h = [f'<section class="ficha-dgetd salto-antes" aria-labelledby="sec-{seccion["id"]}" id="seccion-{seccion["id"]}">',
         '<header class="ficha-dgetd-cabeza">',
         f'<span class="ico-insignia gris">{ico("lapiz")}</span>',
         '<div>',
         '<div class="pregunta-meta"><span class="estado dgetd">Lo llena la DGETD</span>'
         f'<span class="ref codigo">Sección {esc(seccion["id"])}</span></div>',
         f'<h2 id="sec-{seccion["id"]}">{esc(titulo)}'
         + (f' <span class="termino">({esc(aclaracion)})</span>' if aclaracion else "") + "</h2>",
         f'<p class="ficha-dgetd-entrada">{tx(seccion.get("nota", ""))}</p>',
         "</div></header>",
         '<div class="ficha-dgetd-cuerpo">']
    dgetd = [c for c in seccion["campos"] if c.get("quien") == "dgetd"]
    area = [c for c in seccion["campos"] if c.get("quien") != "dgetd"]

    def etiqueta(c, nota=""):
        return (f'<span class="g-nombre">{tx(c["nombre"])}{nota}</span>'
                f'<span class="ref codigo">{esc(c["id"])}</span>')

    grupo = []

    def volcar():
        if not grupo:
            return
        clase = {1: "campos", 2: "campos", 3: "campos tres"}.get(len(grupo), "campos cuatro")
        celdas = []
        for c in grupo:
            forma = ""
            if c["id"] in FORMA_CLAVE:
                forma = f'<span class="forma-clave">{esc(spec["claves"][FORMA_CLAVE[c["id"]]]["formato"])}</span>'
            celdas.append(f'<p class="campo g-campo">{etiqueta(c)}{forma}</p>')
        h.append(f'<div class="{clase}">' + "".join(celdas) + "</div>")
        grupo.clear()

    # Los datos cortos (folio, clave, fechas, versión) van juntos en un renglón de campos al inicio.
    grupo.extend(c for c in dgetd if c["tipo"] == "texto")
    volcar()
    for c in dgetd:
        if c["tipo"] == "texto":
            continue
        nota = f' <span class="g-nota">{tx(c["nota"])}</span>' if c.get("nota") else ""
        bloque = [f'<div class="g-bloque" id="p-{c["id"]}">', f'<p class="g-etiqueta">{etiqueta(c, nota)}</p>']
        if c["tipo"] == "opcion":
            n = len(valores_campo_g(spec, c))
            bloque.append(html_opciones(spec, c, columnas={3: "tres", 5: "cinco"}.get(n, "cuatro"), cortas=True))
        elif c["tipo"] == "texto_largo":
            bloque.append(renglones(2))
        bloque.append("</div>")
        h.append("\n".join(bloque))
    volcar()
    h.append("</div>")
    for c in area:
        h.append(f'<div class="confirma-area" id="p-{c["id"]}">'
                 f'<div class="confirma-cabeza">{ico("check-circulo")}'
                 '<p><b>Confirmación de su área</b> Lo llena su área cuando revisa la ficha y está de acuerdo.</p>'
                 f'<span class="ref codigo">{esc(c["id"])}</span></div>'
                 '<div class="campos tres"><p class="campo ancho-2">Nombre de quien confirma</p>'
                 '<p class="campo">Fecha</p></div></div>')
    h.append("</section>")
    return "\n".join(h)


# -----------------------------------------------------------------------------
# Documento
# -----------------------------------------------------------------------------
CSS = r"""
  /* F-CAT-01 imprimible · CSS particular (kit.css no se edita) */
  /* Formato impreso: nada menor a 9 pt salvo códigos */
  .estado { font-size: 9pt; padding: 1.1mm 2.4mm; }
  .campo { font-size: 9pt; }
  ul.opciones > li small { font-size: 9pt; }
  .etiqueta { font-size: 9pt; letter-spacing: .06em; }
  .cabecera { font-size: 9pt; }
  .contacto b { font-size: 9pt; }
  .ref.codigo { font-family: var(--mono); font-weight: 500; letter-spacing: .03em; }

  /* Página 1 */
  .portada { padding-top: 11mm; padding-bottom: 6mm; grid-template-columns: 1.3fr 1fr; align-items: stretch; }
  .portada h1 { font-size: 30pt; }
  .portada .entrada { font-size: 12pt; }
  .portada .nombre-oficial { margin-top: 4mm; font-size: 9.5pt; color: var(--ink-2); }
  .resumen { background: var(--mint-tint); border-radius: var(--radio); padding: 5mm 5.5mm; display: flex; flex-direction: column; gap: 3mm; justify-content: center; }
  .resumen-titulo { font-family: var(--serif); font-weight: 700; font-size: 13pt; line-height: 1.2; }
  .resumen ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 3mm; }
  .resumen li { display: grid; grid-template-columns: 10mm 1fr; column-gap: 3mm; align-items: center; margin: 0; }
  .resumen li > b { font-family: var(--serif); font-weight: 700; font-size: 24pt; line-height: 1; color: var(--mint-ink); text-align: right; }
  .resumen li > span { display: grid; gap: 1mm; justify-items: start; font-size: 9.5pt; color: var(--ink-2); line-height: 1.3; }
  .page > .cuerpo { gap: 4.5mm; }
  .antes-titulo { display: flex; align-items: baseline; gap: 4mm; }
  .antes-titulo h2 { font-size: 17pt; }
  .tarjetas-antes { list-style: none; padding: 0; margin: 0; gap: 4mm; }
  .tarjetas-antes > li { margin: 0; padding: 4.5mm 5mm; gap: 2mm; }
  .tarjetas-antes .tarjeta-cabeza { display: flex; align-items: center; gap: 3mm; }
  .tarjetas-antes h3 { font-size: 12.5pt; }
  .tarjetas-antes p { font-size: 10pt; color: var(--ink-2); line-height: 1.42; }
  .tarjetas-antes p b { color: var(--ink); }
  .leyenda { padding: 4.5mm 5.5mm 5mm; }
  .leyenda h3 { font-size: 11.5pt; margin-bottom: 3mm; }
  .leyenda ul { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 2.6mm 5mm; }
  .leyenda li { margin: 0; display: grid; gap: 1.2mm; justify-items: start; font-size: 9.5pt; color: var(--ink-2); line-height: 1.32; }
  .leyenda .muestra-casilla { position: relative; padding-left: 6.6mm; font-weight: 700; color: var(--ink); font-size: 9.5pt; }
  .leyenda .muestra-casilla::before { content: ""; position: absolute; left: 0; top: .1mm; width: 4.2mm; height: 4.2mm; border: .35mm solid var(--ink-2); border-radius: .8mm; background: #fff; }
  .leyenda .muestra-casilla.circulo::before { border-radius: 50%; }
  .leyenda .muestra-renglon { display: block; width: 26mm; height: 4.4mm; border-bottom: .3mm solid var(--trazo); }
  .pie .ph { font-size: 10.5pt; }

  /* Partes A–F con número grande */
  .parte + .parte { margin-top: 5mm; }
  .parte-inicio { break-inside: avoid; page-break-inside: avoid; }
  .parte-cabeza { display: grid; grid-template-columns: 19mm minmax(0, 1fr); column-gap: 5mm; align-items: end;
    padding-bottom: 3mm; border-bottom: .6mm solid var(--ink); break-after: avoid; page-break-after: avoid; }
  .parte-num { font-family: var(--serif); font-weight: 700; font-size: 48pt; line-height: .8; color: var(--mint-ink);
    border-left: 1.6mm solid var(--mint); padding-left: 3mm; }
  .parte-de { display: flex; align-items: center; gap: 2mm; font-size: 9.5pt; color: var(--ink-2); margin-bottom: 1.2mm; }
  .parte-cabeza h2 { font-size: 18pt; line-height: 1.12; }
  .parte-cabeza h2 .termino { font-size: 11pt; }
  .parte-resumen { margin-top: 1.4mm; font-size: 10pt; color: var(--ink-2); }
  .parte .recuadro { margin-top: 3mm; padding: 3mm 4.5mm; }
  .parte .recuadro + .pregunta, .parte .aviso-dgetd + .pregunta { border-top: 0; }
  .flujo .parte > * + * { margin-top: 0; }
  .flujo .parte .recuadro + * { margin-top: 0; }

  /* Pregunta */
  .pregunta { padding: 3mm 0 3.2mm; }
  .lineas { display: grid; }
  .lineas > span { display: block; height: 8mm; border-bottom: .3mm solid var(--trazo); }
  .parte-cabeza + .pregunta, .parte-inicio > .pregunta:first-of-type { border-top: 0; }
  .pregunta-num { width: 9mm; height: 9mm; font-size: 11pt; background: var(--mint-tint); }
  .pregunta { grid-template-columns: 9mm minmax(0, 1fr); }
  .pregunta-cuerpo { gap: 1.8mm; }
  .pregunta-meta .codigo { margin-left: auto; }
  .pregunta-texto { font-family: var(--serif); font-weight: 700; font-size: 13pt; line-height: 1.25; text-wrap: pretty; }
  .pregunta-texto .termino { font-size: 9.75pt; }
  ul.opciones .termino { font-size: 9pt; }
  .marque { font-size: 9pt; color: var(--ink-2); }
  .ayuda { font-size: 10pt; line-height: 1.4; }
  .ayuda > .ico { width: 4.2mm; height: 4.2mm; }
  .ejemplo { display: flex; gap: 2.5mm; align-items: baseline; font-size: 10pt; color: var(--ink); background: var(--panel);
    border: var(--borde); border-radius: 1mm; padding: 1.8mm 3mm; }
  .ejemplo-etq { font-family: var(--mono); font-weight: 500; font-size: 9pt; letter-spacing: .06em; text-transform: uppercase; color: var(--mint-ink); flex: none; }
  .nota-pregunta { font-size: 9pt; line-height: 1.42; color: var(--ink-2); border-left: .6mm solid var(--line); padding-left: 3mm; margin-left: 6mm; }
  .pregunta .lineas, .pregunta .campos, .pregunta ul.opciones { margin-top: 1mm; }
  .pregunta .campos { gap: 3mm 7mm; }
  .campo { min-height: 10.5mm; }
  .campos.cuatro { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .campo-pista { color: var(--ink-2); }
  .campos.fecha { grid-template-columns: 34mm 34mm; }
  ul.opciones { gap: 2.6mm; }
  ul.opciones > li.otro::after { content: ""; display: inline-block; width: 40mm; margin-left: 2mm; border-bottom: .3mm solid var(--trazo); height: 3.6mm; vertical-align: -.6mm; }
  .casilla { font-size: 10pt; margin-top: 1mm; }
  .casilla::before { width: 4.2mm; height: 4.2mm; }

  /* Revisión final */
  .flujo section.revision { margin-top: 5mm; padding: 4.5mm 6mm 5mm; }
  .revision-cabeza { display: flex; align-items: center; gap: 3mm; margin-bottom: 3.5mm; }
  .revision h2 { font-size: 14pt; margin: 0 !important; }
  .revision ul.opciones > li { font-size: 10pt; }

  /* Aviso de campo que llena la DGETD (B1) */
  .aviso-dgetd { display: grid; grid-template-columns: 9mm minmax(0, 1fr); column-gap: 4mm; align-items: start;
    margin-top: 4mm; padding: 4mm 4.5mm; background: var(--mint-tint); border-radius: var(--radio); break-inside: avoid; }
  .aviso-dgetd { grid-template-columns: 9mm minmax(0, 1fr) auto; align-items: center; padding: 3mm 4.5mm; }
  .aviso-meta { display: grid; gap: 1.5mm; justify-items: end; }
  .aviso-titulo { font-weight: 700; font-size: 10.5pt; }
  .aviso-texto { font-size: 10pt; color: var(--ink-2); }

  /* Sección G · panel gris claramente distinto */
  .ficha-dgetd { background: var(--panel); border: .5mm dashed var(--ink-2); border-radius: 2.5mm; overflow: hidden; }
  .ficha-dgetd-cabeza { display: grid; grid-template-columns: 9mm minmax(0, 1fr); column-gap: 4mm; align-items: start;
    background: var(--line); padding: 4mm 6mm 3.5mm; }
  .ficha-dgetd-cabeza > div { display: grid; gap: 1.8mm; }
  .ficha-dgetd-cabeza h2 { font-size: 17pt; }
  .ficha-dgetd-cabeza .termino { font-size: 11pt; }
  .ficha-dgetd-entrada { font-size: 10pt; color: var(--ink); }
  .ficha-dgetd-cuerpo { padding: 1mm 6mm 1mm; }
  .ficha-dgetd-cuerpo > .campos { background: #fff; border-radius: 1mm; padding: 1.5mm 4mm 3mm; margin-top: 3.5mm; border: var(--borde); }
  .g-bloque { padding: 2.3mm 0 2.4mm; border-top: var(--borde); display: grid; gap: 2.2mm; break-inside: avoid; }
  .ficha-dgetd-cuerpo > .campos + .g-bloque { border-top: 0; }
  .g-etiqueta { display: flex; align-items: center; gap: 2mm; font-weight: 700; font-size: 10.5pt; }
  .g-etiqueta .codigo, .g-campo .codigo { margin-left: auto; }
  .g-campo { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: .6mm 2mm; align-content: start; align-items: start; }
  ul.opciones.cinco { grid-template-columns: repeat(5, minmax(0, 1fr)); column-gap: 3mm; }
  .forma-clave { grid-column: 1 / -1; font-family: var(--mono); font-size: 9pt; color: var(--ink-2); letter-spacing: .04em; }
  .g-nota { font-weight: 400; font-size: 9pt; color: var(--ink-2); margin-left: 1.5mm; }
  .ficha-dgetd .lineas { background: #fff; }
  .ficha-dgetd ul.opciones > li { font-size: 9.5pt; }
  .confirma-area { margin: 1mm 6mm 5mm; background: #fff; border: .45mm solid var(--mint-ink); border-radius: var(--radio); padding: 3mm 5mm 3.5mm; break-inside: avoid; }
  .confirma-cabeza { display: flex; align-items: center; gap: 2.5mm; font-size: 10pt; }
  .confirma-cabeza > .ico { color: var(--mint-ink); width: 5mm; height: 5mm; }
  .confirma-cabeza p { color: var(--ink-2); }
  .confirma-cabeza p b { color: var(--mint-ink); margin-right: 1.5mm; }
  .confirma-cabeza .codigo { margin-left: auto; }
  .confirma-area .campos.tres { grid-template-columns: 2fr 1fr; margin-top: 2mm; }

  /* Cierre */
  .despues .titulo-bloque h2 { font-size: 19pt; }
  .despues ol.pasos > li { font-size: 10pt; }
  .despues ol.pasos > li .ref { margin-top: 2mm; }
  .despues .rejilla { margin-top: 6mm; align-items: stretch; }
  .despues .recuadro.compromiso { padding: 5mm 5.5mm; font-size: 10pt; }
  .despues .recuadro-titulo { font-size: 11.5pt; }
  .despues .recuadro .ico { color: var(--green-ink); }
  .compromiso-plazos { border-top: .3mm solid rgba(74, 122, 60, .25); padding-top: 2.5mm; margin: 0; display: grid; gap: .8mm; }
  .compromiso-plazos dt { font-weight: 700; margin-top: 1mm; }
  .compromiso-plazos dd { margin: 0; }
  .despues ol.pasos .ref { font-size: 9pt; }
  .despues .cierre { grid-template-columns: 1fr; gap: 4mm; padding: 5.5mm 6mm; align-content: start; }
  .despues .cierre h3 { font-family: var(--serif); font-size: 14pt; }
  .despues .cierre p { font-size: 10pt; margin-top: 1.5mm; }
  .contacto { font-size: 9.5pt; }
  .para-saber-mas { margin-top: 9mm; }
  .para-saber-mas h3 { margin-top: 3mm; }
  .para-saber-mas .recuadro { margin-top: 3mm; }
  .para-saber-mas ul { padding-left: 4.5mm; }
  .tabla-art8 { margin-top: 3mm; font-size: 9pt; color: var(--ink); }
  .tabla-art8 caption { text-align: left; font-weight: 700; font-size: 9.5pt; padding-bottom: 2mm; color: var(--ink); }
  .tabla-art8 th, .tabla-art8 td { padding: .6mm 2.5mm; }
  .tabla-art8 .ref { vertical-align: 0; }
  .flujo .para-saber-mas.salto-antes { border-top: 0; padding-top: 0; }
  .para-saber-mas .recuadro { padding: 3mm 4.5mm; }
  .tabla-art8 thead th { font-size: 9pt; }
  .tabla-art8 tbody th { font-weight: 600; background: none; white-space: nowrap; width: 20mm; }
  .identificacion { margin-top: 4mm; font-size: 9pt; color: var(--ink-2); }
"""


def construir(spec):
    m = marcadores_de(spec)
    tx = Texto(m)

    def ph(clave):
        return f'<span class="ph">{esc(m[clave])}</span>'

    secciones = [s for s in spec["secciones"] if s["id"] != "G"]
    seccion_g = next(s for s in spec["secciones"] if s["id"] == "G")

    # Numeración consecutiva de las preguntas que responde el área
    numeros, n = {}, 0
    for s in secciones:
        for c in s["campos"]:
            if c.get("quien") != "dgetd":
                n += 1
                numeros[c["id"]] = n
    total = n
    estados = [estado_de(c)[0] for s in secciones for c in s["campos"] if c.get("quien") != "dgetd"]
    n_ob, n_pc, n_op = (estados.count("obligatorio"), estados.count("por-confirmar"), estados.count("opcional"))
    indispensables = [numeros[f] for f in ("A1", "B2", "B3")]
    ind_txt = f"{indispensables[0]}, {indispensables[1]} y {indispensables[2]}"
    n_e1 = numeros.get("E1")

    out = []
    w = out.append
    w('<!doctype html>\n<html lang="es-MX">\n<head>\n<meta charset="utf-8">')
    w("<title>F-CAT-01 · Registro de catálogo existente · versión imprimible</title>")
    w('<meta name="author" content="Dirección General de Estrategia y Transformación Digital (DGETD)">')
    w('<meta name="description" content="Versión imprimible del formato F-CAT-01 para registrar una lista '
      '(catálogo) ante la DGETD conforme al Transitorio CUARTO de los Lineamientos Generales de Catálogos '
      'Institucionales. Generada desde spec/registro.yaml.">')
    w('<meta name="pdf-encabezado" content="F-CAT-01 · Registro de catálogo existente">')
    w(f'<meta name="pdf-pie" content="Versión {esc(spec["version"])} · {esc(spec["estatus"])} · no vigente">')
    w('<meta name="generator" content="build/formato_html.py a partir de spec/registro.yaml">')
    w('<link rel="stylesheet" href="diseno/kit.css">')
    w("<style>" + CSS + "</style>\n</head>\n<body>")
    w("<!-- Archivo generado por build/formato_html.py desde spec/registro.yaml. No se edita a mano. -->")

    # ---------------- Página 1 ----------------
    w('<article class="page" aria-label="Página 1: presentación y antes de empezar">')
    w('<header class="cabecera"><span class="marca">Órgano de Administración Judicial · DGETD</span>'
      '<span class="etiqueta simple">Formato F-CAT-01 · Para imprimir</span></header>')
    w('<section class="portada">')
    w('<div><span class="etiqueta">Registro de listas · Transitorio CUARTO</span>'
      '<h1>Registro de una lista <em>de su área</em></h1>'
      '<p class="entrada">Le pedimos datos sobre la lista, no la lista. Use estas hojas para preparar sus '
      'respuestas o para registrarla con nosotros por Teams o por teléfono.</p>'
      '<p class="nombre-oficial">Nombre oficial: Registro de catálogo existente '
      '<span class="ref">F-CAT-01</span></p></div>')
    w('<aside class="resumen" aria-label="Cuántas preguntas tiene el formato">'
      f'<p class="resumen-titulo">{total} preguntas en {len(secciones)} partes</p><ul>'
      f'<li><b>{n_ob}</b><span><span class="estado obligatorio">Obligatoria</span>Se responden siempre.</span></li>'
      f'<li><b>{n_pc}</b><span><span class="estado por-confirmar">Acepta «por confirmar»</span>'
      'Si no sabe el dato, lo completamos con usted.</span></li>'
      f'<li><b>{n_op}</b><span><span class="estado opcional">Opcional</span>Nos ayudan a planear; '
      'puede dejarlas en blanco.</span></li></ul></aside>')
    w("</section>")

    w('<section class="cuerpo" aria-labelledby="antes">')
    w('<div class="antes-titulo"><h2 id="antes">Antes de empezar</h2></div>')
    tarjetas = [
        ("documento", "Una ficha por cada lista",
         "Si su área lleva varias listas, llene una ficha por cada una. <b>Ante la duda, regístrela</b>: "
         "registrar no es autorizar."),
        ("candado", "Datos sobre la lista, no la lista",
         "No adjunte su contenido ni datos personales. Registrar no publica la lista ni cambia quién la "
         "administra."),
        ("pregunta", "«Por confirmar» vale",
         "Si no sabe un dato, marque o escriba «Por confirmar» donde se indica. "
         "<b>No invente</b>: le ayudamos a completarlo."),
        ("pantalla", "Mejor en línea",
         f"El camino principal es el formulario: {ph('liga_formulario')}. Con más de 5 listas, use la "
         "plantilla de Excel."),
    ]
    w('<ul class="rejilla estirar tarjetas-antes">')
    for icono, titulo, texto in tarjetas:
        w(f'<li class="tarjeta si"><div class="tarjeta-cabeza"><span class="ico-insignia">{ico(icono)}</span>'
          f'<h3>{titulo}</h3></div><p>{texto}</p></li>')
    w("</ul>")
    w('<section class="banda gris leyenda" aria-labelledby="leyenda"><h3 id="leyenda">Cómo leer cada pregunta</h3><ul>'
      '<li><span class="estado obligatorio">Obligatoria</span>Necesitamos la respuesta.</li>'
      '<li><span class="estado por-confirmar">Acepta «por confirmar»</span>Puede responder «Por confirmar».</li>'
      '<li><span class="estado opcional">Opcional</span>Puede dejarla en blanco.</li>'
      '<li><span class="muestra-casilla circulo">Círculo</span>Marque una sola opción.</li>'
      '<li><span class="muestra-casilla">Cuadro</span>Márquelo si es su caso.</li>'
      '<li><span class="muestra-renglon" aria-hidden="true"></span>Escriba con letra clara, sin siglas.</li>'
      "</ul></section>")
    w('<div class="recuadro nota"><p class="recuadro-titulo">' + ico("reloj") + "¿Se acerca la fecha límite?</p>"
      f"<p>Envíe lo que sepa. Con el área, el nombre y la descripción de la lista (preguntas {ind_txt}), "
      "la DGETD recibe su registro, le da trámite y completa el resto con usted.</p></div>")
    w("</section>")
    w(f'<footer class="pie"><span>Fecha límite para registrar: {ph("fecha_limite_registro")}</span>'
      f'<span><strong>Dudas:</strong> {ph("contacto_dgetd")}</span></footer>')
    w("</article>")

    # ---------------- Partes A–F ----------------
    w('<main class="flujo">')
    for i, s in enumerate(secciones, start=1):
        titulo, aclaracion = titulo_amable(s["titulo"])
        campos = s["campos"]
        w(f'<section class="parte" aria-labelledby="sec-{s["id"]}" id="seccion-{s["id"]}">')
        w('<div class="parte-inicio">')
        w('<header class="parte-cabeza">'
          f'<span class="parte-num" aria-hidden="true">{i}</span><div>'
          f'<p class="parte-de">Parte {i} de {len(secciones)} <span class="ref codigo">Sección {esc(s["id"])}</span></p>'
          f'<h2 id="sec-{s["id"]}"><span class="visualmente-oculto">Parte {i}. </span>{esc(titulo)}'
          + (f' <span class="termino">({esc(aclaracion)})</span>' if aclaracion else "")
          + f'</h2><p class="parte-resumen">{esc(resumen_seccion(campos))}</p></div></header>')
        if s.get("nota"):
            frases = oraciones(s["nota"])
            w(f'<div class="recuadro nota"><p class="recuadro-titulo">{ico("info")}{tx(frases[0])}</p>'
              + (f'<p>{tx(" ".join(frases[1:]))}</p>' if len(frases) > 1 else "") + "</div>")
        primera = True
        for c in campos:
            if c.get("quien") == "dgetd":
                w(html_aviso_dgetd(c, tx))
                continue
            w(html_pregunta(spec, c, numeros[c["id"]], tx))
            if primera:
                w("</div>")      # fin de .parte-inicio: el título nunca queda solo al pie de página
                primera = False
        w("</section>")

    # ---------------- Revisión final (lista para marcar) ----------------
    oblig = [numeros[c["id"]] for s in secciones for c in s["campos"]
             if c["id"] in numeros and estado_de(c)[0] == "obligatorio"]
    lista_ob = ", ".join(str(x) for x in oblig[:-1]) + f" y {oblig[-1]}"
    w('<section class="revision banda" aria-labelledby="revise">'
      f'<div class="revision-cabeza"><span class="ico-insignia">{ico("check-circulo")}</span>'
      '<h2 id="revise">Antes de capturar sus respuestas</h2></div>'
      '<ul class="opciones">'
      f"<li>Respondió las {len(oblig)} preguntas obligatorias: {lista_ob}.</li>"
      "<li>En las que aceptan «por confirmar», anotó el dato o marcó «Por confirmar».</li>"
      f"<li>La persona titular de la pregunta {numeros['A3']} conoce este registro.</li>"
      f"<li>Capture sus respuestas en el formulario: {ph('liga_formulario')}, o pida el registro "
      f"acompañado: {ph('contacto_dgetd')}.</li>"
      "</ul></section>")

    # ---------------- Sección G ----------------
    w(html_seccion_g(spec, seccion_g, tx))

    # ---------------- Qué pasa después ----------------
    est = {e["valor"]: e for e in spec["estatus_registro"]}
    pasos = [
        ("Recibe su acuse", "Recibido",
         "Con folio, fecha y la clave de su lista, por ejemplo CAT-0042. La persona titular recibe copia."),
        ("Revisamos y prellenamos", "En revisión",
         "Completamos lo que la DGETD ya conoce, como los sistemas que usan la lista. Si falta algo que solo "
         "su área sabe, su persona de contacto le llama."),
        ("Le enviamos su ficha", "Ficha enviada",
         f"Con lo que usted registró y lo que prellenamos. Plazo: {m['plazo_ficha_confirmacion']}."),
        ("Usted la confirma", "Confirmado",
         "La revisa, corrige lo necesario y la confirma con su nombre y la fecha. Con eso, el registro queda "
         "completo."),
    ]
    for _, estatus, _ in pasos:
        assert estatus in est, f"El estatus «{estatus}» ya no está en registro.yaml > estatus_registro"
    w('<section class="despues salto-antes" aria-labelledby="despues">')
    w('<header class="titulo-bloque"><span class="etiqueta">Cuando termine</span>'
      '<h2 id="despues">Qué pasa después</h2>'
      '<p class="entrada">Capture sus respuestas en el formulario en línea o pídanos que las capturemos '
      'con usted. A partir de ahí, esto es lo que sigue.</p></header>')
    w('<ol class="pasos">')
    for titulo, estatus, texto in pasos:
        w(f'<li><b>{titulo}</b>{tx(texto)}<br><span class="ref">Estatus: {esc(estatus)}</span></li>')
    w("</ol>")
    w('<div class="rejilla estirar">')
    w('<div class="recuadro compromiso"><p class="recuadro-titulo">' + ico("escudo-check")
      + "Compromiso DGETD</p>"
      '<ul class="marcas-si">'
      "<li>Acuse con folio y fecha.</li>"
      "<li>Clave de su lista asignada por la DGETD.</li>"
      "<li>Prellenado de lo que la DGETD ya conoce.</li>"
      "<li>Una persona de contacto con nombre.</li>"
      "<li>No volver a pedirle lo que ya entregó.</li>"
      "<li>Correcciones sin costo hasta el dictamen.</li></ul>"
      "<p>El registro no es una auditoría: los errores se corrigen sin costo hasta el dictamen.</p>"
      f'<dl class="compromiso-plazos"><dt>Plazo para enviarle la ficha</dt><dd>{ph("plazo_ficha_confirmacion")}</dd>'
      f'<dt>Plazo para responder sus dudas</dt><dd>{ph("plazo_respuesta_dudas")}</dd></dl></div>')
    w('<div class="cierre"><div><h3>Le acompañamos en el registro</h3>'
      "<p>Si prefiere, registramos juntos su lista por Teams o por teléfono. Usted responde y nosotros "
      "capturamos.</p></div>"
      '<ul class="contacto">'
      f'<li><span class="ico-insignia">{ico("correo")}</span><span><b>Asesoría DGETD</b>{ph("contacto_dgetd")}</span></li>'
      f'<li><span class="ico-insignia">{ico("enlace")}</span><span><b>Formulario de registro</b>{ph("liga_formulario")}</span></li>'
      f'<li><span class="ico-insignia">{ico("carpeta")}</span><span><b>Plantilla de Excel, más de 5 listas</b>{ph("liga_sharepoint")}</span></li>'
      "</ul></div>")
    w("</div>")
    w("</section>")

    # ---------------- Para saber más ----------------
    w('<section class="para-saber-mas salto-antes" aria-labelledby="saber-mas">')
    w('<h2 id="saber-mas">Para saber más</h2>')
    w('<div class="recuadro pendiente"><p class="recuadro-titulo">' + ico("alerta")
      + "Por confirmar: registros con datos pendientes</p>"
      f"<p>La DGETD recibe y da trámite a todo registro que traiga el área, el nombre y la descripción de la "
      f"lista (preguntas {ind_txt}) y completa con el área los demás datos que lleguen «por confirmar». El "
      "registro queda completo cuando el área confirma la ficha. Si un registro con datos «por confirmar» "
      "se tiene por presentado en tiempo para el Transitorio CUARTO lo decide el Comité de Gobernanza "
      "Digital; está pendiente.</p></div>")
    w('<div class="recuadro oj"><p class="recuadro-titulo">Órganos jurisdiccionales</p>'
      "<p>Este formato les llega por el conducto institucional del Órgano de Administración Judicial (OAJ). "
      "Si su órgano no lleva listas propias, no tiene que hacer nada más. No se piden expedientes, "
      "contenidos ni datos personales.</p></div>")
    # Las demás reglas de registro.yaml ya están en la página 1 y en las notas de cada parte.
    w('<h3>Lo que conviene saber</h3><ul>')
    w(f"<li><b>Niveles de acceso (pregunta {n_e1}).</b> {tx(spec['valores']['nota_nivel_acceso'])}</li>")
    w(f"<li><b>Aviso de privacidad.</b> Sobre los datos de las personas que anota en las preguntas "
      f"{numeros['A2']}, {numeros['A3']} y {numeros['C2']}: {ph('liga_aviso_privacidad')}.</li>")
    w("<li><b>Ejemplos y fechas.</b> Los ejemplos de listas, claves y folios son ilustrativos. Las fechas están "
      "por confirmar.</li>")
    w("</ul>")
    # Qué fracción del art. 8 cubre cada pregunta
    fr = []
    for s in spec["secciones"]:
        for c in s["campos"]:
            if c.get("art8") and s["id"] != "G":
                donde = f"Pregunta {numeros[c['id']]}" if c["id"] in numeros else "La asigna la DGETD"
                fr.append((c["art8"], c["id"], donde, c["nombre"]))
    w("<h3>Fundamento</h3>")
    w("<p>" + tx("Lineamientos Generales de Catálogos Institucionales (LGCI), Transitorio CUARTO: las áreas "
      "y los órganos jurisdiccionales registran ante la Dirección General de Estrategia y Transformación "
      "Digital (DGETD) los catálogos que ya administran, con los datos mínimos del artículo 8. La DGETD "
      "emite los formatos (art. 14 fr. IX). El Comité formaliza propietario y custodio al aprobar el "
      "catálogo (art. 12) y determina si es estratégico u operativo (art. 5). Procedimiento: PR-CAT-04 "
      "Procedimiento de registro de catálogos existentes.") + "</p>")
    w('<table class="tabla-art8"><caption>Cada dato del artículo 8 y dónde se pregunta</caption>'
      '<thead><tr><th scope="col">Fracción</th><th scope="col">Dato</th><th scope="col">Dónde se pregunta</th>'
      '<th scope="col">Código</th></tr></thead><tbody>')
    for frac, fid, donde, nombre in fr:
        w(f'<tr><th scope="row">fr. {esc(frac)}</th><td>{esc(nombre)}</td><td>{esc(donde)}</td>'
          f'<td><span class="ref codigo">{esc(fid)}</span></td></tr>')
    w("</tbody></table>")
    w(f'<p class="identificacion">F-CAT-01 Registro de catálogo existente · Versión imprimible · '
      f'Versión {esc(spec["version"])} · {FECHA} · {esc(spec["estatus"])} · no vigente · '
      "Responsable: DGETD · Generada desde spec/registro.yaml.</p>")
    w("</section>")
    w("</main>")
    w('<script src="diseno/iconos.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    with open(SPEC, encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)
    contenido = construir(spec)
    with open(SALIDA_HTML, "w", encoding="utf-8") as fh:
        fh.write(contenido)
    print(f"Escrito {os.path.relpath(SALIDA_HTML, RAIZ)}")
    if "--sin-pdf" in args:
        return
    cmd = ["node", "html_pdf.js", os.path.relpath(SALIDA_HTML, AQUI)] + [a for a in args if a in ("--png", "--borrador")]
    subprocess.run(cmd, cwd=AQUI, check=True)


if __name__ == "__main__":
    main()
