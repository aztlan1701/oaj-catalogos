"""Genera la plantilla de Excel de F-CAT-01 (registro masivo de catálogos existentes).

Uso:
    python3 plantilla_excel.py        # escribe ../entregables/F-CAT-01-plantilla-masiva.xlsx

Lee ../spec/registro.yaml (fuente de verdad) y arma un libro con estas hojas, en este orden:
    Cómo llenar   instrucciones breves, una idea por renglón
    Mis listas    un renglón por lista; columnas = campos de las secciones A a F (tabla tblMisListas)
    Ejemplo       2 renglones ilustrativos con la misma estructura (tabla tblEjemplo)
    Áreas         lista oficial de áreas y órganos que carga la DGETD (tabla tblAreas)
    Valores       oculta; valores permitidos que alimentan las listas desplegables

Los subcampos de persona y las casillas siguen la sección 5.5 de ET-CAT-01. Si cambia
registro.yaml, se vuelve a ejecutar este script.
"""
import os
import re

import yaml
from openpyxl import Workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter, quote_sheetname
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.pagebreak import Break
from openpyxl.worksheet.table import Table, TableStyleInfo

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SPEC = os.path.join(RAIZ, "spec", "registro.yaml")
SALIDA = os.path.join(RAIZ, "entregables", "F-CAT-01-plantilla-masiva.xlsx")

# Paleta del paquete (build/referencia.py)
INK = "161A1D"
INK2 = "575F71"
LINE = "E6EAEF"
PANEL = "F8FAFC"
MINT = "49B6B2"
MINT_TINT = "E8F5F4"
MINT_INK = "2A7370"
AMBER_TINT = "FBF1DA"
AMBER_INK = "8A5D06"

FUENTE = "Calibri"
FILAS_CAPTURA = 200
ESCALA_CAPTURA = 70      # escala de impresión de «Mis listas» y «Ejemplo» (31 columnas)

# En «Cómo llenar», secciones que empiezan en hoja nueva al imprimir (para no partirlas).
SALTO_ANTES = ("Cómo entregarla",)

# Hojas
H_COMO = "Cómo llenar"
H_MIS = "Mis listas"
H_EJ = "Ejemplo"
H_AREAS = "Áreas"
H_VAL = "Valores"

AREAS_PRIMERA = 5        # primer renglón de datos en la hoja Áreas
AREAS_MAX = 2000         # renglones de Áreas que cubren las listas desplegables

# Valores de sí o no para las casillas (tipo «Sí o no», ET-CAT-01 sección 5.2)
CASILLA = ["Sí", "No"]

# Subcampos de persona (ET-CAT-01, tabla 5.5). La pregunta de cada subcampo completa la de registro.yaml.
SUBCAMPOS = {
    "A2": [
        ("nombre completo", "Escriba su nombre completo."),
        ("puesto", "Puesto de la persona enlace."),
        ("correo institucional", "Correo institucional de la persona enlace."),
        ("extensión", "Extensión telefónica de la persona enlace."),
    ],
    "A3": [
        ("nombre completo", "Escriba el nombre completo de la persona titular."),
        ("puesto", "Puesto de la persona titular."),
    ],
}

# Columnas complementarias que piden las propias preguntas o casillas de registro.yaml
COMPLEMENTOS = {
    "C2": [("persona de contacto", "Persona de contacto del área que mantiene la lista.",
            "Indique nombre, puesto, correo institucional y extensión de una persona del área que mantiene la lista.",
            "texto", 30)],
    "D2": [("qué lo dispara", "Si eligió «Cada vez que ocurre un cambio», ¿qué hecho dispara el cambio?",
            "Por ejemplo: cuando se crea o se readscribe un órgano. Déjela vacía si eligió otra frecuencia.",
            "texto", 30)],
    "D3": [("versión actual", "Si respondió «Sí», ¿cuál es la versión actual?",
            "Escriba la versión como la usan hoy, por ejemplo v2.3. Déjela vacía si respondió «No».",
            "texto", 18)],
}

# Anchos por campo (en caracteres de Excel)
ANCHOS = {
    "A1": 36, "B1": 18, "B1b": 18, "B2": 34, "B3": 50, "C1": 34, "C2": 34, "C2b": 22, "C3": 24,
    "D1": 44, "D2": 26, "D3": 22, "D4": 20, "E1": 20, "E2": 20,
    "F1": 30, "F2": 18, "F3": 38, "F4": 30, "F5": 44,
}
ANCHO_SUB = {"nombre completo": 28, "puesto": 28, "correo institucional": 30, "extensión": 16}
ANCHO_CASILLA = 20

# Propietario y custodio son áreas administrativas (LGCI art. 4 fr. XVII y VI). Sus listas desplegables
# ofrecen «Por confirmar» y solo las áreas de la hoja «Áreas» cuyo tipo es TIPO_ADMIN.
TIPO_ADMIN = "Área administrativa"
TIPO_OJ = "Órgano jurisdiccional"
SOLO_ADMIN = {"C1": "art. 4 fr. XVII", "C2": "art. 4 fr. VI"}

# Ayuda de Excel que sustituye a la de registro.yaml (máximo 255 caracteres en el recuadro de Excel).
# C1: la plantilla solo marca el área que registra cuando es un área administrativa (art. 4 fr. XVII).
# Pendiente: pasar este texto a registro.yaml > C1 > ayuda para que los tres canales digan lo mismo.
AYUDA_EXCEL = {
    "C1": ("Es el área administrativa que decide sobre el contenido. Si registra un área administrativa, "
           "viene marcada; cámbiela si decide otra. Si registra un órgano jurisdiccional, viene "
           "«Por confirmar»: elija el área competente (art. 4 fr. XVII)."),
}

# Marcadores que usa la plantilla y que todavía no están en registro.yaml > marcadores.
# Si registro.yaml los da de alta con la misma clave, manda el valor de registro.yaml.
MARCADORES_EXTRA = {
    "aviso_privacidad": "[liga al aviso de privacidad simplificado, por definir con la unidad de transparencia]",
}

FORMATO_FECHA_MES = " Escriba año y mes así: 2026-09 (formato AAAA-MM)."

# Campo obligatorio que acepta «por confirmar» pero cuya lista de registro.yaml no trae ese valor (hoy, D3).
# La celda se deja vacía y se registra «Por confirmar» (ET-CAT-01, sección 5.1, regla 5).
SUFIJO_PC_VACIA = "(obligatorio; si no lo sabe, déjela vacía)"
AYUDA_PC_VACIA = " Si no lo sabe, deje la celda vacía: se registra «Por confirmar»."


# -----------------------------------------------------------------------------
# Utilidades
# -----------------------------------------------------------------------------
def font(size=11, bold=False, color=INK, italic=False):
    return Font(name=FUENTE, size=size, bold=bold, italic=italic, color=color)


def relleno(color):
    return PatternFill(fill_type="solid", start_color=color, end_color=color)


def recortar(texto, limite):
    """Recorta en la última oración completa que quepa; si no hay, en la última palabra, con «…»."""
    texto = " ".join(str(texto).split())
    if len(texto) <= limite:
        return texto
    corte = texto[:limite]
    fin = max(corte.rfind(". "), corte.rfind(".» "))
    if fin >= limite // 2:
        return corte[:fin + 1].rstrip()
    return corte[:corte.rfind(" ")].rstrip(" ,;:") + "…"


def lineas(texto, ancho, size=11, negrita=False):
    """Estima cuántas líneas ocupa un texto con ajuste en una columna de cierto ancho (Calibri)."""
    por_linea = max(1.0, ancho * (11.0 / size) * (1.05 if negrita else 1.2))
    total = 0
    for parte in str(texto).split("\n"):
        total += max(1, -(-len(parte) // int(por_linea)))
    return total


def rico(partes, base_size=11, base_bold=False, base_color=INK):
    """partes: lista de (texto, es_marcador). Los marcadores van en negritas y ámbar de tinta."""
    bloques = []
    for texto, marcador in partes:
        if marcador:
            f = InlineFont(rFont=FUENTE, sz=base_size, b=True, color=AMBER_INK)
        else:
            f = InlineFont(rFont=FUENTE, sz=base_size, b=base_bold, color=base_color)
        bloques.append(TextBlock(f, texto))
    return CellRichText(bloques)


def marcadores_de(spec):
    """Marcadores de registro.yaml más los de MARCADORES_EXTRA que registro.yaml todavía no tiene."""
    return {**MARCADORES_EXTRA, **spec["marcadores"]}


def partir_marcadores(texto, marcadores):
    """Separa un texto en partes normales y marcadores (valores de registro.yaml > marcadores)."""
    patron = "(" + "|".join(re.escape(m) for m in marcadores) + ")"
    partes = []
    for trozo in re.split(patron, texto):
        if trozo:
            partes.append((trozo, trozo in marcadores))
    return partes


# -----------------------------------------------------------------------------
# Columnas de captura
# -----------------------------------------------------------------------------
def normalizar_obligatorio(valor):
    """PyYAML lee «no» como False (YAML 1.1); se vuelve a la cadena de registro.yaml."""
    if valor is None or valor is False:
        return "no"
    if valor is True:
        return "si"
    return str(valor)


def valores_campo(spec, campo):
    """Valores permitidos de un campo de opción, de su lista propia o de registro.yaml > valores."""
    if campo.get("valores_ref"):
        return [v["valor"] if isinstance(v, dict) else v for v in spec["valores"][campo["valores_ref"]]]
    return list(campo.get("valores") or [])


def construir_columnas(spec):
    """Devuelve la lista de columnas de captura a partir de las secciones A a F."""
    columnas = []
    for seccion in spec["secciones"]:
        if seccion["id"] == "G":
            continue
        for c in seccion["campos"]:
            fid = c["id"]
            ayuda = AYUDA_EXCEL.get(fid) or c.get("ayuda") or c.get("pregunta", "")
            if fid in SOLO_ADMIN and fid not in AYUDA_EXCEL:
                ayuda += f" Solo aparecen áreas administrativas ({SOLO_ADMIN[fid]})."
            pc_vacia = (normalizar_obligatorio(c.get("obligatorio")) == "por_confirmar"
                        and c["tipo"] == "opcion" and "Por confirmar" not in valores_campo(spec, c))
            if pc_vacia:
                ayuda += AYUDA_PC_VACIA
            base = {
                "campo": fid,
                "seccion": seccion["id"],
                "tipo": c["tipo"],
                "obligatorio": normalizar_obligatorio(c.get("obligatorio")),
                "quien": c.get("quien", "area"),
                "ayuda": ayuda,
                "pc_vacia": pc_vacia,
            }
            if fid in SUBCAMPOS:
                for i, (sub, preg_sub) in enumerate(SUBCAMPOS[fid]):
                    pregunta = f"{c['pregunta']} {preg_sub}" if i == 0 else preg_sub
                    columnas.append({**base, "etiqueta": f"{fid} · {c['nombre']}: {sub}",
                                     "pregunta": pregunta, "tipo": "texto",
                                     "ancho": ANCHO_SUB[sub], "titulo_ayuda": f"{fid} · {sub}"})
                continue
            if c["tipo"] == "fecha_mes":
                base["ayuda"] = recortar(ayuda, 250 - len(FORMATO_FECHA_MES)) + FORMATO_FECHA_MES
            columnas.append({**base, "etiqueta": f"{fid} · {c['nombre']}", "pregunta": c["pregunta"],
                             "valores": c.get("valores"), "valores_ref": c.get("valores_ref"),
                             "ancho": ANCHOS.get(fid, 24), "titulo_ayuda": f"{fid} · {c['nombre']}"})
            if c.get("casilla"):
                columnas.append({"campo": fid, "seccion": seccion["id"], "tipo": "casilla",
                                 "obligatorio": "no", "quien": "area",
                                 "etiqueta": f"{fid} · Casilla", "pregunta": c["casilla"],
                                 "ayuda": f"Elija «Sí» si es su caso: {c['casilla']}",
                                 "ancho": ANCHO_CASILLA, "titulo_ayuda": f"{fid} · casilla"})
            for sub, preg, ayuda_sub, tipo, ancho in COMPLEMENTOS.get(fid, []):
                columnas.append({"campo": fid, "seccion": seccion["id"], "tipo": tipo,
                                 "obligatorio": "no", "quien": "area",
                                 "etiqueta": f"{fid} · {c['nombre']}: {sub}", "pregunta": preg,
                                 "ayuda": ayuda_sub, "ancho": ancho, "titulo_ayuda": f"{fid} · {sub}"})
    return columnas


def sufijo_encabezado(col):
    if col["quien"] == "dgetd":
        return "(lo llena la DGETD)"
    if col["obligatorio"] == "si":
        return "(obligatorio)"
    if col.get("pc_vacia"):
        return SUFIJO_PC_VACIA
    if col["obligatorio"] == "por_confirmar":
        return "(obligatorio o «Por confirmar»)"
    if col["seccion"] == "F" or col["obligatorio"] == "no":
        return "(opcional)"
    return ""


# -----------------------------------------------------------------------------
# Hoja Valores (oculta) y nombres definidos
# -----------------------------------------------------------------------------
def lista_valores(spec, col):
    if col["tipo"] == "casilla":
        return "casilla", CASILLA
    if col.get("valores_ref"):
        ref = col["valores_ref"]
        vals = spec["valores"][ref]
        return ref, [v["valor"] if isinstance(v, dict) else v for v in vals]
    if col.get("valores"):
        return f"{col['campo'].lower()}", list(col["valores"])
    return None, None


def hoja_valores(wb, spec, columnas):
    ws = wb.create_sheet(H_VAL)
    ws.sheet_state = "hidden"
    listas = {}
    for col in columnas:
        clave, vals = lista_valores(spec, col)
        if clave and clave not in listas:
            listas[clave] = vals
    nombres = {}
    j = 1
    for clave, vals in listas.items():
        letra = get_column_letter(j)
        ws.cell(row=1, column=j, value=clave).font = font(bold=True)
        for i, v in enumerate(vals, start=2):
            ws.cell(row=i, column=j, value=v).font = font()
        nombre = f"lst_{clave}"
        ref = f"{quote_sheetname(H_VAL)}!${letra}$2:${letra}${len(vals) + 1}"
        wb.defined_names[nombre] = DefinedName(nombre, attr_text=ref)
        nombres[clave] = nombre
        ws.column_dimensions[letra].width = max(14, min(60, max(len(str(v)) for v in vals) + 2))
        j += 1

    # Áreas y órganos: lista oficial (hoja Áreas) y la misma lista con «Por confirmar» al inicio.
    areas = quote_sheetname(H_AREAS)
    rango_areas = f"{areas}!$A${AREAS_PRIMERA}:$A${AREAS_PRIMERA + AREAS_MAX - 1}"
    wb.defined_names["lst_areas"] = DefinedName(
        "lst_areas",
        attr_text=f"OFFSET({areas}!$A${AREAS_PRIMERA},0,0,MAX(1,COUNTA({rango_areas})),1)")

    # Áreas administrativas (propietario y custodio): «Por confirmar» y luego solo las áreas de tipo
    # TIPO_ADMIN, sin huecos. Una columna auxiliar numera cada área administrativa y la siguiente
    # la acomoda en orden con INDEX y MATCH (funciona en cualquier versión de Excel).
    rango_tipos = f"{areas}!$B${AREAS_PRIMERA}:$B${AREAS_PRIMERA + AREAS_MAX - 1}"
    letra_n = get_column_letter(j)
    letra = get_column_letter(j + 1)
    ws.cell(row=1, column=j, value="n_area_admin").font = font(bold=True)
    ws.cell(row=1, column=j + 1, value="areas_admin_por_confirmar").font = font(bold=True)
    ws.cell(row=2, column=j + 1, value="Por confirmar").font = font()
    for i in range(AREAS_MAX):
        r = AREAS_PRIMERA + i
        ws.cell(row=2 + i, column=j, value=(
            f'=IF(AND({areas}!$A{r}<>"",{areas}!$B{r}="{TIPO_ADMIN}"),'
            f'COUNTIFS({areas}!$A${AREAS_PRIMERA}:$A{r},"<>",{areas}!$B${AREAS_PRIMERA}:$B{r},"{TIPO_ADMIN}"),"")'
        )).font = font()
        ws.cell(row=3 + i, column=j + 1, value=(
            f'=IFERROR(INDEX({rango_areas},MATCH({i + 1},${letra_n}$2:${letra_n}${AREAS_MAX + 1},0)),"")'
        )).font = font()
    ws.column_dimensions[letra_n].width = 14
    ws.column_dimensions[letra].width = 40
    wb.defined_names["lst_areas_adm_pc"] = DefinedName(
        "lst_areas_adm_pc",
        attr_text=(f"OFFSET({quote_sheetname(H_VAL)}!${letra}$2,0,0,"
                   f'1+COUNTIFS({rango_areas},"<>",{rango_tipos},"{TIPO_ADMIN}"),1)'))
    nombres["areas"] = "lst_areas"
    nombres["areas_adm_pc"] = "lst_areas_adm_pc"
    return nombres


# -----------------------------------------------------------------------------
# Encabezados de las hojas de captura
# -----------------------------------------------------------------------------
BORDE_DATOS = Border(bottom=Side(style="thin", color=LINE), right=Side(style="thin", color=LINE))
BORDE_ID = Border(right=Side(style="thin", color="FFFFFF"))
BORDE_PREGUNTA = Border(bottom=Side(style="medium", color=MINT), right=Side(style="thin", color="FFFFFF"))


def escribir_encabezados(ws, columnas, fila_id):
    """Renglón fila_id: ID y nombre corto. Renglón fila_id + 1: pregunta completa (encabezado de la tabla)."""
    fila_preg = fila_id + 1
    alto_id, alto_preg = 1, 1
    for j, col in enumerate(columnas, start=1):
        etiqueta = col["etiqueta"]
        sufijo = sufijo_encabezado(col)
        texto_id = f"{etiqueta}\n{sufijo}" if sufijo else etiqueta
        c = ws.cell(row=fila_id, column=j, value=texto_id)
        c.font = font(bold=True)
        c.fill = relleno(MINT_TINT)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = BORDE_ID
        p = ws.cell(row=fila_preg, column=j, value=col["pregunta"])
        p.font = font(size=9)
        p.fill = relleno(MINT_TINT)
        p.alignment = Alignment(wrap_text=True, vertical="top")
        p.border = BORDE_PREGUNTA
        ws.column_dimensions[get_column_letter(j)].width = col["ancho"]
        alto_id = max(alto_id, lineas(etiqueta, col["ancho"], negrita=True)
                      + (lineas(sufijo, col["ancho"], negrita=True) if sufijo else 0))
        alto_preg = max(alto_preg, lineas(col["pregunta"], col["ancho"], size=9))
    ws.row_dimensions[fila_id].height = 15 * alto_id + 3
    ws.row_dimensions[fila_preg].height = 12 * alto_preg + 4


def preparar_celdas_datos(ws, columnas, primera, ultima):
    for j, col in enumerate(columnas, start=1):
        dgetd = col["quien"] == "dgetd"
        for i in range(primera, ultima + 1):
            c = ws.cell(row=i, column=j)
            c.font = font(color=INK2 if dgetd else INK)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = BORDE_DATOS
            c.number_format = "@"
            if dgetd:
                c.fill = relleno(PANEL)


def imprimir_captura(ws):
    """Hojas anchas de captura: horizontal, carta, escala reducida y márgenes estrechos."""
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.scale = ESCALA_CAPTURA
    ws.page_margins.left = ws.page_margins.right = 0.4
    ws.page_margins.top = ws.page_margins.bottom = 0.5
    ws.print_options.gridLines = False


def agregar_tabla(ws, nombre, ref):
    tabla = Table(displayName=nombre, ref=ref)
    tabla.tableStyleInfo = TableStyleInfo(name=None, showFirstColumn=False, showLastColumn=False,
                                          showRowStripes=False, showColumnStripes=False)
    ws.add_table(tabla)


# -----------------------------------------------------------------------------
# Validaciones
# -----------------------------------------------------------------------------
def validaciones(ws, spec, columnas, nombres, primera, ultima, contacto):
    for j, col in enumerate(columnas, start=1):
        letra = get_column_letter(j)
        rango = f"{letra}{primera}:{letra}{ultima}"
        titulo = recortar(col["titulo_ayuda"], 32)
        prompt = recortar(col["ayuda"], 250)
        if col["tipo"] == "area":
            admin = col["campo"] in SOLO_ADMIN
            dv = DataValidation(type="list", formula1=nombres['areas_adm_pc' if admin else 'areas'],
                                allow_blank=True)
            dv.errorTitle = "Área no válida"
            dv.error = recortar(
                "Elija el área de la lista desplegable. No la escriba a mano. "
                + (f"Solo aparecen áreas administrativas ({SOLO_ADMIN[col['campo']]}). "
                   "Si no la sabe, elija «Por confirmar». " if admin else "")
                + f"Si su área no aparece, avísenos: {contacto}", 250)
        else:
            clave, vals = lista_valores(spec, col)
            if clave:
                dv = DataValidation(type="list", formula1=nombres[clave], allow_blank=True)
                dv.errorTitle = "Opción no válida"
                if "Por confirmar" in vals:
                    dv.error = ("Elija una opción de la lista desplegable (flecha a la derecha de la celda). "
                                "Si no sabe la respuesta, elija «Por confirmar».")
                else:
                    opciones = ", ".join(f"«{v}»" for v in vals)
                    msg = f"Elija una opción de la lista desplegable: {opciones}."
                    if col.get("pc_vacia"):
                        msg += " Si no lo sabe, deje la celda vacía."
                    if len(msg) > 225:
                        msg = "Elija una opción de la lista desplegable (flecha a la derecha de la celda)."
                    dv.error = msg
            else:
                # Texto libre: sin restricción, solo el mensaje de ayuda al seleccionar la celda.
                dv = DataValidation(allow_blank=True)
        dv.errorStyle = "stop"
        dv.showErrorMessage = dv.type == "list"
        dv.promptTitle = titulo
        dv.prompt = prompt
        dv.showInputMessage = True
        dv.add(rango)
        ws.add_data_validation(dv)


# -----------------------------------------------------------------------------
# Hoja «Mis listas»
# -----------------------------------------------------------------------------
def hoja_mis_listas(wb, spec, columnas):
    ws = wb.create_sheet(H_MIS)
    ws.sheet_properties.tabColor = MINT
    escribir_encabezados(ws, columnas, fila_id=1)
    primera, ultima = 3, 2 + FILAS_CAPTURA
    preparar_celdas_datos(ws, columnas, primera, ultima)

    # C1: si el área que registra (A1) es un área administrativa, viene marcada y la persona la cambia
    # si decide otra. Si es un órgano jurisdiccional, viene «Por confirmar»: el propietario es el área
    # administrativa competente (art. 4 fr. XVII).
    j_a1 = next(j for j, c in enumerate(columnas, 1) if c["campo"] == "A1")
    j_c1 = next(j for j, c in enumerate(columnas, 1) if c["campo"] == "C1")
    la1 = get_column_letter(j_a1)
    areas = quote_sheetname(H_AREAS)
    rango_nombres = f"{areas}!$A${AREAS_PRIMERA}:$A${AREAS_PRIMERA + AREAS_MAX - 1}"
    rango_tipos = f"{areas}!$B${AREAS_PRIMERA}:$B${AREAS_PRIMERA + AREAS_MAX - 1}"
    for i in range(primera, ultima + 1):
        formula = (f'=IF(${la1}{i}="","",IF(COUNTIFS({rango_nombres},${la1}{i},{rango_tipos},"{TIPO_ADMIN}")>0,'
                   f'${la1}{i},"Por confirmar"))')
        c = ws.cell(row=i, column=j_c1, value=formula)
        c.number_format = "General"

    ultima_col = get_column_letter(len(columnas))
    agregar_tabla(ws, "tblMisListas", f"A2:{ultima_col}{ultima}")
    ws.freeze_panes = "B3"
    ws.sheet_view.zoomScale = 100
    ws.print_title_rows = "1:2"
    ws.print_title_cols = "A:A"
    imprimir_captura(ws)
    # Área de impresión dinámica: los encabezados y solo hasta el último renglón con A1, A2, B2 o B3
    # (C1 trae fórmula en todos los renglones, por eso no cuenta). Sin datos, imprime un renglón vacío.
    hoja = quote_sheetname(H_MIS)
    letras = [get_column_letter(next(j for j, c in enumerate(columnas, 1) if c["etiqueta"].startswith(e)))
              for e in ("A1 ", "A2 ", "B2 ", "B3 ")]
    texto = "&".join(f"{hoja}!${l}${primera}:${l}${ultima}" for l in letras)
    ultimo = f"SUMPRODUCT(MAX((LEN({texto})>0)*ROW({hoja}!$A${primera}:$A${ultima})))"
    ws.defined_names["_xlnm.Print_Area"] = DefinedName(
        "_xlnm.Print_Area", attr_text=f"OFFSET({hoja}!$A$1,0,0,MAX({primera},{ultimo}),{len(columnas)})")
    return ws


# -----------------------------------------------------------------------------
# Hoja «Ejemplo»
# -----------------------------------------------------------------------------
EJEMPLOS = [
    {
        "A1": "Dirección General de Inmuebles y Mantenimiento",
        "A2 · nombre completo": "Ana Laura Pérez Gómez",
        "A2 · puesto": "Jefa de Departamento de Control Inmobiliario",
        "A2 · correo institucional": "ana.perez@[dominio institucional]",
        "A2 · extensión": "4521",
        "A3 · nombre completo": "(nombre de la persona titular)",
        "A3 · puesto": "Titular de la Dirección General de Inmuebles y Mantenimiento",
        "B1": "",
        "B1b": "INM-01",
        "B2": "Catálogo de inmuebles del OAJ",
        "B3": ("Lista de los inmuebles que ocupa el OAJ, con domicilio y uso. Se usa para programar "
               "mantenimiento y para ubicar órganos en los reportes estadísticos."),
        "C1": "Dirección General de Inmuebles y Mantenimiento",
        "C2": "Dirección General de Inmuebles y Mantenimiento",
        "C2 · persona de contacto": "Ana Laura Pérez Gómez, Jefa de Departamento de Control Inmobiliario, ext. 4521",
        "C2b": "No sé",
        "C3": "Entidades",
        "D1": ("Sistema de mantenimiento de inmuebles\n"
               "Reporte mensual de ocupación (Excel de la Dirección de Estadística)"),
        "D1 · casilla": "Sí",
        "D2": "Cada vez que ocurre un cambio",
        "D2 · qué lo dispara": "Cuando se arrienda, se adquiere o se desocupa un inmueble.",
        "D3": "No",
        "D3 · versión actual": "",
        "D4": "2026-09",
        "D4 · casilla": "No",
        "E1": "Interna",
        "E2": "No",
        "F1": "En una hoja de cálculo en carpeta compartida",
        "F2": "De 50 a 500",
        "F3": "Sí, y la clave tiene significado (incluye año, lugar, materia u otro dato)",
        "F4": "La Dirección de Estadística lleva una copia para sus reportes.",
        "F5": "Otras áreas tienen versiones distintas y hay que conciliarlas a mano para cada reporte.",
    },
    {
        "A1": "Dirección General de Archivo y Documentación",
        "A2 · nombre completo": "Luis Alberto Hernández Mora",
        "A2 · puesto": "Subdirector de Gestión Documental",
        "A2 · correo institucional": "luis.hernandez@[dominio institucional]",
        "A2 · extensión": "3310",
        "A3 · nombre completo": "(nombre de la persona titular)",
        "A3 · puesto": "Titular de la Dirección General de Archivo y Documentación",
        "B1": "",
        "B1b": "",
        "B2": "Catálogo de tipos de documento",
        "B3": ("Lista de los tipos de documento que se reciben y se generan en el OAJ, como oficio, "
               "acuerdo o circular. Se usa para clasificar documentos en el sistema de gestión documental "
               "y para los reportes de archivo."),
        "C1": "Por confirmar",
        "C2": "Dirección General de Archivo y Documentación",
        "C2 · persona de contacto": "Luis Alberto Hernández Mora, Subdirector de Gestión Documental, ext. 3310",
        "C2b": "Sí",
        "C3": "Clasificación",
        "D1": "Sistema de gestión documental\nTablero de correspondencia de la Oficialía de Partes",
        "D1 · casilla": "Sí",
        "D2": "Casi nunca cambia",
        "D2 · qué lo dispara": "",
        "D3": "Sí (indique cuál es la actual)",
        "D3 · versión actual": "v2.1",
        "D4": "Por confirmar",
        "D4 · casilla": "Sí",
        "E1": "Interna",
        "E2": "No",
        "F1": "En un sistema o base de datos",
        "F2": "Menos de 50",
        "F3": "Sí, y es un número sin significado",
        "F4": "",
        "F5": "Se recaptura en dos sistemas y a veces no coinciden.",
    },
]


def clave_ejemplo(col):
    """Clave con la que EJEMPLOS identifica cada columna."""
    etiqueta = col["etiqueta"]
    if ": " in etiqueta:
        return f"{col['campo']} · {etiqueta.split(': ', 1)[1]}"
    if col["tipo"] == "casilla":
        return f"{col['campo']} · casilla"
    return col["campo"]


def hoja_ejemplo(wb, spec, columnas):
    ws = wb.create_sheet(H_EJ)
    ws.sheet_properties.tabColor = "D9950F"
    aviso = ("EJEMPLOS ILUSTRATIVOS. Las personas, sistemas y claves no son reales; las áreas se usan solo como "
             "ejemplo y los renglones no describen sus listas reales. No copie estos renglones en «Mis listas».")
    c = ws.cell(row=1, column=1, value=aviso)
    c.font = font(bold=True, color=AMBER_INK)
    for j in range(1, len(columnas) + 1):
        ws.cell(row=1, column=j).fill = relleno(AMBER_TINT)
    ws.row_dimensions[1].height = 22
    c.alignment = Alignment(vertical="center")

    escribir_encabezados(ws, columnas, fila_id=2)
    primera = 4
    ultima = primera + len(EJEMPLOS) - 1
    preparar_celdas_datos(ws, columnas, primera, ultima)
    for i, ejemplo in enumerate(EJEMPLOS, start=primera):
        alto = 1
        for j, col in enumerate(columnas, start=1):
            clave = clave_ejemplo(col)
            if clave not in ejemplo:
                raise KeyError(f"Falta el valor de ejemplo para la columna {clave}")
            valor = ejemplo[clave]
            celda = ws.cell(row=i, column=j)
            if col["quien"] == "dgetd" and not valor:
                celda.value = "Lo asigna la DGETD"
                celda.font = font(italic=True, color=INK2)
            else:
                celda.value = valor or None
            # Los valores de opción deben existir en registro.yaml
            _, vals = lista_valores(spec, col)
            if vals and valor and valor not in vals:
                raise ValueError(f"Valor de ejemplo no permitido en {clave}: {valor}")
            alto = max(alto, lineas(valor, col["ancho"]))
        ws.row_dimensions[i].height = 15 * alto + 4
    agregar_tabla(ws, "tblEjemplo", f"A3:{get_column_letter(len(columnas))}{ultima}")
    ws.freeze_panes = "B4"
    ws.print_title_rows = "2:3"
    imprimir_captura(ws)
    return ws


# -----------------------------------------------------------------------------
# Hoja «Áreas»
# -----------------------------------------------------------------------------
def hoja_areas(wb, spec):
    ws = wb.create_sheet(H_AREAS)
    notas = [
        ("Esta hoja es de la DGETD. Usted no tiene que llenarla ni modificarla.", True),
        ("Aquí está la lista oficial de áreas administrativas y órganos jurisdiccionales. De aquí salen las "
         "opciones de A1 en «Mis listas». C1 y C2 solo ofrecen áreas administrativas (art. 4 fr. VI y XVII).",
         False),
        ("Para la DGETD: antes de publicar la plantilla, borre los 3 renglones de ejemplo y pegue la lista "
         "oficial a partir del renglón 5, un área u órgano por renglón y sin renglones vacíos. Anote en la "
         f"columna Tipo «{TIPO_ADMIN}» u «{TIPO_OJ}»: sin el tipo, el área no aparece en C1 ni en C2.", False),
    ]
    # Renglón 1 y 2: notas; renglón 3: nota para la DGETD; renglón 4: encabezado de la tabla.
    for i, (texto, negrita) in enumerate(notas, start=1):
        c = ws.cell(row=i, column=1, value=texto)
        c.font = font(bold=negrita, color=AMBER_INK if i == 3 else INK)
        # Cada nota ocupa el ancho de las 3 columnas de la tabla, para que no se salga al imprimir.
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=3)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[i].height = 15 * lineas(texto, 70 + 24 + 52, negrita=negrita) + 3
        if i == 3:
            for j in range(1, 4):
                ws.cell(row=i, column=j).fill = relleno(AMBER_TINT)
    encabezados = ["Área u órgano (nombre oficial completo)", "Tipo", "Observación"]
    for j, texto in enumerate(encabezados, start=1):
        c = ws.cell(row=4, column=j, value=texto)
        c.font = font(bold=True)
        c.fill = relleno(MINT_TINT)
        c.border = Border(bottom=Side(style="medium", color=MINT))
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ejemplos = [
        ("[Ejemplo] Dirección General de Estrategia y Transformación Digital", TIPO_ADMIN),
        ("[Ejemplo] Dirección General de Inmuebles y Mantenimiento", TIPO_ADMIN),
        ("[Ejemplo] Juzgado Primero de Distrito en Materia Penal en la Ciudad de México", TIPO_OJ),
    ]
    for i, (nombre, tipo) in enumerate(ejemplos, start=AREAS_PRIMERA):
        valores = [nombre, tipo, "Ejemplo ilustrativo. Bórrelo al cargar la lista oficial."]
        for j, v in enumerate(valores, start=1):
            c = ws.cell(row=i, column=j, value=v)
            c.font = font(color=AMBER_INK if j in (1, 3) else INK)
            c.border = BORDE_DATOS
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 70
    ws.column_dimensions["B"].width = 24
    ws.column_dimensions["C"].width = 52
    agregar_tabla(ws, "tblAreas", f"A4:C{AREAS_PRIMERA + len(ejemplos) - 1}")
    dv = DataValidation(type="list", formula1=f'"{TIPO_ADMIN},{TIPO_OJ}"', allow_blank=True)
    dv.errorTitle = "Tipo no válido"
    dv.error = f"Escriba «{TIPO_ADMIN}» u «{TIPO_OJ}». De este dato depende qué áreas aparecen en C1 y C2."
    dv.errorStyle = "stop"
    dv.showErrorMessage = True
    dv.add(f"B{AREAS_PRIMERA}:B{AREAS_PRIMERA + AREAS_MAX - 1}")
    ws.add_data_validation(dv)
    ws.freeze_panes = "A5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return ws


# -----------------------------------------------------------------------------
# Hoja «Cómo llenar»
# -----------------------------------------------------------------------------
def contenido_como_llenar(spec, columnas):
    m = marcadores_de(spec)
    # Campos de opción que aceptan «por confirmar» sin tener ese valor en su lista (hoy, D3).
    pc_vacia = sorted({col["campo"] for col in columnas if col.get("pc_vacia")})
    idea_pc = ("Si el encabezado de una columna menciona «Por confirmar» y usted no sabe la respuesta, elija "
               "o escriba «Por confirmar». No invente datos: la DGETD le ayuda a completarlos.")
    if pc_vacia:
        idea_pc += (f" En {' y '.join(pc_vacia)}, si no lo sabe, deje la celda vacía: "
                    "se registra «Por confirmar».")
    clas = spec["valores"]["clasificacion"]
    acceso = spec["valores"]["nivel_acceso"]
    # Cada elemento: ("titulo", texto) | ("idea", número o "", texto) | ("vacio",)
    c = [
        ("portada", "Registro de catálogos existentes · Plantilla de Excel para varias listas"),
        ("sub", f"F-CAT-01 · Versión {spec['version']} · {spec['estatus']} · no vigente"),
        ("sub", "Dirección General de Estrategia y Transformación Digital (DGETD) · "
                "Órgano de Administración Judicial (OAJ)"),
        ("vacio",),
        ("titulo", "Para qué sirve"),
        ("idea", "", "Con esta plantilla su área registra varias listas a la vez ante la DGETD."),
        ("idea", "", "Úsela si su área lleva más de 5 listas. Si lleva 5 o menos, use el formulario en línea: "
                     f"{m['liga_formulario']}."),
        ("idea", "", "Ante la duda, registre la lista. La DGETD revisa después si es catálogo institucional. "
                     "Registrar no es autorizar."),
        ("vacio",),
        ("titulo", "Fecha límite"),
        ("idea", "", f"Suba la plantilla a más tardar el {m['fecha_limite_registro']}."),
        ("vacio",),
        ("titulo", "La regla principal: un renglón por lista"),
        ("idea", "", "Cada renglón de la hoja «Mis listas» es una lista. Si su área lleva 12 listas, llene 12 renglones."),
        ("idea", "", "No junte dos listas en un renglón ni reparta una lista en dos renglones."),
        ("idea", "", "Cada renglón recibe su propio folio de registro y su propia clave de catálogo."),
        ("vacio",),
        ("titulo", "Cómo llenarla"),
        ("idea", "1.", "Vea primero la hoja «Ejemplo»: tiene 2 listas llenas a modo de ilustración."),
        ("idea", "2.", "Escriba en la hoja «Mis listas» a partir del renglón 3. Los renglones 1 y 2 dicen qué va en cada columna."),
        ("idea", "3.", "Al seleccionar una celda aparece un recuadro con ayuda sobre esa pregunta."),
        ("idea", "4.", "En las columnas con flecha, elija una opción de la lista. La celda no acepta otro texto."),
        ("idea", "5.", "Elija el área de la lista oficial de áreas y órganos. No la escriba a mano: así la misma "
                       "área no aparece escrita de varias formas. En C1 y C2 solo aparecen áreas administrativas, "
                       "porque los Lineamientos asignan a un área administrativa la tarea de decidir qué entra en "
                       "la lista (propietario) y la de mantenerla (custodio)."),
        ("idea", "6.", f"Si su área no aparece en la lista, avísenos: {m['contacto_dgetd']}."),
        ("idea", "7.", "Llene siempre las columnas marcadas «(obligatorio)». Si se le acerca la fecha límite, envíe la "
                       "plantilla con lo que sepa: el área (A1), el nombre (B2) y la descripción (B3) son "
                       "indispensables; lo demás puede ir «Por confirmar» y la DGETD lo completa con usted."),
        ("idea", "8.", idea_pc),
        ("idea", "9.", "La columna B1 la llena la DGETD. Déjela vacía."),
        ("idea", "10.", "Si su área es un área administrativa, la columna C1 la trae ya marcada. Cámbiela si otra "
                        "área decide qué entra y qué sale de la lista. Si registra un órgano jurisdiccional, C1 trae "
                        "«Por confirmar»: elija el área administrativa competente en la materia o déjela así. "
                        "Si deja C1 en blanco, se registra «Por confirmar»."),
        ("idea", "11.", "Las columnas de la sección F son opcionales. Nos ayudan a preparar el plan de adecuación "
                        "de los catálogos existentes."),
        ("idea", "12.", "Para escribir varios renglones dentro de una celda (por ejemplo, en D1), use Alt + Entrar."),
        ("idea", "13.", "No agregue, quite ni mueva columnas, y no cambie el nombre de las hojas. Así la DGETD pasa "
                        "sus respuestas al inventario sin recapturarlas."),
        ("vacio",),
        ("titulo", "Qué no le pedimos"),
        ("idea", "", "El contenido de la lista. No pegue ni adjunte la lista: solo describa de qué es."),
        ("idea", "", "Datos personales. La pregunta E2 solo pide saber si la lista los contiene."),
        ("idea", "", "Cambios en sus sistemas. Registrar no publica la lista, no cambia quién la administra "
                     "ni modifica ningún sistema."),
        ("idea", "", "Decisiones definitivas. El propietario, el custodio y la clasificación que anote son propuestas: "
                     "los formaliza el Comité de Gobernanza Digital al aprobar el catálogo."),
        ("vacio",),
        ("titulo", "Cómo entregarla"),
        ("idea", "", "Guarde el archivo en formato de Excel (.xlsx)."),
        ("idea", "", f"Súbalo a la carpeta de SharePoint: {m['liga_sharepoint']}."),
        ("idea", "", "No lo envíe por correo."),
        ("idea", "", "La fecha de recepción es el día en que sube el archivo a la carpeta."),
        ("idea", "", "Para corregir una plantilla ya enviada, no la vuelva a subir; avise a su persona de contacto. "
                     "Si la vuelve a subir, todas sus listas se registran otra vez."),
        ("idea", "", "Aviso de privacidad sobre los datos de las personas que anota en A2, A3 y C2: "
                     f"{m['aviso_privacidad']}."),
        ("vacio",),
        ("titulo", "Qué hace la DGETD después (compromiso DGETD)"),
        ("idea", "", "Le envía un acuse con un folio y una clave de catálogo por cada renglón, con copia a la "
                     "persona titular que valida (A3)."),
        ("idea", "", "Prellena lo que ya conoce y le envía la ficha de cada lista para que la confirme. "
                     f"Plazo: {m['plazo_ficha_confirmacion']}."),
        ("idea", "", "Le asigna una persona de contacto con nombre para resolver sus dudas. "
                     f"Plazo de respuesta: {m['plazo_respuesta_dudas']}."),
        ("idea", "", "No le volverá a pedir lo que ya entregó."),
        ("idea", "", "El registro no es una auditoría. Los errores se corrigen sin costo hasta el dictamen."),
        ("vacio",),
        ("titulo", "Dudas"),
        ("idea", "", f"Asesoría DGETD: {m['contacto_dgetd']}."),
        ("idea", "", "Si lo prefiere, pida un registro acompañado por Teams o por teléfono: la DGETD captura "
                     "mientras usted responde."),
        ("vacio",),
        ("titulo", "Qué significa cada opción de C3 (tipo de lista)"),
    ]
    for v in clas:
        if v["ejemplo"]:
            c.append(("idea", "", f"{v['valor']}: {v['pregunta'].lower()}. Por ejemplo: {v['ejemplo']}."))
        else:
            c.append(("idea", "", f"{v['valor']}: {v['pregunta'].lower()}."))
    c += [("vacio",), ("titulo", "Qué significa cada opción de E1 (nivel de acceso)")]
    for v in acceso:
        c.append(("idea", "", f"{v['valor']}: {v['descripcion'][0].lower()}{v['descripcion'][1:]}"))
    c += [
        ("vacio",),
        ("titulo", "Fundamento"),
        ("idea", "", "Lineamientos Generales de Catálogos Institucionales (LGCI): Transitorio CUARTO (registro de "
                     "los catálogos existentes) y artículo 8 (metadatos obligatorios)."),
        ("idea", "", "Propietario y custodio: son áreas administrativas (art. 4 fr. VI y XVII) y los formaliza "
                     "el Comité al aprobar el catálogo (art. 12). Clasificación: art. 5. Criterios de catálogo "
                     "institucional: art. 6."),
        ("idea", "", "Procedimiento: PR-CAT-04 Procedimiento de registro de catálogos existentes."),
    ]
    return c


def hoja_como_llenar(wb, spec, columnas):
    ws = wb.active
    ws.title = H_COMO
    ws.sheet_properties.tabColor = MINT_INK
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 110
    marcadores = list(marcadores_de(spec).values())
    fila = 1
    for item in contenido_como_llenar(spec, columnas):
        tipo = item[0]
        if tipo == "vacio":
            ws.row_dimensions[fila].height = 8
        elif tipo == "portada":
            c = ws.cell(row=fila, column=2, value=item[1])
            c.font = font(size=14, bold=True)
            ws.row_dimensions[fila].height = 22
        elif tipo == "sub":
            c = ws.cell(row=fila, column=2, value=item[1])
            c.font = font(color=INK2)
        elif tipo == "titulo":
            if item[1] in SALTO_ANTES:
                ws.row_breaks.append(Break(id=fila - 1))
            c = ws.cell(row=fila, column=2, value=item[1])
            c.font = font(bold=True, color=MINT_INK)
            c.fill = relleno(MINT_TINT)
            c.border = Border(bottom=Side(style="medium", color=MINT))
            a = ws.cell(row=fila, column=1)
            a.fill = relleno(MINT_TINT)
            a.border = Border(bottom=Side(style="medium", color=MINT))
            ws.row_dimensions[fila].height = 18
        elif tipo == "idea":
            _, numero, texto = item
            if numero:
                n = ws.cell(row=fila, column=1, value=numero)
                n.font = font(bold=True, color=MINT_INK)
                n.alignment = Alignment(horizontal="right", vertical="top")
            partes = partir_marcadores(texto, marcadores)
            c = ws.cell(row=fila, column=2)
            if any(es for _, es in partes):
                c.value = rico(partes)
                c.fill = relleno(AMBER_TINT)
            else:
                c.value = texto
                c.font = font()
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[fila].height = 15 * lineas(texto, 110) + 2
        fila += 1
    ws.page_setup.orientation = "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left = ws.page_margins.right = 0.5
    return ws


# -----------------------------------------------------------------------------
# Libro
# -----------------------------------------------------------------------------
def main():
    with open(SPEC, encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)
    columnas = construir_columnas(spec)

    wb = Workbook()
    hoja_como_llenar(wb, spec, columnas)
    ws_mis = hoja_mis_listas(wb, spec, columnas)
    hoja_ejemplo(wb, spec, columnas)
    hoja_areas(wb, spec)
    nombres = hoja_valores(wb, spec, columnas)
    # Las validaciones se agregan cuando ya existen los nombres definidos de «Valores».
    validaciones(ws_mis, spec, columnas, nombres, 3, 2 + FILAS_CAPTURA, spec["marcadores"]["contacto_dgetd"])

    p = wb.properties
    p.title = "F-CAT-01 Registro de catálogos existentes · Plantilla de Excel para varias listas"
    p.subject = "Registro de catálogos existentes (Transitorio CUARTO de los LGCI)"
    p.creator = "DGETD"
    p.lastModifiedBy = "DGETD"
    p.description = (f"Versión {spec['version']} · {spec['estatus']} · no vigente. "
                     "Generada con build/plantilla_excel.py a partir de spec/registro.yaml.")
    p.keywords = "F-CAT-01; catálogos; registro; LGCI; DGETD; OAJ"
    p.category = "Formato"
    p.language = "es-MX"
    wb.calculation.fullCalcOnLoad = True
    wb.active = 0

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    wb.save(SALIDA)
    print(f"Escrito {SALIDA} · {len(columnas)} columnas · {FILAS_CAPTURA} renglones de captura")



if __name__ == "__main__":
    main()
