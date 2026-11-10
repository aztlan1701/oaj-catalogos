"""Convierte una fuente Markdown (con front matter YAML) en un .docx con el sistema visual de catálogos.

Uso:
    python3 construir.py ../fuentes/PR-CAT-04.md            # escribe ../entregables/PR-CAT-04.docx
    python3 construir.py ../fuentes/PR-CAT-04.md --pdf      # además, vista previa PDF en ../vista-previa/

Posproceso (python-docx): portada clara de la familia de la Hoja de valor (sin tablas de maquetación;
el título es un encabezado real), número de capítulo de cada H1 en mint-ink, etiqueta de cada recuadro
(«**Por confirmar.**») como chip en su propio párrafo dentro de la caja, corchetes literales en los
marcadores, guion no separable en códigos (F-CAT-01, CAT-0042, RC-2027-0118) de títulos y celdas,
figuras a lo ancho de la columna con su pie arriba, viñetas en mint, cebra suave en tablas, filas que no
se parten, encabezado y pie finos, fuentes incrustadas, idioma es-MX y compatibilidad de Word 2013+.

Front matter reconocido:
    codigo, titulo, subtitulo, tipo, version, fecha, estatus, responsable, fundamento,
    acento (opcional: palabras del título que van en mint-ink; si falta, se usa la tabla ACENTOS),
    portada: completa | breve | sin-ficha
        completa  = página propia: marca, etiqueta, título, subtítulo, ficha ligera, índice
                    «En este documento» con vínculos a cada capítulo y pie institucional
        breve     = la misma cabecera y ficha en la primera página; el texto sigue en la misma página
        sin-ficha = encabezado tipo oficio (circular): membrete con barra mint, estatus, título y caja de datos

Convenciones de Markdown (Pandoc):
    ::: {custom-style="Compromiso"}   bloques: Nota, Norma, Compromiso, Pendiente, Alerta, Etiqueta, Firma, Pequeno
    [texto]{custom-style="Marcador"}  marcador por confirmar; también Clave, Obligatorio, Dgetd
    Un párrafo Pequeno «Figura N. …» justo después de una imagen se vuelve su pie (arriba de la figura).
"""
import argparse
import copy
import os
import re
import shutil
import subprocess
import tempfile
import uuid
import zipfile

import yaml
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
REFERENCIA = os.path.join(AQUI, "reference.docx")
FUENTES_TTF = os.path.join(AQUI, "fuentes-tipograficas")


# Tokens en hexadecimal para el XML (mismos valores que referencia.py y kit.css).
H_INK, H_INK2, H_LINE, H_PANEL = "161A1D", "575F71", "E6EAEF", "F8FAFC"
H_MINT, H_MINT2, H_MINT_TINT, H_MINT_INK = "49B6B2", "78C9C6", "E8F5F4", "2A7370"
H_AMBER, H_AMBER_TINT, H_AMBER_INK = "D9950F", "FBF1DA", "8A5D06"

# Medidas de página (twips: 1 cm = 567).
PAGINA_ANCHO = 11906          # A4
MARGEN_LADO = 1361            # 2.4 cm
COLUMNA = PAGINA_ANCHO - 2 * MARGEN_LADO

RECUADROS = ("Nota", "Norma", "Compromiso", "Pendiente", "Alerta")

SERIF, SANS = "Source Serif 4", "Source Sans 3"
MONO, MONO_MED = "Source Code Pro", "Source Code Pro Medium"

# (familia en Word, tipo de incrustación, archivo)
EMBEBIDAS = [
    ("Source Sans 3", "embedRegular", "SourceSans3-Regular.ttf"),
    ("Source Sans 3", "embedBold", "SourceSans3-Bold.ttf"),
    ("Source Sans 3", "embedItalic", "SourceSans3-It.ttf"),
    ("Source Serif 4", "embedBold", "SourceSerif4-Bold.ttf"),
    ("Source Code Pro", "embedRegular", "SourceCodePro-Regular.ttf"),
    ("Source Code Pro Medium", "embedRegular", "SourceCodePro-Medium.ttf"),
]


def leer_front_matter(ruta):
    with open(ruta, encoding="utf-8") as fh:
        texto = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    meta = yaml.safe_load(m.group(1)) if m else {}
    return meta or {}


# --- Utilidades XML ------------------------------------------------------------

def el(tag, **attrs):
    """Crea un elemento w:… con atributos w:… (los nombres con _ se escriben sin prefijo w: si llevan ':')."""
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(k if ":" in k else "w:" + k), str(v))
    return e


def sub(parent, tag, **attrs):
    e = el(tag, **attrs)
    parent.append(e)
    return e


def rpr_xml(size=None, color=None, bold=False, font=None, caps=False, spacing=None, fill=None, rstyle=None):
    rpr = el("w:rPr")
    if rstyle:
        sub(rpr, "w:rStyle", val=rstyle)
    if font:
        sub(rpr, "w:rFonts", ascii=font, hAnsi=font, eastAsia=font, cs=font)
    if bold:
        sub(rpr, "w:b"); sub(rpr, "w:bCs")
    if caps:
        sub(rpr, "w:caps")
    if color:
        sub(rpr, "w:color", val=color)
    if spacing:
        sub(rpr, "w:spacing", val=spacing)
    if size:
        sub(rpr, "w:sz", val=int(size * 2)); sub(rpr, "w:szCs", val=int(size * 2))
    if fill:
        sub(rpr, "w:shd", val="clear", color="auto", fill=fill)
    return rpr


def run(p_el, texto, **fmt):
    r = sub(p_el, "w:r")
    r.append(rpr_xml(**fmt))
    t = sub(r, "w:t"); t.set(qn("xml:space"), "preserve"); t.text = texto
    return r


def tab_run(p_el):
    r = sub(p_el, "w:r"); sub(r, "w:tab")


def parrafo_xml(style=None, before=None, after=None, line=None, ind_left=None, ind_right=None,
                tabs=(), borders=None, keep_next=False, jc=None, fill=None, hanging=None):
    """Crea un w:p con pPr en el orden que exige el esquema."""
    p = el("w:p")
    ppr = sub(p, "w:pPr")
    if style:
        sub(ppr, "w:pStyle", val=style)
    if keep_next:
        sub(ppr, "w:keepNext")
    if borders:
        bdr = sub(ppr, "w:pBdr")
        for lado in ("top", "left", "bottom", "right"):
            if lado in borders:
                color, sz, space = borders[lado]
                sub(bdr, "w:" + lado, val="single", sz=sz, space=space, color=color)
    if fill:
        sub(ppr, "w:shd", val="clear", color="auto", fill=fill)
    if tabs:
        tb = sub(ppr, "w:tabs")
        for pos, alin in tabs:
            sub(tb, "w:tab", val=alin, pos=pos)
    if before is not None or after is not None or line is not None:
        sp = sub(ppr, "w:spacing")
        if before is not None:
            sp.set(qn("w:before"), str(before))
        if after is not None:
            sp.set(qn("w:after"), str(after))
        if line is not None:
            sp.set(qn("w:line"), str(line)); sp.set(qn("w:lineRule"), "auto")
    if ind_left is not None or ind_right is not None or hanging is not None:
        ind = sub(ppr, "w:ind")
        if ind_left is not None:
            ind.set(qn("w:left"), str(ind_left))
        if ind_right is not None:
            ind.set(qn("w:right"), str(ind_right))
        if hanging is not None:
            ind.set(qn("w:hanging"), str(hanging))
    if jc:
        sub(ppr, "w:jc", val=jc)
    return p


# --- Encabezado y pie ------------------------------------------------------------

def campo(fld_text, p_el, size=8, color=H_INK2):
    """Inserta un campo de Word (PAGE, NUMPAGES) en un párrafo."""
    def r_():
        r = sub(p_el, "w:r"); r.append(rpr_xml(size=size, color=color)); return r
    sub(r_(), "w:fldChar", fldCharType="begin")
    it = sub(r_(), "w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = f" {fld_text} "
    sub(r_(), "w:fldChar", fldCharType="separate")
    t = sub(r_(), "w:t"); t.text = "1"
    sub(r_(), "w:fldChar", fldCharType="end")


def limpiar(parte):
    """Vacía un encabezado o pie y devuelve su elemento raíz."""
    raiz = parte._element
    for hijo in list(raiz):
        raiz.remove(hijo)
    return raiz


def encabezado_normal(parte, meta):
    codigo = meta.get("codigo", "")
    version = meta.get("version", "")
    raiz = limpiar(parte)
    p = parrafo_xml(after=0, line=240, tabs=[(COLUMNA, "right")], borders={"left": (H_MINT, 24, 5)})
    if meta.get("portada") == "sin-ficha":
        # Circular: quien la emite sigue por confirmar, así que el encabezado no nombra a la DGETD.
        run(p, f"Órgano de Administración Judicial · {codigo or meta.get('tipo', '')}", size=8, bold=True, color=H_INK)
        tab_run(p)
        run(p, f"v{version}", size=7.5, color=H_INK2, font=MONO)
    else:
        run(p, "Órgano de Administración Judicial · DGETD", size=8, bold=True, color=H_INK)
        tab_run(p)
        run(p, f"{codigo or meta.get('tipo', '')}  ·  v{version}", size=7.5, color=H_INK2, font=MONO)
    raiz.append(p)


def pie_normal(parte, meta):
    estatus = meta.get("estatus", "Borrador para revisión")
    raiz = limpiar(parte)
    p = parrafo_xml(after=0, line=240, tabs=[(COLUMNA, "right")], borders={"top": (H_LINE, 4, 7)})
    run(p, estatus, size=8, color=H_INK2)
    tab_run(p)
    run(p, "Página ", size=8, color=H_INK2)
    campo("PAGE", p)
    run(p, " de ", size=8, color=H_INK2)
    campo("NUMPAGES", p)
    raiz.append(p)


def pie_portada(parte, meta):
    """Pie institucional de la portada completa."""
    raiz = limpiar(parte)
    p1 = parrafo_xml(after=0, line=260, tabs=[(COLUMNA, "right")], borders={"top": (H_MINT, 12, 10)})
    run(p1, "Dirección General de Estrategia y Transformación Digital", size=9.5, bold=True, color=H_INK)
    tab_run(p1)
    run(p1, str(meta.get("fecha", "")), size=8.5, color=H_INK2, font=MONO)
    p2 = parrafo_xml(before=20, after=0, line=260)
    run(p2, "Órgano de Administración Judicial", size=9, color=H_INK2)
    raiz.append(p1); raiz.append(p2)


def preparar_secciones(doc, meta):
    tipo_portada = meta.get("portada")
    secciones = list(doc.sections)
    for s in secciones:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.gutter = Cm(0)  # w:gutter es obligatorio en w:pgMar para Word
    cuerpo = secciones[-1]
    cuerpo.left_margin = cuerpo.right_margin = Cm(2.4)
    cuerpo.top_margin, cuerpo.bottom_margin = Cm(2.5), Cm(2.3)
    cuerpo.header_distance, cuerpo.footer_distance = Cm(1.2), Cm(1.1)
    cuerpo.header.is_linked_to_previous = False
    cuerpo.footer.is_linked_to_previous = False
    encabezado_normal(cuerpo.header, meta)
    pie_normal(cuerpo.footer, meta)

    if tipo_portada == "completa" and len(secciones) > 1:
        # Portada clara dentro de los márgenes de impresión (nada a sangre).
        port = secciones[0]
        port.left_margin = port.right_margin = Cm(2.4)
        port.top_margin, port.bottom_margin = Cm(2.0), Cm(3.1)
        port.header_distance, port.footer_distance = Cm(1.0), Cm(1.5)
        port.header.is_linked_to_previous = False
        limpiar(port.header).append(parrafo_xml(after=0))
        port.footer.is_linked_to_previous = False
        pie_portada(port.footer, meta)
    else:
        if tipo_portada == "sin-ficha":
            # Oficio: márgenes de arriba y abajo un poco menores.
            cuerpo.top_margin, cuerpo.bottom_margin = Cm(2.0), Cm(2.0)
            cuerpo.header_distance, cuerpo.footer_distance = Cm(1.0), Cm(1.0)
        # La primera página ya lleva la marca o el membrete en el cuerpo: sin encabezado repetido.
        cuerpo.different_first_page_header_footer = True
        limpiar(cuerpo.first_page_header).append(parrafo_xml(after=0))
        pie_normal(cuerpo.first_page_footer, meta)


# --- Portadas ----------------------------------------------------------------------
# Misma familia que la Hoja de valor y la Guía: página blanca, cuadro menta con la marca, etiqueta mono
# en mint-ink con raya menta, título serif en tinta con una o dos palabras en mint-ink, ficha ligera.
# Todo en párrafos (sin tablas de maquetación): el título es un encabezado real para la navegación.

# Palabras del título que van en mint-ink (como «mi área» en la Guía). Se puede fijar con `acento:`.
ACENTOS = {
    "ET-CAT-01": "catálogos institucionales",
    "PR-CAT-04": "catálogos existentes",
    "F-CAT-01": "catálogo existente",
    "Circular-registro": "su área",
    "implementacion-registro": "registro de catálogos",
}


def etiqueta_portada(meta):
    tipo = meta.get("tipo", "")
    codigo = meta.get("codigo", "")
    if tipo and codigo and tipo.lower() in codigo.lower():
        return codigo
    return " · ".join(x for x in (tipo, codigo) if x)


def p_marca(before=0):
    """Cuadro menta + «Órgano de Administración Judicial · DGETD», y a la derecha la colección."""
    p = parrafo_xml(before=before, after=0, line=240, tabs=[(COLUMNA, "right")])
    # Cuadro menta: espacios duros con fondo menta (adorno; no se lee como texto).
    run(p, "\u2003", size=10, fill=H_MINT)
    run(p, "\u2002\u2002Órgano de Administración Judicial · DGETD", size=9, bold=True, color=H_INK)
    tab_run(p)
    run(p, "Catálogos institucionales", size=7.5, color=H_MINT_INK, font=MONO_MED, caps=True, spacing=14)
    return p


def p_etiqueta(texto, before):
    p = parrafo_xml(style="Etiqueta", before=before, after=140, keep_next=True)
    run(p, "\u2014\u2014", color=H_MINT, font=SANS, bold=True, size=9, spacing=-20)
    run(p, "\u2002" + texto)
    return p


def p_titulo(meta, base, size, after=220):
    titulo = guiones_no_separables(meta.get("titulo", ""))
    acento = meta.get("acento") or ACENTOS.get(meta.get("codigo", "")) or ACENTOS.get(base)
    p = parrafo_xml(style="Title", after=after, line=240)
    i = titulo.rfind(acento) if acento else -1
    if i >= 0:
        if titulo[:i]:
            run(p, titulo[:i], size=size)
        run(p, acento, size=size, color=H_MINT_INK)
        if titulo[i + len(acento):]:
            run(p, titulo[i + len(acento):], size=size)
    else:
        run(p, titulo, size=size)
    return p


def p_subtitulo(meta, size=13, after=0):
    p = parrafo_xml(style="Subtitle", after=after, line=290)
    run(p, meta["subtitulo"], size=size)
    return p


# Posiciones de la ficha (twips): etiqueta, dato; en la primera fila, tres pares.
FICHA_DATO = 2200
FICHA_PARES = [(0, 2200), (3900, 4900), (5900, 6700)]


def ficha_parrafos(meta, before):
    """Ficha ligera en párrafos con tabulaciones: filete menta arriba, filete gris abajo, sin tabla."""
    def etq(p, texto):
        run(p, texto, size=7.5, color=H_INK2, font=MONO_MED, caps=True, spacing=12)

    def dato(p, etiqueta, valor):
        if etiqueta in ("Código", "Versión"):
            run(p, valor, size=10, color=H_INK, font=MONO)
        elif etiqueta == "Estatus":
            run(p, "\u00a0" + valor + "\u00a0", rstyle="ChipEstatus")
        else:
            run(p, valor, size=10, color=H_INK)

    cortos = [(e, v) for e, v in (("Código", meta.get("codigo", "")), ("Versión", str(meta.get("version", ""))),
                                  ("Fecha", str(meta.get("fecha", "")))) if v]
    largos = [(e, v) for e, v in (("Estatus", meta.get("estatus", "")), ("Área responsable", meta.get("responsable", "")),
                                  ("Fundamento", meta.get("fundamento", ""))) if v]
    parrafos = []
    if cortos:
        tabs = []
        for i, _ in enumerate(cortos):
            x_etq, x_dato = FICHA_PARES[i]
            if x_etq:
                tabs.append((x_etq, "left"))
            tabs.append((x_dato, "left"))
        p = parrafo_xml(style="FichaDato", tabs=tabs)
        for i, (e, v) in enumerate(cortos):
            if i:
                tab_run(p)
            etq(p, e); tab_run(p); dato(p, e, v)
        parrafos.append(p)
    for e, v in largos:
        p = parrafo_xml(style="FichaDato", tabs=[(FICHA_DATO, "left")], ind_left=FICHA_DATO, hanging=FICHA_DATO)
        etq(p, e); tab_run(p); dato(p, e, v)
        parrafos.append(p)
    # Aire arriba del primer renglón (el estilo da 0).
    ppr = parrafos[0].find(qn("w:pPr"))
    sp = ppr.find(qn("w:spacing"))
    if sp is None:
        sp = el("w:spacing")
        ind = ppr.find(qn("w:ind"))
        (ind.addprevious if ind is not None else ppr.append)(sp)
    sp.set(qn("w:before"), str(before))
    return parrafos


def capitulos(doc):
    """Lista de H1 del cuerpo: (número para mostrar, título, marcador de Word)."""
    lista = []
    for p in doc.element.body.iter(qn("w:p")):
        if estilo_de(p) != "Heading1":
            continue
        texto = "".join(t.text or "" for t in p.iter(qn("w:t"))).strip()
        previo = p.getprevious()
        ancla = previo.get(qn("w:name")) if previo is not None and previo.tag == qn("w:bookmarkStart") else None
        m = re.match(r"^(\d+|Anexo ([A-Z]))\.\s+(.*)$", texto)
        if m:
            num = m.group(2) or f"{int(m.group(1)):02d}"
            lista.append((num, m.group(3), ancla))
        else:
            lista.append(("—", texto, ancla))
    return lista


def indice_parrafos(doc):
    """«En este documento»: capítulos numerados en mono, cada uno con vínculo a su capítulo."""
    caps = capitulos(doc)
    if not caps:
        return []
    out = []
    p = parrafo_xml(style="Etiqueta", before=340, after=60, keep_next=True)
    run(p, "\u2014\u2014", color=H_LINE, font=SANS, bold=True, size=9, spacing=-20)
    run(p, "\u2002En este documento", color=H_INK2)
    out.append(p)
    for n, (num, titulo, ancla) in enumerate(caps):
        # Sangría derecha alterna para que Word y LibreOffice no fundan los filetes de renglones seguidos.
        p = parrafo_xml(style="IndiceEntrada", ind_right=0 if n % 2 else 20)
        cont = p
        if ancla:
            cont = sub(p, "w:hyperlink", anchor=ancla)
        run(cont, num, size=8.5, color=H_MINT_INK, font=MONO_MED)
        tab_run(cont)
        run(cont, guiones_no_separables(titulo), size=10, color=H_INK)
        out.append(p)
    return out


def portada_completa(doc, meta, base, antes):
    """Página propia, clara: marca, etiqueta, título, subtítulo, ficha e índice; pie institucional."""
    ins = antes.addprevious
    ins(p_marca())
    ins(p_etiqueta(etiqueta_portada(meta), before=480))
    ins(p_titulo(meta, base, size=31, after=240 if meta.get("subtitulo") else 0))
    if meta.get("subtitulo"):
        ins(p_subtitulo(meta, size=13))
    for p in ficha_parrafos(meta, before=420):
        ins(p)
    for p in indice_parrafos(doc):
        ins(p)


def portada_breve(doc, meta, base, antes):
    """Encabezado claro en la primera página; el texto sigue en la misma página."""
    ins = antes.addprevious
    ins(p_marca())
    ins(p_etiqueta(etiqueta_portada(meta), before=900))
    ins(p_titulo(meta, base, size=28, after=200 if meta.get("subtitulo") else 0))
    if meta.get("subtitulo"):
        ins(p_subtitulo(meta, size=12.5))
    for p in ficha_parrafos(meta, before=440):
        ins(p)
    ins(parrafo_xml(before=0, after=200, line=240))


def portada_oficio(doc, meta, base, antes):
    """Encabezado tipo oficio: membrete con barra mint, estatus, etiqueta y título (encabezado real)."""
    ins = antes.addprevious
    barra = {"left": (H_MINT, 48, 9)}
    p = parrafo_xml(before=0, after=0, line=250, tabs=[(COLUMNA, "right")], borders=barra, ind_left=200)
    run(p, "Órgano de Administración Judicial", size=13, bold=True, color=H_INK, font=SERIF)
    tab_run(p)
    if meta.get("estatus"):
        run(p, "\u00a0" + meta["estatus"] + "\u00a0", rstyle="ChipEstatus")
    ins(p)
    p = parrafo_xml(before=30, after=0, line=250, borders=barra, ind_left=200)
    run(p, "Proyecto preparado por la Dirección General de Estrategia y Transformación Digital (DGETD)",
        size=9.5, color=H_INK2)
    ins(p)
    ins(p_etiqueta(etiqueta_portada(meta), before=360))
    ins(p_titulo(meta, base, size=26, after=100))
    if meta.get("subtitulo"):
        ins(p_subtitulo(meta, size=12.5, after=200))
    # El primer párrafo del cuerpo (número de circular, quién emite, a quién se dirige) va en caja de datos.
    if antes.tag == qn("w:p"):
        ppr = antes.find(qn("w:pPr"))
        if ppr is None:
            ppr = el("w:pPr"); antes.insert(0, ppr)
        ps = ppr.find(qn("w:pStyle"))
        if ps is None:
            ps = el("w:pStyle"); ppr.insert(0, ps)
        ps.set(qn("w:val"), "DatosOficio")


def portada(doc, meta, base):
    cuerpo = doc.element.body
    primero = cuerpo[0]
    tipo = meta.get("portada")
    if tipo == "completa":
        portada_completa(doc, meta, base, primero)
        # Párrafo que cierra la sección de portada y la separa del cuerpo.
        sect_cuerpo = cuerpo.find(qn("w:sectPr"))
        sect = copy.deepcopy(sect_cuerpo)
        for ref in sect.findall(qn("w:headerReference")) + sect.findall(qn("w:footerReference")):
            sect.remove(ref)
        p = parrafo_xml(before=0, after=0, line=240)
        p.find(qn("w:pPr")).append(sect)
        primero.addprevious(p)
        tipo_sec = sect_cuerpo.find(qn("w:type"))
        if tipo_sec is None:
            tipo_sec = el("w:type"); sect_cuerpo.insert(0, tipo_sec)
        tipo_sec.set(qn("w:val"), "nextPage")
    elif tipo == "sin-ficha":
        portada_oficio(doc, meta, base, primero)
    else:
        portada_breve(doc, meta, base, primero)

# --- Detalles del cuerpo -------------------------------------------------------------

def estilo_de(p):
    ps = p.find(qn("w:pPr") + "/" + qn("w:pStyle"))
    return ps.get(qn("w:val")) if ps is not None else None


def textos(p):
    return [t for t in p.iter(qn("w:t"))]


def numero_capitulo(doc):
    """Colorea en mint-ink el número de capítulo de cada H1 («1.», «Anexo A.»)."""
    for p in doc.element.body.iter(qn("w:p")):
        if estilo_de(p) != "Heading1":
            continue
        r = p.find(qn("w:r"))
        if r is None:
            continue
        t = r.find(qn("w:t"))
        if t is None or not t.text:
            continue
        m = re.match(r"^((?:\d+|Anexo [A-Z])\.)(\s+)", t.text)
        if not m:
            continue
        nuevo = copy.deepcopy(r)
        rpr = nuevo.find(qn("w:rPr"))
        if rpr is None:
            rpr = el("w:rPr"); nuevo.insert(0, rpr)
        rpr.insert(0, el("w:rStyle", val="NumeroCapitulo"))
        nt = nuevo.find(qn("w:t")); nt.text = m.group(1) + "\u2002"; nt.set(qn("xml:space"), "preserve")
        t.text = t.text[m.end():]
        r.addprevious(nuevo)


def recuadros(doc):
    """Etiqueta del recuadro como chip en su propio párrafo (dentro de la caja) y aire arriba y abajo.

    El chip va en un párrafo aparte con el mismo estilo de caja: se ve dentro del recuadro y la lectura
    en voz alta hace la pausa entre la etiqueta y el texto.
    """
    hijos = list(doc.element.body)
    for i, p in enumerate(hijos):
        if p.tag != qn("w:p"):
            continue
        est = estilo_de(p)
        if est not in RECUADROS:
            continue
        previo = hijos[i - 1] if i else None
        sig = hijos[i + 1] if i + 1 < len(hijos) else None
        es_primero = previo is None or previo.tag != qn("w:p") or estilo_de(previo) != est
        es_ultimo = sig is None or sig.tag != qn("w:p") or estilo_de(sig) != est
        ppr = p.find(qn("w:pPr"))
        sp = ppr.find(qn("w:spacing"))
        if sp is None:
            sp = el("w:spacing"); ppr.append(sp)
        sp.set(qn("w:before"), "280" if es_primero else "0")
        sp.set(qn("w:after"), "280" if es_ultimo else "120")
        if not es_primero:
            continue
        r = p.find(qn("w:r"))
        if r is None or r.find(qn("w:rPr") + "/" + qn("w:b")) is None:
            continue
        t = r.find(qn("w:t"))
        if t is None or not t.text:
            continue
        etiqueta = t.text.strip().rstrip(".:").strip()
        if not etiqueta or len(etiqueta) > 48:
            continue
        rpr = r.find(qn("w:rPr"))
        for hijo in list(rpr):
            rpr.remove(hijo)
        rpr.append(el("w:rStyle", val="Chip" + est))
        t.text = "\u00a0" + etiqueta + "\u00a0"
        t.set(qn("xml:space"), "preserve")
        # Párrafo propio para el chip, con el mismo estilo de caja.
        chip_p = el("w:p")
        chip_ppr = copy.deepcopy(ppr)
        chip_p.append(chip_ppr)
        chip_ppr.insert(1, el("w:keepNext"))
        csp = chip_ppr.find(qn("w:spacing"))
        csp.set(qn("w:before"), "280"); csp.set(qn("w:after"), "60")
        sp.set(qn("w:before"), "0")
        p.addprevious(chip_p)
        chip_p.append(r)
        # Quita el espacio que separaba la etiqueta del texto.
        for r2 in p.findall(qn("w:r")):
            ts = r2.findall(qn("w:t"))
            if not ts:
                continue
            ts[0].text = (ts[0].text or "").lstrip()
            if ts[0].text:
                break
            r2.getparent().remove(r2)


def marcadores(doc):
    """Corchetes literales en cada marcador (pandoc los quita); dentro de «Pendiente», fondo blanco."""
    for p in doc.element.body.iter(qn("w:p")):
        grupo = []
        grupos = []
        for hijo in p:
            es_marc = hijo.tag == qn("w:r") and hijo.find(qn("w:rPr") + "/" + qn("w:rStyle")) is not None and \
                hijo.find(qn("w:rPr") + "/" + qn("w:rStyle")).get(qn("w:val")) == "Marcador"
            if es_marc:
                grupo.append(hijo)
            elif grupo:
                grupos.append(grupo); grupo = []
        if grupo:
            grupos.append(grupo)
        en_pendiente = estilo_de(p) == "Pendiente"
        for g in grupos:
            ts = [t for r in g for t in r.findall(qn("w:t"))]
            if not ts:
                continue
            if not (ts[0].text or "").startswith("["):
                ts[0].text = "[" + (ts[0].text or "")
            if not (ts[-1].text or "").endswith("]"):
                ts[-1].text = (ts[-1].text or "") + "]"
            for t in ts:
                t.set(qn("xml:space"), "preserve")
            if en_pendiente:
                # Sobre el fondo ámbar del recuadro, el marcador va en blanco para seguir distinguiéndose.
                for r in g:
                    rpr = r.find(qn("w:rPr"))
                    if rpr.find(qn("w:shd")) is None:
                        rpr.append(el("w:shd", val="clear", color="auto", fill="FFFFFF"))


CODIGO_RE = re.compile(r"(?<![\w\u2011-])(?:[A-Z]{1,3}-)?(?:CAT|RC)-[0-9A-Z]{2,4}(?:-[0-9A-Z]{2,4})?(?![\w-])")


def guiones_no_separables(texto):
    """F-CAT-01, CAT-0042, RC-2027-0118: guion no separable (U+2011) para que el código no se parta."""
    return CODIGO_RE.sub(lambda m: m.group(0).replace("-", "\u2011"), texto)


def es_mono(r):
    rpr = r.find(qn("w:rPr"))
    if rpr is None:
        return False
    rs = rpr.find(qn("w:rStyle"))
    if rs is not None and rs.get(qn("w:val")) in ("Clave", "VerbatimChar"):
        return True
    rf = rpr.find(qn("w:rFonts"))
    return rf is not None and "Code" in (rf.get(qn("w:ascii")) or "")


def codigos_enteros(doc):
    """Aplica el guion no separable en títulos, pies y celdas de tabla (Source Code Pro no lo tiene)."""
    estilos = {"Heading1", "Heading2", "Heading3", "Heading4", "Title", "TableCaption", "ImageCaption"}
    for p in doc.element.body.iter(qn("w:p")):
        en_tabla = any(a.tag == qn("w:tc") for a in p.iterancestors())
        if not en_tabla and estilo_de(p) not in estilos:
            continue
        for r in p.iter(qn("w:r")):
            if es_mono(r):
                continue
            for t in r.findall(qn("w:t")):
                if t.text:
                    t.text = guiones_no_separables(t.text)


def tablas_anchas(doc):
    """En tablas de 5 o más columnas, menos relleno lateral de celda para que el texto respire."""
    for tbl in doc.element.body.iter(qn("w:tbl")):
        grid = tbl.find(qn("w:tblGrid"))
        if grid is None or len(grid.findall(qn("w:gridCol"))) < 5:
            continue
        tblPr = tbl.find(qn("w:tblPr"))
        if tblPr is None or tblPr.find(qn("w:tblCellMar")) is not None:
            continue
        cm = el("w:tblCellMar")
        for lado, v in (("top", 110), ("left", 80), ("bottom", 80), ("right", 80)):
            sub(cm, "w:" + lado, w=v, type="dxa")
        look = tblPr.find(qn("w:tblLook"))
        (look.addprevious if look is not None else tblPr.append)(cm)


ALTO_MAX_FIGURA = int(20.6 * 360000)   # EMU: la figura, su pie y el título del capítulo caben en una página
ANCHO_COLUMNA_EMU = COLUMNA * 635      # twips a EMU


def figuras(doc):
    """Pie de figura arriba, con el mismo estilo que el título de tabla, pegado a su figura."""
    for p in list(doc.element.body.iter(qn("w:p"))):
        dib = p.find(".//" + qn("w:drawing"))
        if dib is None:
            continue
        # A lo ancho de la columna (pandoc usa un ancho de texto genérico para width=100%),
        # sin pasar de la altura máxima y conservando la proporción.
        ext = dib.find(".//" + qn("wp:extent"))
        if ext is not None:
            cx, cy = int(ext.get("cx")), int(ext.get("cy"))
            ncx = ANCHO_COLUMNA_EMU
            ncy = int(cy * ncx / cx)
            if ncy > ALTO_MAX_FIGURA:
                ncx, ncy = int(ncx * ALTO_MAX_FIGURA / ncy), ALTO_MAX_FIGURA
            ext.set("cx", str(ncx)); ext.set("cy", str(ncy))
            for a_ext in dib.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}ext"):
                if a_ext.get("cx"):
                    a_ext.set("cx", str(ncx)); a_ext.set("cy", str(ncy))
        sig = p.getnext()
        if sig is None or sig.tag != qn("w:p") or estilo_de(sig) != "Pequeno":
            continue
        texto = "".join(t.text or "" for t in sig.iter(qn("w:t"))).strip()
        if not re.match(r"^Figura \d+\.", texto):
            continue
        sig.find(qn("w:pPr") + "/" + qn("w:pStyle")).set(qn("w:val"), "ImageCaption")
        p.addprevious(sig)
        ppr = p.find(qn("w:pPr"))
        if ppr is None:
            ppr = el("w:pPr"); p.insert(0, ppr)
        ps = ppr.find(qn("w:pStyle"))
        if ps is not None:
            ps.set(qn("w:val"), "Figure")
        else:
            ppr.insert(0, el("w:pStyle", val="Figure"))


def ajustes_oficio(doc, meta):
    """Circular: espaciado compacto (mismo cuerpo de letra) y nota interna bien separada de la firma."""
    if meta.get("portada") != "sin-ficha":
        return

    def espacio(p, before=None, after=None):
        ppr = p.find(qn("w:pPr"))
        if ppr is None:
            ppr = el("w:pPr"); p.insert(0, ppr)
        sp = ppr.find(qn("w:spacing"))
        if sp is None:
            sp = el("w:spacing")
            despues = [h for h in ppr if h.tag in (qn("w:ind"), qn("w:jc"), qn("w:outlineLvl"), qn("w:rPr"), qn("w:sectPr"))]
            (despues[0].addprevious if despues else ppr.append)(sp)
        if before is not None:
            sp.set(qn("w:before"), str(before))
        if after is not None:
            sp.set(qn("w:after"), str(after))

    hijos = doc.element.body.findall(qn("w:p"))
    vio_firma = False
    for i, p in enumerate(hijos):
        est = estilo_de(p)
        if est == "Heading2":
            espacio(p, 220, 40)
        elif est in ("BodyText", "FirstParagraph"):
            espacio(p, after=110)
        elif est == "Compact":
            espacio(p, 0, 40)
        elif est == "Firma":
            if not vio_firma:
                espacio(p, before=260)
            vio_firma = True
        elif est == "Compromiso":
            ppr = p.find(qn("w:pPr")); sp = ppr.find(qn("w:spacing"))
            if sp.get(qn("w:before")) == "280":
                sp.set(qn("w:before"), "200")
            if sp.get(qn("w:after")) == "280":
                sp.set(qn("w:after"), "200")
        elif est == "Pendiente" and vio_firma:
            # Nota interna después de la firma: bien separada del texto que se firma.
            espacio(p, before=720)
            vio_firma = False


def listas(doc):
    """Viñetas en mint y números en mint-ink, con sangría más corta."""
    try:
        numeracion = doc.part.numbering_part.element
    except Exception:
        return
    vinetas = ["\u2022", "\u2013", "\u2022", "\u2013", "\u2022", "\u2013", "\u2022", "\u2013", "\u2022"]
    for lvl in numeracion.iter(qn("w:lvl")):
        nivel = int(lvl.get(qn("w:ilvl")))
        fmt = lvl.find(qn("w:numFmt"))
        es_vineta = fmt is not None and fmt.get(qn("w:val")) == "bullet"
        if es_vineta:
            lt = lvl.find(qn("w:lvlText"))
            if lt is not None:
                lt.set(qn("w:val"), vinetas[nivel])
        ppr = lvl.find(qn("w:pPr"))
        if ppr is None:
            ppr = sub(lvl, "w:pPr")
        ind = ppr.find(qn("w:ind"))
        if ind is None:
            ind = sub(ppr, "w:ind")
        ind.set(qn("w:left"), str(400 + 400 * nivel))
        ind.set(qn("w:hanging"), "300" if es_vineta else "360")
        rpr = lvl.find(qn("w:rPr"))
        if rpr is not None:
            lvl.remove(rpr)
        if es_vineta:
            rpr = rpr_xml(font="Source Sans 3", color="49B6B2", bold=True)
        else:
            rpr = rpr_xml(font="Source Sans 3", color=H_MINT_INK, bold=True)
        lvl.append(rpr)


def propiedades(doc, meta):
    cp = doc.core_properties
    cp.title = f"{meta.get('codigo', '')} {meta.get('titulo', '')}".strip()
    cp.subject = meta.get("subtitulo", "") or meta.get("tipo", "")
    cp.author = "Dirección General de Estrategia y Transformación Digital (DGETD)"
    cp.language = "es-MX"
    cp.keywords = "catálogos institucionales; OAJ; DGETD"
    cp.comments = meta.get("estatus", "")


def ofuscar(datos, guid):
    hexa = guid.strip("{}").replace("-", "")
    clave = [int(hexa[i:i + 2], 16) for i in range(0, 32, 2)][::-1]
    b = bytearray(datos)
    for i in range(32):
        b[i] ^= clave[i % 16]
    return bytes(b)


def incrustar_fuentes(ruta_docx):
    if not os.path.isdir(FUENTES_TTF):
        print("  (sin carpeta de tipografías; no se incrustan)")
        return
    tmp = ruta_docx + ".tmp"
    familias = {}
    archivos = {}
    rels = []
    for n, (familia, tipo, archivo) in enumerate(EMBEBIDAS, start=1):
        guid = "{" + str(uuid.uuid4()).upper() + "}"
        rid = f"rIdFont{n}"
        with open(os.path.join(FUENTES_TTF, archivo), "rb") as fh:
            archivos[f"word/fonts/font{n}.odttf"] = ofuscar(fh.read(), guid)
        rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/font{n}.odttf"/>')
        familias.setdefault(familia, []).append(f'<w:{tipo} r:id="{rid}" w:fontKey="{guid}"/>')

    orden = ["embedRegular", "embedBold", "embedItalic", "embedBoldItalic"]
    fuentes_xml = ""
    for familia, emb in familias.items():
        emb.sort(key=lambda x: orden.index(re.search(r"<w:(\w+)", x).group(1)))
        fuentes_xml += (f'<w:font w:name="{familia}"><w:charset w:val="00"/><w:family w:val="auto"/>'
                        f'<w:pitch w:val="variable"/>{"".join(emb)}</w:font>')
    font_table = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                  '<w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                  'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                  f'{fuentes_xml}</w:fonts>')
    font_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 f'{"".join(rels)}</Relationships>')

    with zipfile.ZipFile(ruta_docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename.endswith("/") or item.filename.startswith("word/fonts/") \
                    or item.filename == "word/_rels/fontTable.xml.rels":
                continue
            data = zin.read(item.filename)
            if item.filename == "word/fontTable.xml":
                data = font_table.encode("utf-8")
            elif item.filename == "word/settings.xml":
                s = data.decode("utf-8")
                if "embedTrueTypeFonts" not in s:
                    s = re.sub(r"(<w:zoom[^>]*/>)", r"\1<w:embedTrueTypeFonts/>", s, count=1)
                if "compatibilityMode" not in s:
                    # Modo de compatibilidad de Word 2013+: la sangría de tabla se mide al borde de la celda.
                    compat = ('<w:compat><w:compatSetting w:name="compatibilityMode" '
                              'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>')
                    s = re.sub(r"(<w:rsids|<w:clrSchemeMapping)", compat + r"\1", s, count=1)
                data = s.encode("utf-8")
            elif item.filename == "[Content_Types].xml":
                s = data.decode("utf-8")
                if 'Extension="odttf"' not in s:
                    s = s.replace("<Types ", "<Types ", 1).replace(
                        "<Default ", '<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/><Default ', 1)
                data = s.encode("utf-8")
            zout.writestr(item.filename, data)
        for nombre, data in archivos.items():
            zout.writestr(nombre, data)
        zout.writestr("word/_rels/fontTable.xml.rels", font_rels)
    os.replace(tmp, ruta_docx)


def cebra(doc):
    """Cebra muy suave (panel) en las filas pares de datos de las tablas de contenido.

    Se aplica directo en cada celda porque LibreOffice no siempre respeta las bandas del estilo de tabla.
    """
    for tbl in doc.element.body.iter(qn("w:tbl")):
        est = tbl.find(qn("w:tblPr") + "/" + qn("w:tblStyle"))
        if est is None or est.get(qn("w:val")) != "Table":
            continue
        filas = tbl.findall(qn("w:tr"))
        for n, tr in enumerate(filas[1:], start=1):
            if n % 2:
                continue
            for tc in tr.findall(qn("w:tc")):
                tcPr = tc.find(qn("w:tcPr"))
                if tcPr is None:
                    tcPr = el("w:tcPr"); tc.insert(0, tcPr)
                if tcPr.find(qn("w:shd")) is None:
                    tcPr.append(el("w:shd", val="clear", color="auto", fill=H_PANEL))


def aire_tras_tablas(doc):
    """Separa de la tabla el párrafo de texto que la sigue (pandoc lo pega al filete inferior)."""
    for tbl in doc.element.body.findall(qn("w:tbl")):
        sig = tbl.getnext()
        if sig is None or sig.tag != qn("w:p"):
            continue
        if estilo_de(sig) not in (None, "BodyText", "FirstParagraph", "Compact", "Pequeno"):
            continue
        ppr = sig.find(qn("w:pPr"))
        if ppr is None:
            ppr = el("w:pPr"); sig.insert(0, ppr)
        sp = ppr.find(qn("w:spacing"))
        if sp is None:
            sp = el("w:spacing")
            despues = [h for h in ppr if h.tag in (qn("w:ind"), qn("w:jc"), qn("w:outlineLvl"), qn("w:rPr"))]
            (despues[0].addprevious if despues else ppr.append)(sp)
        if sp.get(qn("w:before")) in (None, "0"):
            sp.set(qn("w:before"), "200")


def filas_enteras(doc):
    """Evita que una fila de tabla se parta entre dos páginas (w:cantSplit)."""
    for fila in doc.element.body.iter(qn("w:tr")):
        trPr = fila.find(qn("w:trPr"))
        if trPr is None:
            trPr = OxmlElement("w:trPr"); fila.insert(0, trPr)
        if trPr.find(qn("w:cantSplit")) is None:
            trPr.insert(0, OxmlElement("w:cantSplit"))


def construir(ruta_md, pdf=False):
    meta = leer_front_matter(ruta_md)
    base = os.path.splitext(os.path.basename(ruta_md))[0]
    destino_dir = os.path.join(RAIZ, "entregables")
    os.makedirs(destino_dir, exist_ok=True)
    destino = os.path.join(destino_dir, base + ".docx")
    recursos = os.path.dirname(os.path.abspath(ruta_md))

    subprocess.run(["pandoc", ruta_md, "-f", "markdown+fenced_divs+bracketed_spans+pipe_tables+grid_tables",
                    "-t", "docx", "--columns=20", "--reference-doc", REFERENCIA, "--resource-path", recursos + ":" + RAIZ,
                    "-o", destino], check=True)

    doc = Document(destino)
    figuras(doc)
    portada(doc, meta, base)
    numero_capitulo(doc)
    recuadros(doc)
    ajustes_oficio(doc, meta)
    marcadores(doc)
    codigos_enteros(doc)
    listas(doc)
    cebra(doc)
    tablas_anchas(doc)
    aire_tras_tablas(doc)
    filas_enteras(doc)
    preparar_secciones(doc, meta)
    propiedades(doc, meta)
    doc.save(destino)
    incrustar_fuentes(destino)
    print("  docx:", os.path.relpath(destino, RAIZ))

    if pdf:
        vista = os.path.join(RAIZ, "vista-previa")
        os.makedirs(vista, exist_ok=True)
        perfil = tempfile.mkdtemp(prefix="lo-perfil-")
        subprocess.run(["soffice", f"-env:UserInstallation=file://{perfil}", "--headless", "--convert-to", "pdf",
                        "--outdir", vista, destino], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.rmtree(perfil, ignore_errors=True)
        print("  pdf: ", os.path.relpath(os.path.join(vista, base + ".pdf"), RAIZ))
    return destino


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("fuentes", nargs="+")
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    for f in a.fuentes:
        print(os.path.basename(f))
        construir(f, a.pdf)
