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
    · número consecutivo grande (el único numeral grande; la parte va como ceja «Parte N de 6»);
      el código del campo (A1, B2…) va como referencia discreta;
    · estado con texto: «Obligatoria», «Acepta «por confirmar»» u «Opcional» (también dentro del h3, oculto);
    · ayuda corta = primera oración de la ayuda del YAML, salvo las escritas a mano en AYUDA_CORTA
      (lo que tranquiliza o dice qué hacer va arriba); lo demás va a una nota pequeña;
      la oración «Ejemplo: «…»» se muestra aparte, con su rótulo;
    · «En los Lineamientos se llama «X».» se convierte en el término normativo pequeño junto a la pregunta;
    · «(art. N …)» y «(Transitorio …)» salen de la frase y van como chip al final del bloque;
    · espacio de respuesta según el tipo (renglones, campos, casillas).

Después de construir: comprueba en qué página quedó el recuadro para órganos jurisdiccionales (la
página 1 remite a ella; si cambió, reconstruye con el número correcto) y reescribe los títulos de los
marcadores del PDF con el texto de cada encabezado (Chromium pega palabras donde el título se parte).
"""
import html
import os
from html.parser import HTMLParser
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

# Ayuda corta escrita a mano para el papel: (ayuda visible, nota pequeña o None, referencia o None).
# Regla: lo que tranquiliza o dice qué hacer va arriba; el detalle, en la nota; el artículo, como chip
# al final. El contenido es el mismo de registro.yaml, dicho para el papel (aquí hay casillas, no
# campos que se puedan dejar vacíos). Si cambia la ayuda en el YAML, se revisa esta tabla.
AYUDA_CORTA = {
    "B2": ("Si no tiene nombre formal, propóngale uno. Si en su área le dicen de otra forma "
           "(«el Excel de inmuebles»), escríbalo entre paréntesis.", None, None),
    "C1": ("Es el área con autoridad sobre el contenido, aunque no sea la que captura. "
           "Si no sabe cuál es, marque «Por confirmar».",
           "Si es su propia área, anótela. Si la lista nace del trabajo de juzgados o tribunales, anote el "
           "área administrativa que se encarga del tema; esa área pide la opinión de los órganos "
           "jurisdiccionales.", "art. 4 fr. XVII"),
    "C2b": ("Solo registra su interés; lo decide el Comité. Su área seguiría decidiendo las reglas de la lista.",
            None, "arts. 12 y 17"),
    "C3": ("Elija la más parecida; no se preocupe por acertar, nosotros la revisamos.",
           "La DGETD registra una clasificación propuesta, que se formaliza cuando se aprueba el catálogo. "
           "Las cuatro opciones son los tipos de lista que prevén los Lineamientos.", "art. 5"),
    "D1": ("Anote los que conozca, uno por línea. Si no los conoce todos, marque la casilla de abajo: "
           "nosotros completamos la lista con las áreas de sistemas.",
           "Incluya hojas de cálculo o tableros de otras áreas que la copian. Lo preguntamos para poder "
           "avisarles antes de un cambio de estructura.", "art. 13"),
    "D3": ("Lo más común es que no. Si responde «No», nosotros registramos la versión 1.0 con la fecha de "
           "su registro; no tiene que crear versiones.", None, None),
    "D4": ("Basta mes y año aproximados. Si la lista está en un sistema, marque la casilla de abajo y "
           "nosotros obtenemos la fecha exacta.", None, None),
    "E1": ("Registrar no publica su lista. Si duda, elija la opción más restrictiva.",
           "Si contiene información reservada o confidencial, márquela como «Clasificada». Esa clasificación "
           "se rige por la normativa de transparencia; la DGETD la usa para proteger la ficha y aplicar "
           "controles de acceso.", "art. 23"),
    "F3": ("Por ejemplo, si un juzgado tiene la clave «0901-P-01», esa clave «dice» circuito y materia.",
           "Nos ayuda a planear claves que no cambien con el tiempo.", "art. 7"),
}

# Notas de sección reescritas para el papel: (título del recuadro, texto, referencia).
NOTA_SECCION = {
    "C": ("Lo que anote aquí son propuestas.",
          "El Comité formaliza al propietario y al custodio cuando aprueba el catálogo.", "art. 12"),
    "F": ("Estas preguntas no son obligatorias.",
          "Nos ayudan a planear con su área los ajustes que su lista pueda necesitar más adelante. "
          "La DGETD no le volverá a pedir lo que ya entregó.", "Transitorio QUINTO"),
}

# Sección G: primero la palabra de todos los días; el término, en pequeño.
# (nombre visible, término o None, referencia o None)
NOMBRE_G = {
    "G2": ("Clave asignada a su lista", None, None),
    "G4": ("Tipo de lista propuesto", "clasificación", "art. 5 fr. I–IV"),
    "G5": ("Alcance propuesto", "estratégico u operativo", None),
    "G6": ("Sistemas que usan la lista", "sistemas consumidores", None),
    "G8": ("Situación del registro", "estatus", None),
    "G9": ("Situación de la lista en el inventario", "estatus", None),
}

# Página donde queda el recuadro para órganos jurisdiccionales (se comprueba después de construir).
PAGINA_OJ = 10
TITULO_OJ = "Para los órganos jurisdiccionales"

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

    def __call__(self, texto, ref=None):
        """Las referencias «(art. N…)» y «(Transitorio …)» salen de la frase y van como chip al final
        del bloque, sin puntuación después (regla de referencias discretas). `ref` agrega otra."""
        t = esc(texto)
        refs = []

        def guardar(m):
            refs.append(m.group(1))
            return ""
        t = re.sub(r"\s*\(((?:arts?\.|Transitorio )[^)]*)\)", guardar, t)
        if ref:
            refs.append(esc(ref))
        # Marcadores: texto literal, resaltado
        if self.marcadores:
            patron = "(" + "|".join(re.escape(esc(m)) for m in self.marcadores) + ")"
            t = re.sub(patron, r'<span class="ph">\1</span>', t)
        # Claves y folios de ejemplo (con su puntuación, para que no quede suelta)
        t = re.sub(r"\b(CAT-\d{4}|RC-\d{4}-\d{4})\b([.,;:]?)",
                   r'<span class="nw"><span class="clave">\1</span>\2</span>', t)
        if refs:
            t += "".join(f' <span class="ref">{r}</span>' for r in refs)
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
    ref = None
    if campo["id"] in AYUDA_CORTA:
        corta, nota, ref = AYUDA_CORTA[campo["id"]]
        nota = nota or ""
    return termino, corta, ejemplo, nota, ref


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
    termino, corta, ejemplo, nota, ref = preparar_ayuda(campo)
    pregunta = re.sub(r"^\(Opcional\)\s*", "", campo["pregunta"])
    marque = ""
    if campo["tipo"] == "opcion":
        marque = '<span class="marque">Marque una</span>'
    term = f' <span class="termino">({esc(termino)})</span>' if termino else ""
    # El estado va también dentro del h3 (oculto) para quien navega por encabezados;
    # el chip visible se oculta al lector de pantalla para no repetirlo.
    estado_oculto = {"obligatorio": "obligatoria", "por-confirmar": "acepta «por confirmar»",
                     "opcional": "opcional"}[clase]
    h = [f'<div class="pregunta" id="p-{campo["id"]}">',
         f'<span class="pregunta-num" aria-hidden="true">{numero}</span>',
         '<div class="pregunta-cuerpo">',
         f'<div class="pregunta-meta"><span class="estado {clase}" aria-hidden="true">{etiqueta}</span>{marque}'
         f'<span class="ref codigo">{esc(campo["id"])}</span></div>',
         f'<h3 class="pregunta-texto"><span class="visualmente-oculto">Pregunta {numero}, {estado_oculto}. </span>'
         f'{tx(pregunta)}{term}</h3>']
    # La referencia va al final de la nota; si no hay nota, al final de la ayuda.
    if corta:
        h.append(f'<p class="ayuda">{ico("info")}<span>{tx(corta, None if nota else ref)}</span></p>')
    if ejemplo:
        h.append(f'<p class="ejemplo"><span class="ejemplo-etq">Ejemplo</span><span>{tx(ejemplo)}</span></p>')
    if nota:
        h.append(f'<p class="nota-pregunta">{tx(nota, ref)}</p>')
    h.append(html_respuesta(spec, campo, tx))
    h.append("</div></div>")
    return "\n".join(h)


def html_aviso_dgetd(campo, tx):
    """Campo que llena la DGETD dentro de A–F (hoy, B1): aviso sin número."""
    frases = oraciones(campo.get("ayuda", ""))
    # La oración con la forma de la clave («La clave tiene la forma CAT-0042.») se muestra aparte,
    # como muestra, para que la clave no quede en medio de la frase con un punto suelto.
    muestra = ""
    for f in frases:
        mc = re.search(r"\b(CAT-\d{4})\b", f)
        if mc:
            muestra = (f'<span class="aviso-muestra">Así se ve una clave: '
                       f'<span class="clave">{esc(mc.group(1))}</span></span>')
            frases = [x for x in frases if x is not f]
            break
    ayuda = " ".join(frases)
    return (f'<div class="aviso-dgetd" id="p-{campo["id"]}">'
            f'<span class="ico-insignia">{ico("etiqueta")}</span>'
            f'<p class="aviso-texto"><b>{tx(campo["pregunta"])}</b> {tx(ayuda)}{muestra}</p>'
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
         # registro.yaml: «Esta sección la llena la DGETD. El área la revisa y la confirma.» Dicho para
         # quien tiene el papel en la mano: no la llena; es la ficha que le llegará para confirmar.
         '<p class="ficha-dgetd-entrada"><b>Usted no llena esta página.</b> Así se verá la ficha que le '
         'enviaremos para que la revise y la confirme.</p>',
         "</div></header>",
         '<div class="ficha-dgetd-cuerpo">']
    dgetd = [c for c in seccion["campos"] if c.get("quien") == "dgetd"]
    area = [c for c in seccion["campos"] if c.get("quien") != "dgetd"]

    def etiqueta(c, nota=""):
        nombre, termino, ref = NOMBRE_G.get(c["id"], (c["nombre"], None, None))
        term = f' <span class="termino">({esc(termino)})</span>' if termino else ""
        return (f'<span class="g-nombre">{tx(nombre, ref)}{term}{nota}</span>'
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
        # Vista previa, sin renglones: el área confirma la ficha que le llega, no este papel.
        h.append(f'<div class="confirma-area" id="p-{c["id"]}">'
                 f'<div class="confirma-cabeza">{ico("check-circulo")}'
                 '<p><b>Confirmación de su área</b> Cuando le llegue la ficha, su área la revisa, corrige lo '
                 'necesario y la confirma con el nombre de quien confirma y la fecha.</p>'
                 f'<span class="ref codigo">{esc(c["id"])}</span></div></div>')
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
  .portada { padding-top: 8mm; padding-bottom: 4mm; grid-template-columns: 1.3fr 1fr; align-items: stretch; }
  .portada h1 { font-size: 30pt; }
  .portada .entrada { font-size: 12pt; }
  .portada .nombre-oficial { margin-top: 4mm; font-size: 9.5pt; color: var(--ink-2); }
  .resumen { background: var(--mint-tint); border-radius: var(--radio); padding: 5mm 5.5mm; display: flex; flex-direction: column; gap: 3mm; justify-content: center; }
  .resumen-titulo { font-family: var(--serif); font-weight: 700; font-size: 13pt; line-height: 1.2; }
  .resumen ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 3mm; }
  .resumen li { display: grid; grid-template-columns: 10mm 1fr; column-gap: 3mm; align-items: center; margin: 0; }
  .resumen li > b { font-family: var(--serif); font-weight: 700; font-size: 24pt; line-height: 1; color: var(--mint-ink); text-align: right; }
  .resumen li > span { display: grid; gap: 1mm; justify-items: start; font-size: 9.5pt; color: var(--ink-2); line-height: 1.3; }
  .page > .cuerpo { gap: 3.6mm; }
  .antes-titulo { display: flex; align-items: baseline; gap: 4mm; }
  .antes-titulo h2 { font-size: 17pt; }
  .tarjetas-antes { list-style: none; padding: 0; margin: 0; gap: 3.5mm; }
  .tarjetas-antes > li { margin: 0; padding: 3.6mm 5mm 3.8mm; gap: 1.6mm; }
  .tarjetas-antes .tarjeta-cabeza { display: flex; align-items: center; gap: 3mm; }
  .tarjetas-antes h3 { font-size: 12.5pt; }
  .tarjetas-antes p { font-size: 10pt; color: var(--ink-2); line-height: 1.42; }
  .tarjetas-antes p b { color: var(--ink); }
  .leyenda { padding: 3.6mm 5.5mm 3.8mm; }
  .leyenda h3 { font-size: 11.5pt; margin-bottom: 2.4mm; }
  .leyenda ul { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 2.6mm 5mm; }
  .leyenda li { margin: 0; display: grid; gap: 1.2mm; justify-items: start; font-size: 9.5pt; color: var(--ink-2); line-height: 1.32; }
  .leyenda .muestra-casilla { position: relative; padding-left: 6.6mm; font-weight: 700; color: var(--ink); font-size: 9.5pt; }
  .leyenda .muestra-casilla::before { content: ""; position: absolute; left: 0; top: .1mm; width: 4.2mm; height: 4.2mm; border: .35mm solid var(--ink-2); border-radius: .8mm; background: #fff; }
  .leyenda .muestra-casilla.circulo::before { border-radius: 50%; }
  .leyenda .muestra-renglon { display: block; width: 26mm; height: 4.4mm; border-bottom: .3mm solid var(--trazo); }
  .pie { flex-wrap: nowrap; align-items: flex-start; }
  .pie > span { display: grid; gap: 1.2mm; max-width: 50%; }
  .pie > span + span { justify-items: end; text-align: right; }
  .pie strong { font-size: 9.5pt; }
  .pie .ph { font-size: 9.5pt; }
  .portada .aviso-oj { margin-top: 3mm; display: flex; align-items: center; gap: 2mm; font-size: 9.5pt; color: var(--ink-2); }
  .aviso-oj > .ico { width: 4.4mm; height: 4.4mm; color: var(--mint-ink); flex: none; }
  .aviso-oj a { color: var(--mint-ink); font-weight: 700; text-decoration: underline; text-underline-offset: .5mm; }
  .ph-linea { display: block; margin-top: 1.2mm; }
  .ph-linea .ph { white-space: nowrap; }
  .nw { white-space: nowrap; }
  .leyenda-nota { display: flex; align-items: center; gap: 2mm; margin-top: 2.6mm; padding-top: 2.2mm;
    border-top: var(--borde); font-size: 9.5pt; color: var(--ink-2); }
  .leyenda-nota > .ico { width: 4.2mm; height: 4.2mm; flex: none; }
  .faltan { padding: 3mm 5mm; }
  .faltan > * + * { margin-top: 1.2mm; }
  .faltan > p:not(.recuadro-titulo) { font-size: 10pt; }
  .pendiente-linea { display: flex; align-items: center; gap: 2mm; color: var(--amber-ink); font-weight: 700; }
  .pendiente-linea > .ico { width: 4.4mm; height: 4.4mm; flex: none; }

  /* Partes A–F: ceja «Parte N de 6» y título grande; un solo numeral grande (el de la pregunta) */
  .parte + .parte { margin-top: 6mm; }
  .parte-inicio { break-inside: avoid; page-break-inside: avoid; }
  .parte-cabeza { position: relative; padding-bottom: 3mm; border-bottom: .4mm solid var(--line);
    break-after: avoid; page-break-after: avoid; }
  .parte-cabeza::after { content: ""; position: absolute; left: 0; bottom: -.6mm; width: 22mm; height: .8mm;
    background: var(--mint); border-radius: .4mm; }
  .parte-de { display: flex; align-items: center; justify-content: space-between; gap: 2mm; margin-bottom: 1.6mm; }
  .parte-cabeza h2 { font-size: 20pt; line-height: 1.12; }
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
  .flujo section.revision { margin-top: 4mm; padding: 4mm 6mm 4mm; }
  .revision-cabeza { display: flex; align-items: center; gap: 3mm; margin-bottom: 2.5mm; }
  .revision ul.opciones { gap: 1.8mm; }
  .revision h2 { font-size: 14pt; margin: 0 !important; }
  .revision ul.opciones > li { font-size: 10pt; }
  .revision-accion { grid-template-columns: 1fr 1fr; gap: 4mm; margin-top: 3mm; padding-top: 3mm; border-top: .3mm solid rgba(42, 115, 112, .2); }
  .revision-accion > p { display: grid; grid-template-columns: 8mm minmax(0, 1fr); column-gap: 3mm; align-items: start; font-size: 10pt; }
  .revision-accion .ico-insignia { width: 8mm; height: 8mm; background: #fff; }
  .revision-accion b { display: block; margin-bottom: .8mm; }

  /* Aviso de campo que llena la DGETD (B1) */
  .aviso-dgetd { display: grid; grid-template-columns: 9mm minmax(0, 1fr); column-gap: 4mm; align-items: start;
    margin-top: 4mm; padding: 4mm 4.5mm; background: var(--mint-tint); border-radius: var(--radio); break-inside: avoid; }
  .aviso-dgetd { grid-template-columns: 9mm minmax(0, 1fr) auto; align-items: center; padding: 3mm 4.5mm; }
  .aviso-meta { display: grid; gap: 1.5mm; justify-items: end; }
  .aviso-titulo { font-weight: 700; font-size: 10.5pt; }
  .aviso-texto { font-size: 10pt; color: var(--ink-2); }
  .aviso-muestra { display: block; margin-top: 1.2mm; font-size: 9.5pt; }

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
  .flujo .despues > ol.pasos { margin-top: 6mm; }
  .despues ol.pasos > li .ref { margin-top: 2mm; }
  .despues .rejilla { align-items: stretch; }
  .despues .recuadro.compromiso { padding: 5mm 5.5mm; font-size: 10pt; }
  .despues .recuadro-titulo { font-size: 11.5pt; }
  .despues .recuadro .ico { color: var(--green-ink); }
  .compromiso-plazos { border-top: .3mm solid rgba(74, 122, 60, .25); padding-top: 2.5mm; margin: 0; display: grid; gap: .8mm; }
  .compromiso-plazos dt { font-weight: 700; margin-top: 1mm; }
  .compromiso-plazos dd { margin: 0; }
  .despues ol.pasos .ref { font-size: 9pt; }
  .paso-extra { display: block; margin-top: 1.5mm; font-size: 9.5pt; }
  .paso-extra .ph { display: inline; }
  .despues ol.pasos .paso-estatus { display: table; margin-top: 2mm; }
  .flujo .despues > .compromiso-ancho { margin-top: 6mm; }
  .compromiso-ancho ul.marcas-si { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2mm 8mm; }
  .compromiso-ancho ul.marcas-si li + li { margin-top: 0; }
  .compromiso-ancho .compromiso-plazos { grid-template-columns: 1fr 1fr; column-gap: 8mm; }
  .compromiso-ancho .compromiso-plazos dt { margin-top: 0; }
  .avisos-finales { align-items: stretch; }
  .avisos-finales .recuadro.oj > p:not(.recuadro-titulo) { margin-top: 2mm; }
  .pendiente-final { font-size: 10pt; }
  .flujo .despues > .cierre-ancho { grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr); column-gap: 8mm;
    padding: 4.5mm 6mm; align-items: start; }
  .cierre-ancho ul.contacto { gap: 2mm; }
  .flujo .despues > .avisos-finales { margin-top: 4.5mm; }
  .avisos-finales .recuadro-titulo .ico { color: inherit; }
  .recuadro.avisos-finales { padding: 4mm 5mm; font-size: 10pt; }
  .avisos-finales .recuadro-titulo { font-size: 11pt; }
  .recuadro.oj.avisos-finales .recuadro-titulo .ico { color: var(--mint-ink); }
  .despues .cierre { grid-template-columns: 1fr; gap: 4mm; padding: 5.5mm 6mm; align-content: start; }
  .despues .cierre h3 { font-family: var(--serif); font-size: 14pt; }
  .despues .cierre p { font-size: 10pt; margin-top: 1.5mm; }
  .contacto { font-size: 9.5pt; }
  .flujo .para-saber-mas { margin-top: 6mm; padding-top: 4mm; }
  .para-saber-mas h3 { margin-top: 3mm; }
  .para-saber-mas .recuadro { margin-top: 3mm; }
  .para-saber-mas ul { padding-left: 4.5mm; }
  .tabla-art8 { margin-top: 3mm; font-size: 9pt; color: var(--ink); }
  .tabla-art8 caption { text-align: left; font-weight: 700; font-size: 9.5pt; padding-bottom: 2mm; color: var(--ink); }
  .tabla-art8 th, .tabla-art8 td { padding: .35mm 2.5mm; }
  .tabla-art8 .ref { vertical-align: 0; }
  .flujo .para-saber-mas.salto-antes { border-top: 0; padding-top: 0; }
  .para-saber-mas .recuadro { padding: 3mm 4.5mm; }
  .tabla-art8 thead th { font-size: 9pt; }
  .tabla-art8 tbody th { font-weight: 600; background: none; white-space: nowrap; width: 20mm; }
  .identificacion { margin-top: 3mm; font-size: 9pt; color: var(--ink-2); }
"""


def construir(spec, pagina_oj=PAGINA_OJ):
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
      'Institucionales.">')
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
      'respuestas. Si no puede usar el formulario en línea, las capturamos con usted.</p>'
      '<p class="nombre-oficial">Nombre oficial: Registro de catálogo existente '
      '<span class="ref">F-CAT-01</span></p>'
      f'<p class="aviso-oj">{ico("edificio")}<span>¿Es usted de un órgano jurisdiccional? '
      f'Vea la <a href="#oj">página {pagina_oj}</a></span></p></div>')
    w('<aside class="resumen" aria-label="Cuántas preguntas tiene el formato">'
      f'<p class="resumen-titulo">{total} preguntas en {len(secciones)} partes</p><ul>'
      f'<li><b>{n_ob}</b><span><span class="estado obligatorio">Obligatoria</span>Se responden siempre.</span></li>'
      f'<li><b>{n_pc}</b><span><span class="estado por-confirmar">Acepta «por confirmar»</span>'
      'Si no sabe el dato, lo completamos con usted.</span></li>'
      f'<li><b>{n_op}</b><span><span class="estado opcional">Opcional</span>'
      'Puede dejarlas en blanco.</span></li></ul></aside>')
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
         "<b>Mejor «Por confirmar» que un dato supuesto</b>: le ayudamos a completarlo."),
        ("pantalla", "Mejor en línea",
         "El camino principal es el formulario en línea. Con más de 5 listas, use la plantilla de Excel."
         f"<span class=\"ph-linea\">{ph('liga_formulario')}</span>"),
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
      "</ul>"
      f'<p class="leyenda-nota">{ico("info")}<span>Los números de esta hoja no son los del formulario '
      "en línea: al capturar, guíese por el texto de la pregunta.</span></p></section>")
    # Criterio operativo de registro.yaml > reglas. No se liga con el plazo: eso lo decide el Comité.
    w('<div class="recuadro nota faltan"><p class="recuadro-titulo">' + ico("pregunta")
      + "¿No tiene todos los datos?</p>"
      f"<p>Con el área, el nombre y la descripción de la lista (preguntas {ind_txt}), la DGETD recibe su "
      "registro, le da trámite y completa con usted los datos que lleguen «por confirmar».</p>"
      f'<p class="pendiente-linea">{ico("alerta")}<span>Si eso cuenta dentro del plazo lo decide el Comité; '
      "está pendiente.</span></p></div>")
    w("</section>")
    w(f'<footer class="pie"><span><strong>Fecha límite:</strong> {ph("fecha_limite_registro")}</span>'
      f'<span><strong>Dudas:</strong> {ph("contacto_dgetd")}</span></footer>')
    w("</article>")

    # ---------------- Partes A–F ----------------
    w('<main class="flujo">')
    for i, s in enumerate(secciones, start=1):
        titulo, aclaracion = titulo_amable(s["titulo"])
        campos = s["campos"]
        w(f'<section class="parte" aria-labelledby="sec-{s["id"]}" id="seccion-{s["id"]}">')
        w('<div class="parte-inicio">')
        # Un solo numeral grande por página: el de las preguntas. La parte va como ceja (.etiqueta).
        w('<header class="parte-cabeza">'
          f'<p class="parte-de"><span class="etiqueta">Parte {i} de {len(secciones)}</span>'
          f'<span class="ref codigo">Sección {esc(s["id"])}</span></p>'
          f'<h2 id="sec-{s["id"]}"><span class="visualmente-oculto">Parte {i}. </span>{esc(titulo)}'
          + (f' <span class="termino">({esc(aclaracion)})</span>' if aclaracion else "")
          + f'</h2><p class="parte-resumen">{esc(resumen_seccion(campos))}</p></header>')
        tiene_nota = s["id"] in NOTA_SECCION or bool(s.get("nota"))
        if s["id"] in NOTA_SECCION:
            t_nota, texto_nota, ref_nota = NOTA_SECCION[s["id"]]
            w(f'<div class="recuadro nota"><p class="recuadro-titulo">{ico("info")}{tx(t_nota)}</p>'
              f'<p>{tx(texto_nota, ref_nota)}</p></div>')
        elif s.get("nota"):
            frases = oraciones(s["nota"])
            w(f'<div class="recuadro nota"><p class="recuadro-titulo">{ico("info")}{tx(frases[0])}</p>'
              + (f'<p>{tx(" ".join(frases[1:]))}</p>' if len(frases) > 1 else "") + "</div>")
        # .parte-inicio junta el encabezado con su recuadro (nota o aviso de la DGETD) o, si no hay
        # recuadro, con la primera pregunta: el título nunca queda solo al pie de la página.
        primera = True
        if tiene_nota:
            w("</div>")
            primera = False
        for c in campos:
            if c.get("quien") == "dgetd":
                w(html_aviso_dgetd(c, tx))
            else:
                w(html_pregunta(spec, c, numeros[c["id"]], tx))
            # fin de .parte-inicio tras el primer bloque (pregunta o aviso de la DGETD)
            if primera:
                w("</div>")      # fin de .parte-inicio
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
      f"<li>La persona titular que anotó en la pregunta {numeros['A3']} conoce y respalda este registro.</li>"
      "<li>Al capturar, se guía por el texto de cada pregunta, no por su número.</li>"
      f"<li>Capture sus respuestas en el formulario en línea (si no puede usarlo, vea la página {pagina_oj}): "
      f'{ph("liga_formulario")}</li>'
      "</ul></section>")

    # ---------------- Sección G ----------------
    w(html_seccion_g(spec, seccion_g, tx))

    # ---------------- Qué pasa después ----------------
    est = {e["valor"]: e for e in spec["estatus_registro"]}
    pasos = [
        ("Recibe su acuse", "Recibido",
         "Con folio, fecha y la clave de su lista. La persona titular recibe copia.",
         '<span class="paso-extra">Clave de ejemplo <span class="clave">CAT-0042</span></span>'),
        ("Revisamos y prellenamos", "En revisión",
         "Completamos lo que ya conocemos. Si falta algo que solo su área sabe, la persona de contacto "
         "que le asignamos en la DGETD se comunica con usted.", ""),
        ("Le enviamos su ficha", "Ficha enviada",
         "Con lo que usted registró y lo que prellenamos.",
         f'<span class="paso-extra">Plazo {ph("plazo_ficha_confirmacion")}</span>'),
        ("Usted la confirma", "Confirmado",
         "La revisa, corrige lo necesario y la confirma con su nombre y la fecha. Con eso, el registro queda "
         "completo.", ""),
    ]
    for _, estatus, _, _ in pasos:
        assert estatus in est, f"El estatus «{estatus}» ya no está en registro.yaml > estatus_registro"
    w('<section class="despues salto-antes" aria-labelledby="despues">')
    w('<header class="titulo-bloque"><span class="etiqueta">Cuando termine</span>'
      '<h2 id="despues">Qué pasa después</h2>'
      '<p class="entrada">Capture sus respuestas en el formulario en línea; si no puede usarlo, las '
      'capturamos con usted. A partir de ahí, esto es lo que sigue.</p></header>')
    w('<ol class="pasos">')
    for titulo, estatus, texto, extra in pasos:
        w(f'<li><b>{titulo}</b>{tx(texto)}{extra}<span class="ref paso-estatus">Estatus: {esc(estatus)}</span></li>')
    w("</ol>")
    # Compromiso a lo ancho (viñetas en dos columnas); debajo, registro acompañado junto al recuadro para
    # órganos jurisdiccionales (aquí y no al final, para que la secretaría de un órgano lo encuentre
    # pronto; la página 1 remite a esta página) y, al final, el criterio pendiente del Comité.
    w('<div class="recuadro compromiso compromiso-ancho"><p class="recuadro-titulo">' + ico("escudo-check")
      + "Compromiso DGETD</p>"
      '<ul class="marcas-si">'
      "<li>Acuse con folio y fecha.</li>"
      "<li>Una persona de contacto con nombre.</li>"
      "<li>Clave de su lista asignada por la DGETD.</li>"
      "<li>No volver a pedirle lo que ya entregó.</li>"
      "<li>Prellenado de lo que la DGETD ya conoce.</li>"
      "<li>Correcciones sin costo hasta el dictamen.</li></ul>"
      "<p>El registro no es una auditoría: los errores se corrigen sin costo hasta el dictamen.</p>"
      f'<dl class="compromiso-plazos"><div><dt>Plazo para enviarle la ficha</dt><dd>{ph("plazo_ficha_confirmacion")}</dd></div>'
      f'<div><dt>Plazo para responder sus dudas</dt><dd>{ph("plazo_respuesta_dudas")}</dd></div></dl></div>')
    w('<div class="cierre cierre-ancho"><div><h3>Registro acompañado</h3>'
      "<p>Si no puede usar el formulario ni la plantilla, registramos su lista con usted por Teams o por "
      "teléfono: usted responde y nosotros capturamos.</p></div>"
      '<ul class="contacto">'
      f'<li><span class="ico-insignia">{ico("correo")}</span><span><b>Asesoría DGETD</b>{ph("contacto_dgetd")}</span></li>'
      f'<li><span class="ico-insignia">{ico("enlace")}</span><span><b>Formulario de registro</b>{ph("liga_formulario")}</span></li>'
      f'<li><span class="ico-insignia">{ico("carpeta")}</span><span><b>Plantilla de Excel, más de 5 listas</b>{ph("liga_sharepoint")}</span></li>'
      "</ul></div>")
    w(f'<div class="recuadro oj avisos-finales" id="oj"><p class="recuadro-titulo">{ico("edificio")}{TITULO_OJ}</p>'
      "<p>Este formato les llega por el conducto institucional del Órgano de Administración Judicial (OAJ). "
      "Si su órgano lleva listas propias, le invitamos a registrarlas. <b>Si no lleva listas propias, no "
      "tiene que hacer nada más.</b> No se piden expedientes, contenidos ni datos personales.</p></div>")
    w('<div class="recuadro pendiente pendiente-final avisos-finales"><p class="recuadro-titulo">' + ico("alerta")
      + "Por confirmar: registros con datos pendientes</p>"
      + "<p>" + tx(f"La DGETD recibe y da trámite a todo registro con el área, el nombre y la descripción "
                   f"de la lista (preguntas {ind_txt}) y completa con el área los datos que lleguen «por "
                   "confirmar». Si un registro así se tiene por presentado en tiempo para el Transitorio "
                   "CUARTO lo decide el Comité; está pendiente.", "Transitorio SÉPTIMO")
      + "</p></div>")
    w("</section>")

    # ---------------- Para saber más ----------------
    w('<section class="para-saber-mas" aria-labelledby="saber-mas">')
    w('<h2 id="saber-mas">Para saber más</h2>')
    # Las demás reglas de registro.yaml ya están en la página 1 y en las notas de cada parte.
    # registro.yaml > valores > nota_nivel_acceso es una nota pendiente: se muestra como «Por confirmar».
    w('<div class="recuadro pendiente"><p class="recuadro-titulo">' + ico("alerta")
      + f"Por confirmar: opciones de la pregunta {n_e1}</p>"
      f"<p>Las opciones de nivel de acceso de la pregunta {n_e1} son una propuesta de la DGETD. Se alinearán "
      "con las disposiciones de transparencia del OAJ y con la unidad de transparencia competente antes de "
      "la versión definitiva de este formato.</p></div>")
    w('<h3>Lo que conviene saber</h3><ul>')
    w(f"<li><b>Aviso de privacidad.</b> Sobre los datos de las personas que anota en las preguntas "
      f"{numeros['A2']}, {numeros['A3']} y {numeros['C2']}: "
      f'<span class="ph-linea">{ph("liga_aviso_privacidad")}</span></li>')
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
    w("<ul>")
    for linea in [
        "Según los Lineamientos Generales de Catálogos Institucionales (LGCI), las áreas y los órganos "
        "jurisdiccionales registran ante la Dirección General de Estrategia y Transformación Digital (DGETD) "
        "los catálogos que ya administran, con los datos mínimos del artículo 8 (Transitorio CUARTO).",
        "La DGETD emite los formatos (art. 14 fr. IX).",
        "El Comité formaliza propietario y custodio al aprobar el catálogo (art. 12).",
        "El Comité determina si es estratégico u operativo, a propuesta de la DGETD (art. 5).",
        "Procedimiento: PR-CAT-04 Procedimiento de registro de catálogos existentes.",
    ]:
        w(f"<li>{tx(linea)}</li>")
    w("</ul>")
    w('<table class="tabla-art8"><caption>Cada dato del artículo 8 y dónde se pregunta</caption>'
      '<thead><tr><th scope="col">Fracción</th><th scope="col">Dato</th><th scope="col">Dónde se pregunta</th>'
      '<th scope="col">Código</th></tr></thead><tbody>')
    for frac, fid, donde, nombre in fr:
        w(f'<tr><th scope="row">fr. {esc(frac)}</th><td>{esc(nombre)}</td><td>{esc(donde)}</td>'
          f'<td><span class="ref codigo">{esc(fid)}</span></td></tr>')
    w("</tbody></table>")
    w(f'<p class="identificacion">F-CAT-01 · Versión imprimible {esc(spec["version"])} · {FECHA} · '
      f'{esc(spec["estatus"])} · no vigente · Responsable: DGETD</p>')
    w("</section>")
    w("</main>")
    w('<script src="diseno/iconos.js"></script>\n</body>\n</html>\n')
    return "\n".join(out)


# -----------------------------------------------------------------------------
# Después de construir
# -----------------------------------------------------------------------------
class _Encabezados(HTMLParser):
    """Texto de cada h1–h6, sin lo visualmente oculto y con espacios normalizados."""

    def __init__(self):
        super().__init__()
        self.titulos, self._actual, self._pila = [], None, []

    def handle_starttag(self, tag, attrs):
        if re.fullmatch(r"h[1-6]", tag):
            self._actual, self._pila = [], []
        elif self._actual is not None:
            self._pila.append("visualmente-oculto" in (dict(attrs).get("class") or ""))

    def handle_endtag(self, tag):
        if re.fullmatch(r"h[1-6]", tag) and self._actual is not None:
            self.titulos.append(" ".join("".join(self._actual).split()))
            self._actual = None
        elif self._actual is not None and self._pila:
            self._pila.pop()

    def handle_data(self, data):
        if self._actual is not None and not any(self._pila):
            self._actual.append(data)


def corregir_marcadores_pdf(ruta_pdf, contenido_html):
    """Chromium arma los marcadores (outline) con el texto ya partido en renglones y pega palabras
    («Registro de unalista»); a veces repite el título. Se reescribe cada título con el texto del
    encabezado del HTML. No cambia nada más del PDF (etiquetas, fuentes, páginas)."""
    from pypdf import PdfWriter
    from pypdf.generic import NameObject, TextStringObject

    p = _Encabezados()
    p.feed(contenido_html)
    esperados = p.titulos

    def junto(t):
        return re.sub(r"\s+", "", t)

    escritor = PdfWriter(clone_from=ruta_pdf)
    raiz = escritor._root_object
    if "/Outlines" not in raiz:
        return 0
    cambios, i = 0, 0

    def recorrer(nodo):
        nonlocal cambios, i
        while nodo is not None:
            nodo = nodo.get_object()
            titulo = str(nodo.get("/Title", ""))
            for k in range(i, len(esperados)):
                if junto(esperados[k]) and junto(esperados[k]) in junto(titulo):
                    if esperados[k] != titulo:
                        nodo[NameObject("/Title")] = TextStringObject(esperados[k])
                        cambios += 1
                    i = k + 1
                    break
            if "/First" in nodo:
                recorrer(nodo["/First"])
            nodo = nodo.get("/Next")

    recorrer(raiz["/Outlines"].get_object().get("/First"))
    with open(ruta_pdf, "wb") as fh:
        escritor.write(fh)
    return cambios


def pagina_con(ruta_pdf, texto):
    """Número de página (1…) donde aparece `texto`, o None."""
    salida = subprocess.run(["pdftotext", "-layout", ruta_pdf, "-"], capture_output=True, text=True, check=True).stdout
    for n, pagina in enumerate(salida.split("\f"), start=1):
        if texto in " ".join(pagina.split()):
            return n
    return None


def main():
    args = sys.argv[1:]
    with open(SPEC, encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)
    pagina_oj = PAGINA_OJ
    for _ in range(2):
        contenido = construir(spec, pagina_oj)
        with open(SALIDA_HTML, "w", encoding="utf-8") as fh:
            fh.write(contenido)
        print(f"Escrito {os.path.relpath(SALIDA_HTML, RAIZ)}")
        if "--sin-pdf" in args:
            return
        cmd = ["node", "html_pdf.js", os.path.relpath(SALIDA_HTML, AQUI)] + [a for a in args if a in ("--png", "--borrador")]
        subprocess.run(cmd, cwd=AQUI, check=True)
        destino = "vista-previa" if "--borrador" in args else "entregables"
        pdf = os.path.join(RAIZ, destino, os.path.splitext(os.path.basename(SALIDA_HTML))[0] + ".pdf")
        real = pagina_con(pdf, TITULO_OJ)
        if real is None or real == pagina_oj:
            break
        print(f"El recuadro «{TITULO_OJ}» quedó en la página {real}, no en la {pagina_oj}: se reconstruye.")
        pagina_oj = real
    print(f"Marcadores del PDF corregidos: {corregir_marcadores_pdf(pdf, contenido)}")


if __name__ == "__main__":
    main()
