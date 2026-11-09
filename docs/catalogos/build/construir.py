"""Convierte una fuente Markdown (con front matter YAML) en un .docx con el sistema visual de catálogos.

Uso:
    python3 construir.py ../fuentes/PR-CAT-04.md            # escribe ../entregables/PR-CAT-04.docx
    python3 construir.py ../fuentes/PR-CAT-04.md --pdf      # además, vista previa PDF en ../vista-previa/

Front matter reconocido:
    codigo, titulo, subtitulo, tipo, version, fecha, estatus, responsable, fundamento,
    portada: completa | breve | sin-ficha   (completa = salto de página; sin-ficha = sin tabla de datos)

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
import sys
import tempfile
import uuid
import zipfile

import yaml
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
REFERENCIA = os.path.join(AQUI, "reference.docx")
FUENTES_TTF = os.path.join(AQUI, "fuentes-tipograficas")

INK2 = RGBColor(0x57, 0x5F, 0x71)
MINT_INK = RGBColor(0x2A, 0x73, 0x70)

# (familia en Word, tipo de incrustación, archivo)
EMBEBIDAS = [
    ("Source Sans 3", "embedRegular", "SourceSans3-Regular.ttf"),
    ("Source Sans 3", "embedBold", "SourceSans3-Bold.ttf"),
    ("Source Sans 3", "embedItalic", "SourceSans3-It.ttf"),
    ("Source Serif 4", "embedBold", "SourceSerif4-Bold.ttf"),
    ("Source Code Pro", "embedRegular", "SourceCodePro-Regular.ttf"),
]


def leer_front_matter(ruta):
    with open(ruta, encoding="utf-8") as fh:
        texto = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    meta = yaml.safe_load(m.group(1)) if m else {}
    return meta or {}


def campo(fld_text, run_parent):
    """Inserta un campo de Word (PAGE, NUMPAGES) en un párrafo."""
    r1 = OxmlElement("w:r"); fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), "begin"); r1.append(fc)
    r2 = OxmlElement("w:r"); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = f" {fld_text} "; r2.append(it)
    r3 = OxmlElement("w:r"); fc3 = OxmlElement("w:fldChar"); fc3.set(qn("w:fldCharType"), "separate"); r3.append(fc3)
    r4 = OxmlElement("w:r"); t = OxmlElement("w:t"); t.text = "1"; r4.append(t)
    r5 = OxmlElement("w:r"); fc5 = OxmlElement("w:fldChar"); fc5.set(qn("w:fldCharType"), "end"); r5.append(fc5)
    for r in (r1, r2, r3, r4, r5):
        rpr = OxmlElement("w:rPr"); sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "17"); rpr.append(sz)
        col = OxmlElement("w:color"); col.set(qn("w:val"), "575F71"); rpr.append(col)
        r.insert(0, rpr)
        run_parent._p.append(r)


def estilo_run(run, size=8.5, color=INK2, bold=False, mono=False):
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    if mono:
        run.font.name = "Source Code Pro"
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "Source Code Pro")


def tab_derecha(paragraph, section):
    ancho = section.page_width - section.left_margin - section.right_margin
    paragraph.paragraph_format.tab_stops.add_tab_stop(ancho, WD_TAB_ALIGNMENT.RIGHT)


def borde_inferior(paragraph, color="E6EAEF", sz="4"):
    ppr = paragraph._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", sz), ("w:space", "6"), ("w:color", color)):
        b.set(qn(k), v)
    bdr.append(b); ppr.append(bdr)


def borde_superior(paragraph, color="E6EAEF", sz="4"):
    ppr = paragraph._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr"); b = OxmlElement("w:top")
    for k, v in (("w:val", "single"), ("w:sz", sz), ("w:space", "6"), ("w:color", color)):
        b.set(qn(k), v)
    bdr.append(b); ppr.append(bdr)


def preparar_secciones(doc, meta):
    estatus = meta.get("estatus", "Borrador para revisión")
    codigo = meta.get("codigo", "")
    version = meta.get("version", "")
    for s in doc.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.left_margin = s.right_margin = Cm(2.4)
        s.top_margin, s.bottom_margin = Cm(2.4), Cm(2.2)
        s.header_distance, s.footer_distance = Cm(1.1), Cm(1.0)

        h = s.header.paragraphs[0] if s.header.paragraphs else s.header.add_paragraph()
        h.text = ""
        h.paragraph_format.space_after = Pt(0)
        tab_derecha(h, s)
        estilo_run(h.add_run("Órgano de Administración Judicial · DGETD"), bold=True, color=RGBColor(0x16, 0x1A, 0x1D))
        estilo_run(h.add_run("\t"))
        estilo_run(h.add_run(f"{codigo}  ·  v{version}" if codigo else f"v{version}"), mono=True)
        borde_inferior(h)

        f = s.footer.paragraphs[0] if s.footer.paragraphs else s.footer.add_paragraph()
        f.text = ""
        f.paragraph_format.space_after = Pt(0)
        tab_derecha(f, s)
        borde_superior(f)
        estilo_run(f.add_run(estatus))
        estilo_run(f.add_run("\tPágina "))
        campo("PAGE", f)
        estilo_run(f.add_run(" de "))
        campo("NUMPAGES", f)


def portada(doc, meta):
    cuerpo = doc.element.body
    primero = cuerpo[0]

    def parrafo(texto, estilo):
        p = doc.add_paragraph(texto, style=estilo)
        primero.addprevious(p._p)
        return p

    tipo = meta.get("tipo", "")
    codigo = meta.get("codigo", "")
    etiqueta = " · ".join(x for x in (tipo, codigo) if x)
    if etiqueta:
        parrafo(etiqueta, "Etiqueta")
    parrafo(meta.get("titulo", ""), "Title")
    if meta.get("subtitulo"):
        parrafo(meta["subtitulo"], "Subtitle")

    filas = [
        ("Código", codigo),
        ("Versión", str(meta.get("version", ""))),
        ("Fecha", str(meta.get("fecha", ""))),
        ("Estatus", meta.get("estatus", "")),
        ("Área responsable", meta.get("responsable", "")),
        ("Fundamento", meta.get("fundamento", "")),
    ]
    filas = [f for f in filas if f[1]]
    if filas and meta.get("portada") != "sin-ficha":
        t = doc.add_table(rows=0, cols=2)
        t.style = [st for st in doc.styles if st.style_id == "Table"][0]
        t.autofit = False
        tblPr = t._tbl.tblPr
        look = OxmlElement("w:tblLook"); look.set(qn("w:val"), "0000"); look.set(qn("w:firstRow"), "0"); tblPr.append(look)
        for etq, val in filas:
            celdas = t.add_row().cells
            celdas[0].width, celdas[1].width = Cm(4.2), Cm(12.0)
            for c in celdas:
                c.paragraphs[0].paragraph_format.space_after = Pt(0)
                c.paragraphs[0].paragraph_format.space_before = Pt(0)
                c.paragraphs[0].paragraph_format.line_spacing = 1.1
            p0 = celdas[0].paragraphs[0]; r0 = p0.add_run(etq)
            r0.font.size = Pt(9.5); r0.font.color.rgb = INK2; r0.font.bold = True
            p1 = celdas[1].paragraphs[0]; r1 = p1.add_run(val); r1.font.size = Pt(10)
            if etq in ("Código", "Versión"):
                r1.font.name = "Source Code Pro"
        grid = t._tbl.tblGrid
        for gc, w in zip(grid.findall(qn("w:gridCol")), (2381, 6804)):
            gc.set(qn("w:w"), str(w))
        tblW = tblPr.find(qn("w:tblW"))
        if tblW is None:
            tblW = OxmlElement("w:tblW"); tblPr.append(tblW)
        tblW.set(qn("w:w"), "9185"); tblW.set(qn("w:type"), "dxa")
        primero.addprevious(t._tbl)
        sep = doc.add_paragraph("", style="BodyText")
        sep.paragraph_format.space_after = Pt(6)
        primero.addprevious(sep._p)

    if meta.get("portada") == "completa":
        p = doc.add_paragraph("", style="BodyText")
        p.add_run().add_break(__import__("docx").enum.text.WD_BREAK.PAGE)
        primero.addprevious(p._p)


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
