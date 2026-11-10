"""Convierte una fuente Markdown (con front matter YAML) en un .docx con el sistema visual de catálogos.

Uso:
    python3 construir.py ../fuentes/PR-CAT-04.md            # escribe ../entregables/PR-CAT-04.docx
    python3 construir.py ../fuentes/PR-CAT-04.md --pdf      # además, vista previa PDF en ../vista-previa/

Posproceso (python-docx): portada según `portada`, número de capítulo de cada H1 en mint-ink,
etiqueta inicial de cada recuadro («**Por confirmar.**») convertida en chip en su propia línea,
viñetas en mint y números en mint-ink, cebra suave en tablas, filas que no se parten, encabezado y
pie finos, fuentes incrustadas, idioma es-MX y modo de compatibilidad de Word 2013+.

Front matter reconocido:
    codigo, titulo, subtitulo, tipo, version, fecha, estatus, responsable, fundamento,
    portada: completa | breve | sin-ficha
        completa  = página propia: franja de tinta a sangre, ficha ligera y pie institucional
        breve     = franja mint-tint a lo ancho de la página y ficha ligera; el texto sigue en la misma página
        sin-ficha = encabezado tipo oficio (circular): membrete con barra mint, estatus, título y caja de datos

Convenciones de Markdown (Pandoc):
    ::: {custom-style="Compromiso"}   bloques: Nota, Norma, Compromiso, Pendiente, Alerta, Etiqueta, Firma, Pequeno
    [texto]{custom-style="Marcador"}  marcador por confirmar; también Clave, Obligatorio, Dgetd
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
                tabs=(), borders=None, keep_next=False, jc=None, fill=None):
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
    if ind_left is not None or ind_right is not None:
        ind = sub(ppr, "w:ind")
        if ind_left is not None:
            ind.set(qn("w:left"), str(ind_left))
        if ind_right is not None:
            ind.set(qn("w:right"), str(ind_right))
    if jc:
        sub(ppr, "w:jc", val=jc)
    return p


def tabla_xml(anchos, ind=0, mar=(0, 0, 0, 0), bordes=None):
    """Tabla de maquetación sin estilo: anchos en twips, márgenes de celda (arriba, izq, abajo, der)."""
    tbl = el("w:tbl")
    tblPr = sub(tbl, "w:tblPr")
    sub(tblPr, "w:tblW", w=sum(anchos), type="dxa")
    sub(tblPr, "w:tblInd", w=ind, type="dxa")
    b = sub(tblPr, "w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        if bordes and lado in bordes:
            color, sz = bordes[lado]
            sub(b, "w:" + lado, val="single", sz=sz, space=0, color=color)
        else:
            sub(b, "w:" + lado, val="nil")
    sub(tblPr, "w:tblLayout", type="fixed")
    cm = sub(tblPr, "w:tblCellMar")
    for lado, v in zip(("top", "left", "bottom", "right"), mar):
        sub(cm, "w:" + lado, w=v, type="dxa")
    sub(tblPr, "w:tblLook", val="0000", firstRow=0, lastRow=0, firstColumn=0, lastColumn=0, noHBand=1, noVBand=1)
    grid = sub(tbl, "w:tblGrid")
    for a in anchos:
        sub(grid, "w:gridCol", w=a)
    return tbl


def fila_xml(tbl, anchos, fill=None, borde_inf=None):
    tr = sub(tbl, "w:tr")
    trPr = sub(tr, "w:trPr"); sub(trPr, "w:cantSplit")
    celdas = []
    for a in anchos:
        tc = sub(tr, "w:tc")
        tcPr = sub(tc, "w:tcPr")
        sub(tcPr, "w:tcW", w=a, type="dxa")
        if borde_inf:
            bd = sub(tcPr, "w:tcBorders")
            color, sz = borde_inf
            sub(bd, "w:bottom", val="single", sz=sz, space=0, color=color)
        if fill:
            sub(tcPr, "w:shd", val="clear", color="auto", fill=fill)
        celdas.append(tc)
    return celdas


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


def encabezado_normal(parte, meta, ind=0):
    codigo = meta.get("codigo", "")
    version = meta.get("version", "")
    raiz = limpiar(parte)
    p = parrafo_xml(after=0, line=240, tabs=[(COLUMNA + ind, "right")], ind_left=ind,
                    borders={"left": (H_MINT, 24, 5)})
    run(p, "Órgano de Administración Judicial · DGETD", size=8, bold=True, color=H_INK)
    tab_run(p)
    if codigo:
        run(p, f"{codigo}  ·  v{version}", size=7.5, color=H_INK2, font="Source Code Pro")
    else:
        run(p, f"{meta.get('tipo', '')}  ·  v{version}", size=8, color=H_INK2)
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
    """Pie institucional de la portada completa (la sección de portada no tiene márgenes laterales)."""
    raiz = limpiar(parte)
    p1 = parrafo_xml(after=0, line=260, ind_left=MARGEN_LADO, ind_right=MARGEN_LADO,
                     tabs=[(PAGINA_ANCHO - MARGEN_LADO, "right")], borders={"top": (H_MINT, 12, 10)})
    run(p1, "Dirección General de Estrategia y Transformación Digital", size=9.5, bold=True, color=H_INK)
    tab_run(p1)
    run(p1, str(meta.get("fecha", "")), size=8.5, color=H_INK2, font="Source Code Pro")
    p2 = parrafo_xml(before=20, after=0, line=260, ind_left=MARGEN_LADO, ind_right=MARGEN_LADO)
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
        port = secciones[0]
        port.left_margin = port.right_margin = Cm(0)
        port.top_margin, port.bottom_margin = Cm(0), Cm(3.6)
        port.header_distance, port.footer_distance = Cm(0), Cm(1.6)
        port.footer.is_linked_to_previous = False
        pie_portada(port.footer, meta)
    elif tipo_portada == "sin-ficha":
        # La primera página lleva el encabezado de oficio en el cuerpo: sin encabezado repetido.
        cuerpo.different_first_page_header_footer = True
        limpiar(cuerpo.first_page_header).append(parrafo_xml(after=0))
        pie_normal(cuerpo.first_page_footer, meta)


# --- Portadas ----------------------------------------------------------------------

def etiqueta_portada(meta):
    tipo = meta.get("tipo", "")
    codigo = meta.get("codigo", "")
    if tipo and codigo and tipo.lower() in codigo.lower():
        return codigo
    return " · ".join(x for x in (tipo, codigo) if x)


def ficha_xml(meta, ind=0):
    """Ficha ligera: rejilla de 3 columnas con etiqueta pequeña sobre cada dato."""
    filas = [
        ("Código", meta.get("codigo", "")),
        ("Versión", str(meta.get("version", ""))),
        ("Fecha", str(meta.get("fecha", ""))),
        ("Estatus", meta.get("estatus", "")),
        ("Área responsable", meta.get("responsable", "")),
        ("Fundamento", meta.get("fundamento", "")),
    ]
    filas = [f for f in filas if f[1]]
    ancho = COLUMNA // 3
    anchos = [ancho, ancho, COLUMNA - 2 * ancho]
    tbl = tabla_xml(anchos, ind=ind, mar=(150, 0, 190, 280), bordes={"top": (H_LINE, 6), "insideH": (H_LINE, 6)})
    for i in range(0, len(filas), 3):
        celdas = fila_xml(tbl, anchos)
        for j, tc in enumerate(celdas):
            if i + j >= len(filas):
                sub(tc, "w:p")
                continue
            etq, val = filas[i + j]
            p1 = parrafo_xml(before=0, after=50, line=240)
            run(p1, etq, size=7.5, color=H_INK2, font="Source Code Pro Medium", caps=True, spacing=12)
            tc.append(p1)
            p2 = parrafo_xml(before=0, after=0, line=264)
            if etq in ("Código", "Versión"):
                run(p2, val, size=10, color=H_INK, font="Source Code Pro")
            elif etq == "Estatus":
                run(p2, val, size=10, color=H_AMBER_INK, bold=True, fill=H_AMBER_TINT)
            else:
                run(p2, val, size=10, color=H_INK)
            tc.append(p2)
    return tbl


def portada_completa(meta, antes):
    """Franja de tinta a sangre (sección propia sin márgenes), ficha ligera y pie institucional."""
    ins = antes.addprevious
    tbl = tabla_xml([PAGINA_ANCHO], mar=(0, MARGEN_LADO, 0, MARGEN_LADO))
    (tc,) = fila_xml(tbl, [PAGINA_ANCHO], fill=H_INK)
    p = parrafo_xml(before=820, after=0, line=240, tabs=[(COLUMNA, "right")], borders={"left": (H_MINT, 48, 7)})
    run(p, "Órgano de Administración Judicial · DGETD", size=9, bold=True, color="FFFFFF")
    tab_run(p)
    run(p, "Catálogos institucionales", size=7.5, color=H_MINT2, font="Source Code Pro Medium", caps=True, spacing=14)
    tc.append(p)
    # Segunda fila de altura fija con el texto abajo: la franja mide lo mismo en todos los documentos.
    (tc,) = fila_xml(tbl, [PAGINA_ANCHO], fill=H_INK, borde_inf=(H_MINT, 48))
    tr = tc.getparent()
    tr.find(qn("w:trPr")).append(el("w:trHeight", val=7600, hRule="atLeast"))
    tc.find(qn("w:tcPr")).append(el("w:vAlign", val="bottom"))
    p = parrafo_xml(style="Etiqueta", before=600, after=160, keep_next=True)
    run(p, etiqueta_portada(meta), color=H_MINT2, size=9)
    tc.append(p)
    p = parrafo_xml(style="Title", after=260, line=245)
    run(p, meta.get("titulo", ""), color="FFFFFF", size=31)
    tc.append(p)
    if meta.get("subtitulo"):
        p = parrafo_xml(style="Subtitle", after=0, line=300)
        run(p, meta["subtitulo"], color=H_LINE, size=13)
        tc.append(p)
    tc.append(parrafo_xml(before=0, after=900, line=240))
    ins(tbl)

    p = parrafo_xml(style="Etiqueta", before=960, after=120, ind_left=MARGEN_LADO, keep_next=True)
    run(p, "Ficha del documento", color=H_INK2)
    ins(p)
    ins(ficha_xml(meta, ind=MARGEN_LADO))


def portada_breve(meta, antes):
    """Franja clara a lo ancho de la página, seguida de la ficha ligera."""
    ins = antes.addprevious
    tbl = tabla_xml([PAGINA_ANCHO], ind=-MARGEN_LADO, mar=(0, MARGEN_LADO, 0, MARGEN_LADO))
    (tc,) = fila_xml(tbl, [PAGINA_ANCHO], fill=H_MINT_TINT, borde_inf=(H_MINT, 36))
    p = parrafo_xml(style="Etiqueta", before=420, after=120, keep_next=True)
    run(p, etiqueta_portada(meta))
    tc.append(p)
    p = parrafo_xml(style="Title", after=160)
    run(p, meta.get("titulo", ""), size=28)
    tc.append(p)
    if meta.get("subtitulo"):
        p = parrafo_xml(style="Subtitle", after=0)
        run(p, meta["subtitulo"], size=12.5)
        tc.append(p)
    tc.append(parrafo_xml(before=0, after=380, line=240))
    ins(tbl)
    ins(parrafo_xml(before=0, after=120, line=240))
    ins(ficha_xml(meta))
    ins(parrafo_xml(before=0, after=120, line=240))


def portada_oficio(meta, antes):
    """Encabezado tipo oficio: membrete con barra mint, estatus, etiqueta y título."""
    ins = antes.addprevious
    barra = {"left": (H_MINT, 48, 9)}
    p = parrafo_xml(before=0, after=0, line=250, tabs=[(COLUMNA, "right")], borders=barra, ind_left=200)
    run(p, "Órgano de Administración Judicial", size=13, bold=True, color=H_INK, font="Source Serif 4")
    tab_run(p)
    if meta.get("estatus"):
        run(p, f"\u00a0{meta['estatus']}\u00a0", size=7.5, color=H_AMBER_INK, font="Source Code Pro Medium",
            caps=True, spacing=10, fill=H_AMBER_TINT)
    ins(p)
    p = parrafo_xml(before=30, after=0, line=250, borders=barra, ind_left=200)
    run(p, "Proyecto preparado por la Dirección General de Estrategia y Transformación Digital (DGETD)",
        size=9.5, color=H_INK2)
    ins(p)
    p = parrafo_xml(style="Etiqueta", before=640, after=100, keep_next=True)
    run(p, etiqueta_portada(meta))
    ins(p)
    p = parrafo_xml(style="Title", after=200, line=245)
    run(p, meta.get("titulo", ""), size=27)
    ins(p)
    if meta.get("subtitulo"):
        p = parrafo_xml(style="Subtitle")
        run(p, meta["subtitulo"])
        ins(p)
    # El primer párrafo del cuerpo (número de circular, quién emite, a quién se dirige) va en caja de datos.
    if antes.tag == qn("w:p"):
        ppr = antes.find(qn("w:pPr"))
        if ppr is None:
            ppr = el("w:pPr"); antes.insert(0, ppr)
        ps = ppr.find(qn("w:pStyle"))
        if ps is None:
            ps = el("w:pStyle"); ppr.insert(0, ps)
        ps.set(qn("w:val"), "DatosOficio")


def portada(doc, meta):
    cuerpo = doc.element.body
    primero = cuerpo[0]
    tipo = meta.get("portada")
    if tipo == "completa":
        portada_completa(meta, primero)
        # Párrafo que cierra la sección de portada (sin márgenes) y la separa del cuerpo.
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
        portada_oficio(meta, primero)
    else:
        portada_breve(meta, primero)


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
    """Etiqueta del recuadro como chip en su propia línea y aire arriba y abajo de cada grupo."""
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
        salto = el("w:r"); sub(salto, "w:br")
        r.addnext(salto)
        # Quita el espacio que separaba la etiqueta del texto.
        for t2 in salto.itersiblings():
            ts = t2.findall(qn("w:t"))
            if not ts:
                continue
            ts[0].text = (ts[0].text or "").lstrip()
            if ts[0].text:
                break


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
    portada(doc, meta)
    numero_capitulo(doc)
    recuadros(doc)
    listas(doc)
    cebra(doc)
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
