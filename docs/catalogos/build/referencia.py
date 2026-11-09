"""Genera reference.docx: la plantilla de estilos de Word para todos los documentos de catálogos.

Uso: python3 referencia.py
Parte de la plantilla por defecto de pandoc y reemplaza su styles.xml con el sistema visual
acordado (paleta del rediseño con variantes de tinta accesibles, Source Serif 4 / Source Sans 3 /
Source Code Pro). El resultado se usa con `pandoc --reference-doc`.
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
MINT_TINT = "E8F5F4"
MINT_INK = "2A7370"
AMBER = "D9950F"
AMBER_TINT = "FBF1DA"
AMBER_INK = "8A5D06"
CORAL = "E64A58"
CORAL_TINT = "FDECEE"
CORAL_INK = "C42F3D"

SERIF = "Source Serif 4"
SANS = "Source Sans 3"
MONO = "Source Code Pro"


def fonts(name):
    return f'<w:rFonts w:ascii="{name}" w:hAnsi="{name}" w:eastAsia="{name}" w:cs="{name}"/>'


def pstyle(sid, name, ppr="", rpr="", based="Normal", nxt=None, extra=""):
    nxt_xml = f'<w:next w:val="{nxt}"/>' if nxt else ""
    based_xml = f'<w:basedOn w:val="{based}"/>' if based else ""
    return (f'<w:style w:type="paragraph" w:customStyle="1" w:styleId="{sid}"><w:name w:val="{name}"/>'
            f'{based_xml}{nxt_xml}<w:qFormat/>{extra}<w:pPr>{ppr}</w:pPr><w:rPr>{rpr}</w:rPr></w:style>')


def callout(sid, name, fill, bar):
    ppr = (f'<w:pBdr><w:left w:val="single" w:sz="24" w:space="8" w:color="{bar}"/></w:pBdr>'
           f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
           '<w:spacing w:before="160" w:after="160" w:line="288" w:lineRule="auto"/>'
           '<w:ind w:left="227" w:right="113"/>')
    return pstyle(sid, name, ppr, "", based="BodyText", nxt="BodyText")


STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults>
  <w:rPrDefault><w:rPr>{fonts(SANS)}<w:color w:val="{INK}"/><w:sz w:val="24"/><w:szCs w:val="24"/>
    <w:lang w:val="es-MX" w:eastAsia="es-MX" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>
  <w:pPrDefault><w:pPr><w:spacing w:after="140" w:line="300" w:lineRule="auto"/></w:pPr></w:pPrDefault>
</w:docDefaults>

<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>
  <w:pPr><w:spacing w:after="140" w:line="300" w:lineRule="auto"/></w:pPr>
  <w:rPr>{fonts(SANS)}<w:color w:val="{INK}"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="es-MX"/></w:rPr></w:style>
<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:semiHidden/>
  <w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>

{pstyle("BodyText", "Body Text", nxt="BodyText")}
{pstyle("FirstParagraph", "First Paragraph", based="BodyText", nxt="BodyText")}
{pstyle("Compact", "Compact", '<w:spacing w:before="20" w:after="40" w:line="264" w:lineRule="auto"/>', based="BodyText")}

{pstyle("Title", "Title", '<w:keepNext/><w:spacing w:before="0" w:after="160" w:line="240" w:lineRule="auto"/>',
        fonts(SERIF) + f'<w:b/><w:bCs/><w:color w:val="{INK}"/><w:sz w:val="52"/><w:szCs w:val="52"/>', based="Normal", nxt="BodyText")}
{pstyle("Subtitle", "Subtitle", '<w:spacing w:before="0" w:after="240" w:line="276" w:lineRule="auto"/>',
        f'<w:color w:val="{INK2}"/><w:sz w:val="28"/><w:szCs w:val="28"/>', based="Normal", nxt="BodyText")}
{pstyle("Author", "Author", "", f'<w:color w:val="{INK2}"/>', nxt="BodyText")}
{pstyle("Date", "Date", "", f'<w:color w:val="{INK2}"/>', nxt="BodyText")}
{pstyle("Abstract", "Abstract", "", "", nxt="BodyText")}
{pstyle("AbstractTitle", "Abstract Title", "", "<w:b/>", nxt="Abstract")}
{pstyle("Bibliography", "Bibliography")}

{pstyle("Heading1", "heading 1",
        f'<w:keepNext/><w:keepLines/><w:pBdr><w:bottom w:val="single" w:sz="8" w:space="6" w:color="{MINT}"/></w:pBdr>'
        '<w:spacing w:before="480" w:after="200" w:line="240" w:lineRule="auto"/><w:outlineLvl w:val="0"/>',
        fonts(SERIF) + f'<w:b/><w:bCs/><w:color w:val="{INK}"/><w:sz w:val="34"/><w:szCs w:val="34"/>', nxt="BodyText")}
{pstyle("Heading2", "heading 2",
        '<w:keepNext/><w:keepLines/><w:spacing w:before="320" w:after="100" w:line="240" w:lineRule="auto"/><w:outlineLvl w:val="1"/>',
        fonts(SERIF) + f'<w:b/><w:bCs/><w:color w:val="{MINT_INK}"/><w:sz w:val="27"/><w:szCs w:val="27"/>', nxt="BodyText")}
{pstyle("Heading3", "heading 3",
        '<w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="80" w:line="240" w:lineRule="auto"/><w:outlineLvl w:val="2"/>',
        f'<w:b/><w:bCs/><w:color w:val="{INK}"/><w:sz w:val="24"/><w:szCs w:val="24"/>', nxt="BodyText")}
{pstyle("Heading4", "heading 4",
        '<w:keepNext/><w:spacing w:before="200" w:after="60" w:line="240" w:lineRule="auto"/><w:outlineLvl w:val="3"/>',
        f'<w:b/><w:bCs/><w:caps/><w:color w:val="{INK2}"/><w:spacing w:val="10"/><w:sz w:val="19"/><w:szCs w:val="19"/>', nxt="BodyText")}
{pstyle("Heading5", "heading 5", '<w:keepNext/><w:spacing w:before="160" w:after="40"/><w:outlineLvl w:val="4"/>', "<w:b/>", nxt="BodyText")}
{pstyle("Heading6", "heading 6", '<w:keepNext/><w:spacing w:before="160" w:after="40"/><w:outlineLvl w:val="5"/>', "<w:i/>", nxt="BodyText")}

{pstyle("BlockText", "Block Text",
        f'<w:pBdr><w:left w:val="single" w:sz="24" w:space="8" w:color="{MINT}"/></w:pBdr><w:shd w:val="clear" w:color="auto" w:fill="{PANEL}"/>'
        '<w:spacing w:before="60" w:after="60"/><w:ind w:left="227" w:right="113"/>', "", based="BodyText", nxt="BodyText")}
{pstyle("FootnoteText", "footnote text", '<w:spacing w:after="40" w:line="240" w:lineRule="auto"/>', f'<w:color w:val="{INK2}"/><w:sz w:val="18"/><w:szCs w:val="18"/>')}
{pstyle("DefinitionTerm", "Definition Term", '<w:keepNext/><w:spacing w:before="120" w:after="0"/>', "<w:b/>", nxt="Definition")}
{pstyle("Definition", "Definition", '<w:ind w:left="284"/>', "")}
{pstyle("Caption", "caption", '<w:spacing w:before="60" w:after="160"/>', f'<w:color w:val="{INK2}"/><w:sz w:val="19"/><w:szCs w:val="19"/>')}
{pstyle("TableCaption", "Table Caption", '<w:keepNext/><w:spacing w:before="200" w:after="80"/>', fonts(SERIF) + f'<w:b/><w:color w:val="{INK}"/><w:sz w:val="21"/><w:szCs w:val="21"/>', based="Caption")}
{pstyle("ImageCaption", "Image Caption", "", "", based="Caption")}
{pstyle("Figure", "Figure", '<w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/>', "")}
{pstyle("CaptionedFigure", "Captioned Figure", '<w:keepNext/>', "", based="Figure")}
{pstyle("TOCHeading", "TOC Heading", "", "", based="Heading1", nxt="BodyText")}

{callout("Nota", "Nota", PANEL, INK2)}
{callout("Norma", "Norma", PANEL, LINE)}
{callout("Compromiso", "Compromiso", MINT_TINT, MINT)}
{callout("Pendiente", "Pendiente", AMBER_TINT, AMBER)}
{callout("Alerta", "Alerta", CORAL_TINT, CORAL)}
{pstyle("Etiqueta", "Etiqueta", '<w:keepNext/><w:spacing w:before="200" w:after="40"/>',
        fonts(MONO) + f'<w:caps/><w:color w:val="{MINT_INK}"/><w:spacing w:val="12"/><w:sz w:val="17"/><w:szCs w:val="17"/>', based="Normal", nxt="BodyText")}
{pstyle("Firma", "Firma", '<w:keepLines/><w:spacing w:before="480" w:after="0"/>', "", based="BodyText")}
{pstyle("Pequeno", "Pequeno", '<w:spacing w:before="0" w:after="80" w:line="252" w:lineRule="auto"/>', f'<w:color w:val="{INK2}"/><w:sz w:val="19"/><w:szCs w:val="19"/>', based="BodyText")}

<w:style w:type="character" w:customStyle="1" w:styleId="BodyTextChar"><w:name w:val="Body Text Char"/><w:basedOn w:val="DefaultParagraphFont"/></w:style>
<w:style w:type="character" w:customStyle="1" w:styleId="VerbatimChar"><w:name w:val="Verbatim Char"/><w:basedOn w:val="DefaultParagraphFont"/>
  <w:rPr>{fonts(MONO)}<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
<w:style w:type="character" w:customStyle="1" w:styleId="Clave"><w:name w:val="Clave"/><w:basedOn w:val="DefaultParagraphFont"/><w:qFormat/>
  <w:rPr>{fonts(MONO)}<w:color w:val="{INK}"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
<w:style w:type="character" w:customStyle="1" w:styleId="Marcador"><w:name w:val="Marcador"/><w:basedOn w:val="DefaultParagraphFont"/><w:qFormat/>
  <w:rPr><w:b/><w:color w:val="{AMBER_INK}"/><w:shd w:val="clear" w:color="auto" w:fill="{AMBER_TINT}"/></w:rPr></w:style>
<w:style w:type="character" w:customStyle="1" w:styleId="Obligatorio"><w:name w:val="Obligatorio"/><w:basedOn w:val="DefaultParagraphFont"/><w:qFormat/>
  <w:rPr><w:b/><w:color w:val="{CORAL_INK}"/></w:rPr></w:style>
<w:style w:type="character" w:customStyle="1" w:styleId="Dgetd"><w:name w:val="Dgetd"/><w:basedOn w:val="DefaultParagraphFont"/><w:qFormat/>
  <w:rPr><w:b/><w:color w:val="{MINT_INK}"/></w:rPr></w:style>
<w:style w:type="character" w:customStyle="1" w:styleId="SectionNumber"><w:name w:val="Section Number"/><w:basedOn w:val="DefaultParagraphFont"/></w:style>
<w:style w:type="character" w:styleId="FootnoteReference"><w:name w:val="footnote reference"/><w:basedOn w:val="DefaultParagraphFont"/><w:rPr><w:vertAlign w:val="superscript"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:basedOn w:val="DefaultParagraphFont"/><w:rPr><w:color w:val="{MINT_INK}"/><w:u w:val="single"/></w:rPr></w:style>

<w:style w:type="table" w:customStyle="1" w:styleId="Table"><w:name w:val="Table"/><w:basedOn w:val="TableNormal"/><w:qFormat/>
  <w:pPr><w:spacing w:before="40" w:after="40" w:line="252" w:lineRule="auto"/></w:pPr>
  <w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  <w:tblPr><w:tblInd w:w="0" w:type="dxa"/>
    <w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="{LINE}"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="{LINE}"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{LINE}"/></w:tblBorders>
    <w:tblCellMar><w:top w:w="72" w:type="dxa"/><w:left w:w="113" w:type="dxa"/><w:bottom w:w="72" w:type="dxa"/><w:right w:w="113" w:type="dxa"/></w:tblCellMar></w:tblPr>
  <w:tblStylePr w:type="firstRow"><w:pPr><w:keepNext/></w:pPr><w:rPr><w:b/><w:bCs/><w:color w:val="{INK}"/></w:rPr>
    <w:tblPr/><w:trPr><w:tblHeader/></w:trPr>
    <w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{MINT_TINT}"/><w:tcBorders><w:bottom w:val="single" w:sz="8" w:space="0" w:color="{MINT}"/></w:tcBorders></w:tcPr></w:tblStylePr>
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
