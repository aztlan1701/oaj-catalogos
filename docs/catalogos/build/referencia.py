"""Genera reference.docx: la plantilla de estilos de Word para todos los documentos de catálogos.

Uso: python3 referencia.py
Parte de la plantilla por defecto de pandoc y reemplaza su styles.xml con el sistema visual
acordado, de la misma familia que la Hoja de valor y kit.css (paleta con variantes de tinta accesibles,
Source Serif 4 / Source Sans 3 / Source Code Pro). El resultado se usa con `pandoc --reference-doc`.

Lo principal: cuerpo de 11.5 pt con interlineado 1.32; Heading 1–4 integrados (navegación y PDF
etiquetado) con H1 grande y filete, H2 en mint-ink, H4 como etiqueta mono; recuadros (Nota, Norma,
Compromiso, Pendiente, Alerta) con barra gruesa, fondo tintado y relleno interior, y su estilo de
carácter Chip* para la etiqueta; tablas con encabezado mint-tint y filetes finos; Marcador con fondo
amber-tint, borde ámbar y negritas; bloque de código en panel.
"""
import os
import shutil
import subprocess
import tempfile
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "reference.docx")

# --- Tokens -----------------------------------------------------------------
INK = "161A1D"
INK2 = "575F71"
LINE = "E6EAEF"
PANEL = "F8FAFC"
MINT = "49B6B2"
MINT2 = "78C9C6"
MINT_TINT = "E8F5F4"
MINT_INK = "2A7370"
AMBER = "D9950F"
AMBER_TINT = "FBF1DA"
AMBER_INK = "8A5D06"
CORAL = "E64A58"
CORAL_TINT = "FDECEE"
CORAL_INK = "C42F3D"
GREEN = "6BAA58"
GREEN_TINT = "EEF5EA"
GREEN_INK = "4A7A3C"
WHITE = "FFFFFF"

SERIF = "Source Serif 4"
SANS = "Source Sans 3"
MONO = "Source Code Pro"
MONO_MED = "Source Code Pro Medium"

# Cuerpo: 11.5 pt con interlineado 1.32 (Word mide el interlineado en 240avos de línea).
CUERPO = 23
INTERLINEA = 317

# Recuadros: (estilo, relleno, barra, tinta de la etiqueta). Mismo código de color que kit.css (.recuadro.*).
RECUADROS = [
    ("Nota", PANEL, INK2, INK2),
    ("Norma", MINT_TINT, MINT, MINT_INK),
    ("Compromiso", GREEN_TINT, GREEN, GREEN_INK),
    ("Pendiente", AMBER_TINT, AMBER, AMBER_INK),
    ("Alerta", CORAL_TINT, CORAL, CORAL_INK),
]


def fonts(name):
    return f'<w:rFonts w:ascii="{name}" w:hAnsi="{name}" w:eastAsia="{name}" w:cs="{name}"/>'


def pstyle(sid, name, ppr="", rpr="", based="Normal", nxt=None, extra="", custom=True):
    nxt_xml = f'<w:next w:val="{nxt}"/>' if nxt else ""
    based_xml = f'<w:basedOn w:val="{based}"/>' if based else ""
    cust = ' w:customStyle="1"' if custom else ""
    return (f'<w:style w:type="paragraph"{cust} w:styleId="{sid}"><w:name w:val="{name}"/>'
            f'{based_xml}{nxt_xml}<w:qFormat/>{extra}<w:pPr>{ppr}</w:pPr><w:rPr>{rpr}</w:rPr></w:style>')


def cstyle(sid, name, rpr):
    return (f'<w:style w:type="character" w:customStyle="1" w:styleId="{sid}"><w:name w:val="{name}"/>'
            f'<w:basedOn w:val="DefaultParagraphFont"/><w:qFormat/><w:rPr>{rpr}</w:rPr></w:style>')


def caja(fill, bar, arriba=9, abajo=9, barra=36):
    """Bordes de párrafo que dibujan una caja tintada: barra gruesa a la izquierda y relleno interior.

    Los bordes de arriba, abajo y derecha son del mismo color que el fondo; su `w:space` (en puntos)
    funciona como relleno interior. Word y LibreOffice unen párrafos seguidos con los mismos bordes en
    una sola caja.
    """
    return (f'<w:pBdr><w:top w:val="single" w:sz="4" w:space="{arriba}" w:color="{fill}"/>'
            f'<w:left w:val="single" w:sz="{barra}" w:space="11" w:color="{bar}"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="{abajo}" w:color="{fill}"/>'
            f'<w:right w:val="single" w:sz="4" w:space="11" w:color="{fill}"/></w:pBdr>'
            f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>')


def callout(sid, name, fill, bar):
    # Sangría = espacio del borde (11 pt) + grosor de la barra (4.5 pt): la caja queda alineada con la columna.
    ppr = ('<w:keepLines/>' + caja(fill, bar) +
           '<w:spacing w:before="280" w:after="280" w:line="300" w:lineRule="auto"/>'
           '<w:ind w:left="320" w:right="240"/>')
    return pstyle(sid, name, ppr, '<w:sz w:val="22"/><w:szCs w:val="22"/>', based="BodyText", nxt="BodyText")


def chip(sid, name, tinta, fondo=WHITE):
    return cstyle(sid, name, fonts(MONO_MED) + f'<w:caps/><w:color w:val="{tinta}"/><w:spacing w:val="12"/>'
                  f'<w:sz w:val="16"/><w:szCs w:val="16"/><w:shd w:val="clear" w:color="auto" w:fill="{fondo}"/>')


TITULO_RPR = fonts(SERIF) + f'<w:b/><w:bCs/><w:color w:val="{INK}"/><w:sz w:val="60"/><w:szCs w:val="60"/>'

STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults>
  <w:rPrDefault><w:rPr>{fonts(SANS)}<w:color w:val="{INK}"/><w:sz w:val="{CUERPO}"/><w:szCs w:val="{CUERPO}"/>
    <w:lang w:val="es-MX" w:eastAsia="es-MX" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>
  <w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="{INTERLINEA}" w:lineRule="auto"/></w:pPr></w:pPrDefault>
</w:docDefaults>

<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>
  <w:pPr><w:spacing w:after="160" w:line="{INTERLINEA}" w:lineRule="auto"/></w:pPr>
  <w:rPr>{fonts(SANS)}<w:color w:val="{INK}"/><w:sz w:val="{CUERPO}"/><w:szCs w:val="{CUERPO}"/><w:lang w:val="es-MX"/></w:rPr></w:style>
<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:semiHidden/>
  <w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/><w:semiHidden/></w:style>

{pstyle("BodyText", "Body Text", nxt="BodyText")}
{pstyle("FirstParagraph", "First Paragraph", based="BodyText", nxt="BodyText")}
{pstyle("Compact", "Compact", '<w:spacing w:before="20" w:after="80" w:line="300" w:lineRule="auto"/>', based="BodyText")}

{pstyle("Title", "Title", '<w:keepNext/><w:spacing w:before="0" w:after="200" w:line="250" w:lineRule="auto"/>',
        TITULO_RPR, based="Normal", nxt="Subtitle", custom=False)}
{pstyle("Subtitle", "Subtitle", '<w:keepNext/><w:spacing w:before="0" w:after="280" w:line="300" w:lineRule="auto"/>',
        f'<w:color w:val="{INK2}"/><w:sz w:val="27"/><w:szCs w:val="27"/>', based="Normal", nxt="BodyText", custom=False)}
{pstyle("Author", "Author", "", f'<w:color w:val="{INK2}"/>', nxt="BodyText")}
{pstyle("Date", "Date", "", f'<w:color w:val="{INK2}"/>', nxt="BodyText")}
{pstyle("Abstract", "Abstract", "", "", nxt="BodyText")}
{pstyle("AbstractTitle", "Abstract Title", "", "<w:b/>", nxt="Abstract")}
{pstyle("Bibliography", "Bibliography")}

{pstyle("Heading1", "heading 1",
        f'<w:keepNext/><w:keepLines/><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="9" w:color="{LINE}"/></w:pBdr>'
        '<w:spacing w:before="640" w:after="240" w:line="245" w:lineRule="auto"/><w:outlineLvl w:val="0"/>',
        fonts(SERIF) + f'<w:b/><w:bCs/><w:color w:val="{INK}"/><w:sz w:val="42"/><w:szCs w:val="42"/>', nxt="BodyText", custom=False)}
{pstyle("Heading2", "heading 2",
        '<w:keepNext/><w:keepLines/><w:spacing w:before="420" w:after="120" w:line="250" w:lineRule="auto"/><w:outlineLvl w:val="1"/>',
        fonts(SERIF) + f'<w:b/><w:bCs/><w:color w:val="{MINT_INK}"/><w:sz w:val="30"/><w:szCs w:val="30"/>', nxt="BodyText", custom=False)}
{pstyle("Heading3", "heading 3",
        '<w:keepNext/><w:keepLines/><w:spacing w:before="300" w:after="80" w:line="260" w:lineRule="auto"/><w:outlineLvl w:val="2"/>',
        f'<w:b/><w:bCs/><w:color w:val="{INK}"/><w:sz w:val="25"/><w:szCs w:val="25"/>', nxt="BodyText", custom=False)}
{pstyle("Heading4", "heading 4",
        '<w:keepNext/><w:keepLines/><w:spacing w:before="260" w:after="80" w:line="260" w:lineRule="auto"/><w:outlineLvl w:val="3"/>',
        fonts(MONO_MED) + f'<w:caps/><w:color w:val="{MINT_INK}"/><w:spacing w:val="14"/><w:sz w:val="18"/><w:szCs w:val="18"/>', nxt="BodyText", custom=False)}
{pstyle("Heading5", "heading 5", '<w:keepNext/><w:spacing w:before="200" w:after="60"/><w:outlineLvl w:val="4"/>', "<w:b/>", nxt="BodyText", custom=False)}
{pstyle("Heading6", "heading 6", '<w:keepNext/><w:spacing w:before="200" w:after="60"/><w:outlineLvl w:val="5"/>', "<w:i/>", nxt="BodyText", custom=False)}

{pstyle("BlockText", "Block Text",
        caja(PANEL, MINT) + '<w:spacing w:before="200" w:after="200"/><w:ind w:left="320" w:right="240"/>', "", based="BodyText", nxt="BodyText")}
{pstyle("SourceCode", "Source Code",
        f'<w:pBdr><w:top w:val="single" w:sz="4" w:space="8" w:color="{PANEL}"/>'
        f'<w:left w:val="single" w:sz="18" w:space="10" w:color="{LINE}"/><w:bottom w:val="single" w:sz="4" w:space="8" w:color="{PANEL}"/>'
        f'<w:right w:val="single" w:sz="4" w:space="10" w:color="{PANEL}"/></w:pBdr><w:shd w:val="clear" w:color="auto" w:fill="{PANEL}"/>'
        '<w:spacing w:before="240" w:after="240" w:line="252" w:lineRule="auto"/><w:ind w:left="240" w:right="220"/>',
        fonts(MONO) + f'<w:color w:val="{INK}"/><w:sz w:val="17"/><w:szCs w:val="17"/>', based="Normal", nxt="BodyText")}
{pstyle("FootnoteText", "footnote text", '<w:spacing w:after="40" w:line="240" w:lineRule="auto"/>', f'<w:color w:val="{INK2}"/><w:sz w:val="18"/><w:szCs w:val="18"/>')}
{pstyle("DefinitionTerm", "Definition Term", '<w:keepNext/><w:spacing w:before="160" w:after="0"/>', "<w:b/>", nxt="Definition")}
{pstyle("Definition", "Definition", '<w:ind w:left="284"/>', "")}
{pstyle("Caption", "caption", '<w:spacing w:before="80" w:after="200"/>', f'<w:color w:val="{INK2}"/><w:sz w:val="19"/><w:szCs w:val="19"/>')}
{pstyle("TableCaption", "Table Caption",
        f'<w:keepNext/><w:pBdr><w:left w:val="single" w:sz="18" w:space="6" w:color="{MINT}"/></w:pBdr>'
        '<w:spacing w:before="300" w:after="120" w:line="260" w:lineRule="auto"/><w:ind w:left="160"/>',
        f'<w:b/><w:bCs/><w:color w:val="{INK2}"/><w:sz w:val="20"/><w:szCs w:val="20"/>', based="Caption")}
{pstyle("ImageCaption", "Image Caption", "", "", based="Caption")}
{pstyle("Figure", "Figure", '<w:jc w:val="center"/><w:spacing w:before="160" w:after="80"/>', "")}
{pstyle("CaptionedFigure", "Captioned Figure", '<w:keepNext/>', "", based="Figure")}
{pstyle("TOCHeading", "TOC Heading", "", "", based="Heading1", nxt="BodyText")}

{"".join(callout(sid, sid, fill, bar) for sid, fill, bar, _ in RECUADROS)}
{pstyle("Etiqueta", "Etiqueta", '<w:keepNext/><w:spacing w:before="240" w:after="60"/>',
        fonts(MONO_MED) + f'<w:caps/><w:color w:val="{MINT_INK}"/><w:spacing w:val="14"/><w:sz w:val="17"/><w:szCs w:val="17"/>', based="Normal", nxt="BodyText")}
{pstyle("Firma", "Firma", '<w:keepLines/><w:spacing w:before="560" w:after="0"/>', "", based="BodyText")}
{pstyle("Pequeno", "Pequeno", '<w:spacing w:before="0" w:after="80" w:line="264" w:lineRule="auto"/>', f'<w:color w:val="{INK2}"/><w:sz w:val="19"/><w:szCs w:val="19"/>', based="BodyText")}
{pstyle("DatosOficio", "Datos de oficio",
        caja(PANEL, MINT, arriba=8, abajo=8, barra=24) + '<w:spacing w:before="120" w:after="320" w:line="300" w:lineRule="auto"/><w:ind w:left="300" w:right="240"/>',
        '<w:sz w:val="21"/><w:szCs w:val="21"/>', based="BodyText", nxt="BodyText")}

<w:style w:type="character" w:customStyle="1" w:styleId="BodyTextChar"><w:name w:val="Body Text Char"/><w:basedOn w:val="DefaultParagraphFont"/></w:style>
<w:style w:type="character" w:customStyle="1" w:styleId="VerbatimChar"><w:name w:val="Verbatim Char"/><w:basedOn w:val="DefaultParagraphFont"/>
  <w:rPr>{fonts(MONO)}<w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr></w:style>
{cstyle("Clave", "Clave", fonts(MONO) + f'<w:color w:val="{INK}"/><w:sz w:val="19"/><w:szCs w:val="19"/>')}
{cstyle("Marcador", "Marcador", f'<w:b/><w:color w:val="{AMBER_INK}"/><w:bdr w:val="single" w:sz="4" w:space="0" w:color="{AMBER}"/><w:shd w:val="clear" w:color="auto" w:fill="{AMBER_TINT}"/>')}
{cstyle("Obligatorio", "Obligatorio", f'<w:b/><w:color w:val="{CORAL_INK}"/>')}
{cstyle("Dgetd", "Dgetd", f'<w:b/><w:color w:val="{MINT_INK}"/>')}
{cstyle("NumeroCapitulo", "Numero de capitulo", f'<w:color w:val="{MINT_INK}"/>')}
{"".join(chip("Chip" + sid, "Etiqueta de " + sid, tinta) for sid, _, _, tinta in RECUADROS)}
<w:style w:type="character" w:customStyle="1" w:styleId="SectionNumber"><w:name w:val="Section Number"/><w:basedOn w:val="DefaultParagraphFont"/></w:style>
<w:style w:type="character" w:styleId="FootnoteReference"><w:name w:val="footnote reference"/><w:basedOn w:val="DefaultParagraphFont"/><w:rPr><w:vertAlign w:val="superscript"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:basedOn w:val="DefaultParagraphFont"/><w:rPr><w:color w:val="{MINT_INK}"/><w:u w:val="single"/></w:rPr></w:style>

<w:style w:type="table" w:customStyle="1" w:styleId="Table"><w:name w:val="Table"/><w:basedOn w:val="TableNormal"/><w:qFormat/>
  <w:pPr><w:spacing w:before="0" w:after="40" w:line="264" w:lineRule="auto"/></w:pPr>
  <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  <w:tblPr><w:tblInd w:w="0" w:type="dxa"/>
    <w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="{LINE}"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="{LINE}"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{LINE}"/></w:tblBorders>
    <w:tblCellMar><w:top w:w="110" w:type="dxa"/><w:left w:w="130" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:right w:w="130" w:type="dxa"/></w:tblCellMar></w:tblPr>
  <w:tblStylePr w:type="firstRow"><w:pPr><w:keepNext/></w:pPr><w:rPr><w:b/><w:bCs/><w:color w:val="{INK}"/></w:rPr>
    <w:tblPr/><w:trPr><w:tblHeader/></w:trPr>
    <w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{MINT_TINT}"/><w:tcBorders><w:top w:val="nil"/><w:bottom w:val="single" w:sz="12" w:space="0" w:color="{MINT}"/></w:tcBorders></w:tcPr></w:tblStylePr>
  <w:tblStylePr w:type="band2Horz"><w:tblPr/><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{PANEL}"/></w:tcPr></w:tblStylePr>
</w:style>
</w:styles>'''


def main():
    tmp = tempfile.mkdtemp()
    base = os.path.join(tmp, "base.docx")
    with open(base, "wb") as fh:
        fh.write(subprocess.check_output(["pandoc", "--print-default-data-file", "reference.docx"]))
    with zipfile.ZipFile(base) as zin, zipfile.ZipFile(SALIDA, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename.endswith("/"):
                continue
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                data = STYLES.encode("utf-8")
            zout.writestr(item, data)
    shutil.rmtree(tmp)
    print("reference.docx listo:", SALIDA)


if __name__ == "__main__":
    main()
