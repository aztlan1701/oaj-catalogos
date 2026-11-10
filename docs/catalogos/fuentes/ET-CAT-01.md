---
codigo: ET-CAT-01
titulo: Estándar técnico de estructura, identificación, versionamiento y publicación de catálogos institucionales
subtitulo: Artículo 14, fracción II, y Transitorio TERCERO de los Lineamientos Generales de Catálogos Institucionales
tipo: Estándar técnico
version: "0.1"
fecha: "Noviembre de 2026"
estatus: Borrador para revisión · no vigente
responsable: Dirección General de Estrategia y Transformación Digital (DGETD)
fundamento: "LGCI, art. 14 fr. II y IX; arts. 7, 8, 13, 22 y 25; Transitorio TERCERO"
portada: completa
---

# 1. Objeto

Este estándar fija las reglas técnicas con las que se describe, identifica, versiona y publica un catálogo institucional del Órgano de Administración Judicial (OAJ). Lo emite la Dirección General de Estrategia y Transformación Digital (DGETD) en cumplimiento del artículo 14, fracción II, de los Lineamientos Generales de Catálogos Institucionales (en adelante, los Lineamientos o LGCI).

::: {custom-style="Norma"}
**Lo que dice la norma.** La DGETD tiene la obligación de «establecer y publicar estándares técnicos para la estructura y formato de catálogos» (art. 14 fr. II).
:::

## 1.1 Qué regula

1. La ficha de metadatos de cada catálogo: los 11 metadatos del art. 8 y los metadatos complementarios que necesita el registro.
2. La clave de catálogo y el folio de registro.
3. El estatus del trámite de registro y el estatus del catálogo en el inventario.
4. Los valores permitidos de los metadatos que se responden con una lista cerrada de opciones.
5. La estructura mínima de los registros, el identificador único de registro, el versionamiento, la publicación en formatos abiertos y la interoperabilidad entre catálogos.

## 1.2 Estado de esta versión

::: {custom-style="Nota"}
**Versión 0.1.** Los capítulos 1 a 8, el 14 y el Anexo A tienen contenido aplicable al registro de catálogos existentes (Transitorio CUARTO). Los capítulos 9 a 13 contienen lo que ya fijan los Lineamientos, lo que este estándar definirá y las decisiones pendientes; su contenido se completa en la ola 2 del paquete normativo.
:::

## 1.3 Documentos relacionados

| Código | Documento | Relación con este estándar |
|----------------|----------------------------------------|----------------------------------------|
| [PR-CAT-04]{custom-style="Clave"} | Procedimiento de registro de catálogos existentes | Aplica los capítulos 5 a 8 al registro del Transitorio CUARTO. |
| [F-CAT-01]{custom-style="Clave"} | Registro de catálogo existente | Recoge la ficha de metadatos. La correspondencia está en el Anexo A. |
| [F-CAT-03]{custom-style="Clave"} | Diccionario de datos | Documenta los atributos de cada catálogo (capítulo 9). |
| [F-CAT-05]{custom-style="Clave"} | Solicitud de cambio estructural o retiro | Inicia una nueva versión formal o un retiro (capítulos 7 y 11). |
| [F-CAT-06]{custom-style="Clave"} | Bitácora de cambios menores | Registra los cambios de contenido que no generan versión (capítulo 11). |
| [PR-CAT-01]{custom-style="Clave"} | Procedimiento de gestión del ciclo de vida de catálogos | Aplica los capítulos 9 a 13 en cada fase del art. 9. |
| [ET-CAT-02]{custom-style="Clave"} | Catálogo de indicadores y umbrales de calidad | Mide la calidad de los catálogos que cumplen este estándar. |

: Documentos del paquete que dependen de este estándar

La DGETD publica, además, un resumen visual de dos páginas, «ET-CAT-01 en una mirada», para áreas de tecnologías de la información, personas enlace y titulares. En caso de diferencia entre el resumen y este estándar, manda este estándar.

# 2. Ámbito de aplicación

## 2.1 A quién aplica

Los Lineamientos son de observancia obligatoria para las áreas administrativas y los órganos jurisdiccionales a cargo del OAJ (artículo 3 de los Lineamientos). Este estándar desarrolla los artículos 7, 8, 13, 22 y 25 de los Lineamientos en los aspectos que esos artículos remiten a lo que establezca la DGETD y en las reglas técnicas que la DGETD emite conforme al art. 14 fr. II. Las remisiones expresas son el formato del identificador único de registro (art. 7 fr. I d)), el esquema de versiones (art. 13 fr. III) y los formatos de publicación (art. 22).

El estándar aplica también a la DGETD cuando asigna claves, lleva el inventario o actúa como custodio de un catálogo.

## 2.2 A qué aplica

1. A los catálogos institucionales definidos en el art. 4 fr. III.
2. Durante la transición, a las listas que las áreas y los órganos jurisdiccionales registran conforme al Transitorio CUARTO, aunque todavía no se haya determinado si son catálogos institucionales (art. 6).
3. A una lista con estatus «Uso local» solo le aplica la ficha de metadatos con la que quedó documentada.

::: {custom-style="Nota"}
**Registrar no es autorizar.** El registro documenta la lista en el inventario. La DGETD revisa después si cumple los criterios del art. 6. Registrar no publica la lista, no cambia quién la administra ni modifica ningún sistema.
:::

## 2.3 Qué no regula

1. El contenido de los catálogos. Las reglas de negocio las define el propietario (art. 15 fr. I).
2. La designación del propietario y del custodio, que formaliza el Comité de Gobernanza Digital (en adelante, el Comité) al aprobar el catálogo (art. 12).
3. Los pasos, plazos y responsables de cada trámite, que fijan PR-CAT-04 y PR-CAT-01.
4. Los indicadores y umbrales de calidad, que fija ET-CAT-02.
5. Los criterios para resolver asuntos. Un catálogo es una lista de valores de referencia y no fija criterios jurisdiccionales.

# 3. Fundamento

El artículo 14, fracción II, de los Lineamientos obliga a la DGETD a establecer y publicar estándares técnicos. Otras disposiciones remiten de forma expresa a lo que la DGETD establezca o requieren reglas técnicas para cumplirse. La tabla siguiente indica qué capítulo desarrolla cada una.

| Disposición | Lo que establece | Capítulo que la desarrolla |
|--------------------|--------------------------------------------------|------------------------------|
| Art. 14 fr. II | La DGETD establece y publica estándares técnicos para la estructura y formato de catálogos. | Todo el estándar |
| Art. 14 fr. IX | La DGETD emite los formatos y procedimientos operativos para la gestión de catálogos. | Capítulo 5 y Anexo A (base de F-CAT-01) |
| Art. 7 | Atributos mínimos de todo catálogo y criterios del identificador único de registro: persistencia, unicidad global, neutralidad semántica y formato que establezca la DGETD. | Capítulos 9 y 10 |
| Art. 8 | Los 11 metadatos obligatorios de todo catálogo. | Capítulos 5 y 8 |
| Art. 13 fr. III | Cada cambio estructural mayor recibe un nuevo número de versión «siguiendo el esquema establecido por la DGETD». | Capítulo 11 |
| Art. 22 | Los catálogos se publican en formatos estructurados abiertos «conforme a los estándares técnicos establecidos por la DGETD». | Capítulo 12 |
| Art. 25 | Principios de interoperabilidad: identificadores únicos y estables, reutilización, relaciones explícitas y estándares abiertos. | Capítulos 6, 10 y 13 |
| Transitorio TERCERO | La DGETD publica formatos, procedimientos y estándares técnicos dentro de los 60 días naturales siguientes a la entrada en vigor. | Capítulo 14 |

: Disposiciones de los Lineamientos que fundamentan este estándar

Se aplican además, como disposiciones relacionadas, el art. 4 fr. XIX (versionamiento), el art. 5 (clasificación y alcance), el art. 12 (formalización de propietario y custodio) y el Transitorio CUARTO (registro de catálogos existentes con los metadatos del art. 8).

::: {custom-style="Pendiente"}
**Por confirmar.** El plazo del Transitorio TERCERO vence el [miércoles 16 de diciembre de 2026, por confirmar]{custom-style="Marcador"}. La fecha depende de la [fecha de entrada en vigor por confirmar]{custom-style="Marcador"} (vacío V1).
:::

# 4. Definiciones operativas

Los términos definidos en el artículo 4 de los Lineamientos se usan en este estándar con ese significado. Entre ellos: atributo de catálogo, catálogo institucional, catálogo autorizado, custodio, propietario, datos de referencia, diccionario de datos, elemento de catálogo, metadatos, sistema consumidor y versionamiento. Este capítulo solo agrega los términos que los Lineamientos no definen o que necesitan precisión operativa.

| Término | Definición operativa |
|----------------------|------------------------------------------------------------------------------|
| Lista | Conjunto de valores que un área o un órgano jurisdiccional mantiene y que otros sistemas, áreas o reportes usan o copian. Equivale a «catálogo de información» del Transitorio CUARTO. Se registra cada lista por separado, sin juzgar antes si cumple el art. 6. |
| Ficha de metadatos | Conjunto de los 11 metadatos del art. 8 y de los metadatos complementarios del capítulo 5 que describen una lista. Describe la lista, no su contenido. La ficha de confirmación es la ficha que la DGETD prellena y envía al área para que la revise y la confirme. |
| Clave de catálogo | Identificador del catálogo (art. 8 fr. I), con formato [CAT-NNNN]{custom-style="Clave"}, que asigna la DGETD. Identifica al catálogo completo. Cada elemento del catálogo tiene, además, su identificador único de registro (art. 7 fr. I; capítulo 10). |
| Folio de registro | Identificador de un trámite de registro, con formato [RC-AAAA-NNNN]{custom-style="Clave"}. Un catálogo tiene una sola clave y puede tener varios folios. |
| Valor permitido | Cada opción de una lista cerrada que acepta un metadato o un atributo. Un valor que no está en la lista se rechaza. |
| «Por confirmar» | Respuesta válida en los metadatos marcados como «acepta "por confirmar"». Indica que el área todavía no conoce el dato. No es un error: la DGETD ayuda al área a completarlo. |
| Inventario | Registro que lleva la DGETD de las listas que recibe en el registro del Transitorio CUARTO, cada una con su ficha y su estatus. Los catálogos autorizados (art. 4 fr. IV) que contiene forman el inventario institucional de catálogos autorizados que la DGETD mantiene conforme al art. 14 fr. I. |
| Estatus de registro | Estado del trámite de registro identificado con un folio (sección 7.1). |
| Estatus en el inventario | Estado de la lista dentro del inventario (sección 7.2). Es distinto del estatus de vigencia de cada elemento (art. 7 fr. III; capítulo 9). |

: Definiciones operativas de este estándar

# 5. Ficha de metadatos del catálogo

## 5.1 Reglas generales

::: {custom-style="Norma"}
**Lo que dice la norma.** «Todo catálogo institucional deberá contar con los siguientes metadatos»: identificador, nombre oficial, descripción y propósito, propietario, custodio, clasificación, sistemas consumidores, frecuencia de actualización, versión vigente, fecha de última actualización y nivel de acceso (artículo 8, fracciones I a XI, de los Lineamientos). El Transitorio CUARTO pide estos mismos metadatos al registrar los catálogos existentes.
:::

1. Cada lista tiene una ficha. Un área con varias listas presenta una ficha por lista.
2. La ficha describe la lista. No incluye el contenido de la lista ni datos personales.
3. El propietario, el custodio y la clasificación que anota el área son propuestas. El Comité formaliza al propietario y al custodio al aprobar el catálogo (art. 12) y determina si es estratégico u operativo (art. 5, último párrafo). La DGETD propone el tipo de catálogo (art. 5 fr. I a IV) en el dictamen técnico (sección 8.1).
4. Como criterio operativo, la DGETD recibe y da trámite a todo registro que contiene el área que registra ([A1]{custom-style="Clave"}), el nombre oficial ([B2]{custom-style="Clave"}) y la descripción ([B3]{custom-style="Clave"}). Los demás metadatos pueden ir «por confirmar» y la DGETD los completa con el área. El registro queda completo cuando el área confirma la ficha (sección 7.1). Si ese registro se tiene por presentado en tiempo para el Transitorio CUARTO está por confirmar (PR-CAT-04, sección 6.9).
5. Un metadato que acepta «por confirmar» y llega vacío se registra con el valor «Por confirmar».
6. Los nombres técnicos se escriben en minúsculas, con palabras unidas por guion bajo (*snake_case*), sin acentos ni eñe y con un máximo de 30 caracteres. Los usan el formulario en línea, la plantilla de Excel y la lista de SharePoint «Inventario de catálogos».

::: {custom-style="Compromiso"}
**Compromiso DGETD.** La DGETD prellena en la ficha lo que ya conoce de la lista y la envía al área para que la confirme. La DGETD no vuelve a solicitar al área un dato que ya entregó en el registro.
:::

## 5.2 Tipos de dato

| Tipo | Regla |
|------------------|----------------------------------------------------------------------|
| Texto | Una línea, sin saltos. Codificación UTF-8. Longitud máxima de 255 caracteres, salvo que la ficha indique una menor. |
| Texto largo | Admite saltos de línea. La longitud máxima la indica cada metadato. |
| Opción | Un solo valor de una lista cerrada de valores permitidos (capítulo 8). |
| Área | Un valor de la lista oficial de áreas y órganos. No se escribe a mano. |
| Persona | Nombre completo, puesto, correo institucional y extensión (sección 5.5). |
| Fecha (mes) | Año y mes con el formato AAAA-MM de la norma ISO 8601. Si se conoce el día, AAAA-MM-DD. |
| Fecha | Año, mes y día con el formato AAAA-MM-DD de la norma ISO 8601. |
| Sí o no | Casilla que se marca o no se marca. |

: Tipos de dato de la ficha

## 5.3 Los 11 metadatos del artículo 8

Las tablas 5.3.a y 5.3.b describen los mismos 11 metadatos. La primera fija el nombre técnico, el tipo, la obligatoriedad y quién llena cada uno; la segunda, su contenido y la regla de validación. El número de cada metadato coincide con la fracción del art. 8. La fracción XI se cubre con dos datos: el nivel de acceso (11a) y la presencia de datos personales (11b). En la columna «Quién lo llena», el propietario, el custodio y la clasificación que anota el área son propuestas (sección 5.1).

| No. | Metadato (art. 8) y nombre técnico | Tipo y longitud máxima | Obligatorio | Quién lo llena |
|--------|--------------------------------|------------------|--------------------------|----------------|
| 1 | Identificador del catálogo [id_catalogo]{custom-style="Clave"} | Texto, 9 (10 con 5 dígitos) | Sí; lo asigna la DGETD | DGETD |
| 2 | Nombre oficial [nombre_oficial]{custom-style="Clave"} | Texto, 200 | Sí | Área |
| 3 | Descripción y propósito [descripcion]{custom-style="Clave"} | Texto largo, 1,000 | Sí | Área |
| 4 | Propietario [propietario]{custom-style="Clave"} | Área | Sí; acepta «por confirmar» | Área |
| 5 | Custodio [custodio]{custom-style="Clave"} | Área | Sí; acepta «por confirmar» | Área |
| 6 | Clasificación [clasificacion]{custom-style="Clave"} | Opción | Sí; acepta «por confirmar» | Área y DGETD |
| 7 | Sistemas consumidores [sistemas_consumidores]{custom-style="Clave"} | Texto largo, 2,000 | Sí; acepta «por confirmar» | Área y DGETD |
| 8 | Frecuencia de actualización [frecuencia]{custom-style="Clave"} | Opción | Sí; acepta «por confirmar» | Área |
| 9 | Versión vigente [version_vigente]{custom-style="Clave"} | Texto, 20 | Sí; acepta «por confirmar» | Área y DGETD |
| 10 | Fecha de última actualización [fecha_actualizacion]{custom-style="Clave"} | Fecha (mes) | Sí; acepta «por confirmar» | Área y DGETD |
| 11a | Nivel de acceso [nivel_acceso]{custom-style="Clave"} | Opción | Sí; acepta «por confirmar» | Área |
| 11b | Datos personales [datos_personales]{custom-style="Clave"} | Opción | Sí | Área |

: Tabla 5.3.a. Metadatos del art. 8: nombre técnico, tipo y responsable

| No. | Metadato | Descripción | Valores permitidos o regla de validación |
|--------|--------------------|----------------------------|--------------------------------------------|
| 1 | Identificador del catálogo | Clave única que identifica al catálogo en el OAJ. | Formato y reglas del capítulo 6. Única en el inventario. No cambia ni se reutiliza. |
| 2 | Nombre oficial | Denominación completa de la lista. | Sin siglas. Si el área usa otro nombre, se anota entre paréntesis. Si la lista no tiene nombre formal, el área propone uno. No puede quedar vacío. |
| 3 | Descripción y propósito | Qué contiene la lista y para qué se usa. | De 2 a 4 oraciones: de qué es la lista y qué trámite, reporte o decisión depende de ella. No puede quedar vacío. |
| 4 | Propietario | Área con autoridad sobre el contenido: decide qué entra, qué sale y con qué reglas. | Valor de la lista oficial de áreas y órganos. Viene marcada el área que registra. Si el contenido deriva de la función jurisdiccional, es el área administrativa competente (art. 4 fr. XVII). |
| 5 | Custodio | Área que mantiene la lista al día: da de alta, corrige y da de baja. | Valor de la lista oficial de áreas y órganos, con una persona de contacto (sección 5.5). |
| 6 | Clasificación | Tipo de catálogo conforme al art. 5. | Valores de la sección 8.1. El área propone ([C3]{custom-style="Clave"}); la DGETD revisa y registra la clasificación propuesta ([G4]{custom-style="Clave"}), que es la que queda en la ficha. |
| 7 | Sistemas consumidores | Sistemas, aplicaciones, archivos o reportes que usan la lista, dentro y fuera del área. | Un elemento por línea. Incluye hojas de cálculo y tableros de otras áreas que copian la lista. Si el área marca la casilla de la sección 5.5, la DGETD completa la lista con las áreas de sistemas ([G6]{custom-style="Clave"}). |
| 8 | Frecuencia de actualización | Cada cuánto se agrega, quita o corrige algo en la lista, según lo que ocurre hoy. | Valores de la sección 8.3. Con «Cada vez que ocurre un cambio» se indica qué hecho lo dispara (sección 5.5). |
| 9 | Versión vigente | Número o código de la versión actual. | Si el área no maneja versiones, la DGETD registra 1.0 con la fecha del registro ([G7]{custom-style="Clave"}). Si las maneja, se registra la versión que indique el área. |
| 10 | Fecha de última actualización | Fecha del último cambio en la estructura o el contenido. | No puede ser posterior a la fecha de recepción. Basta año y mes. Si la lista está en un sistema y el área marca la casilla, la DGETD obtiene la fecha exacta. |
| 11a | Nivel de acceso | Quién puede consultar la lista. | Valores de la sección 8.4. Ante la duda, se elige el valor más restrictivo. |
| 11b | Datos personales | Si la lista contiene datos personales, como nombres, RFC, CURP, domicilios particulares o teléfonos. | Valores de la sección 8.5. El área no entrega los datos; solo informa si existen. |

: Tabla 5.3.b. Metadatos del art. 8: descripción y regla de validación

## 5.4 Metadatos complementarios de gestión

El registro necesita datos que no forman parte del art. 8: quién registra, cómo se identifica el trámite y en qué estatus está. La DGETD los conserva en el inventario junto con la ficha.

| ID | Metadato y nombre técnico | Obligatorio · quién lo llena | Tipo, longitud y regla de validación |
|--------|------------------------------|------------------|--------------------------------------------|
| [A1]{custom-style="Clave"} | Área que registra [area_registra]{custom-style="Clave"} | Sí · área | Área. Valor de la lista oficial de áreas y órganos. |
| [A2]{custom-style="Clave"} | Persona enlace [enlace]{custom-style="Clave"} | Sí · área | Persona. Subcampos de la sección 5.5. Es la persona de contacto del registro. |
| [A3]{custom-style="Clave"} | Persona titular que valida [titular]{custom-style="Clave"} | Sí · área | Persona. Nombre y puesto. Recibe copia del acuse. |
| [B1b]{custom-style="Clave"} | Clave interna actual [clave_interna]{custom-style="Clave"} | No · área | Texto, 50. Se conserva como referencia. No sustituye a la clave de catálogo. |
| [C2b]{custom-style="Clave"} | Preferencia de custodia [preferencia_custodia]{custom-style="Clave"} | No · área | Opción. Sí, No o No sé. Solo registra el interés del área; el custodio lo formaliza el Comité al aprobar el catálogo (arts. 12 y 17). |
| [G1]{custom-style="Clave"} | Folio de registro [folio_registro]{custom-style="Clave"} | Sí · DGETD | Texto, 12 (13 con 5 dígitos). Formato y reglas de la sección 6.2. |
| [G3]{custom-style="Clave"} | Fecha de recepción [fecha_recepcion]{custom-style="Clave"} | Sí · DGETD | Fecha. Día en que llega el registro por cualquiera de los canales. |
| [G5]{custom-style="Clave"} | Alcance propuesto [alcance]{custom-style="Clave"} | Sí · DGETD | Opción. Valores de la sección 8.2. Lo determina el Comité al aprobar (art. 5). |
| [G8]{custom-style="Clave"} | Estatus del registro [estatus_registro]{custom-style="Clave"} | Sí · DGETD | Opción. Valores y transiciones de la sección 7.1. |
| [G9]{custom-style="Clave"} | Estatus en el inventario [estatus_inventario]{custom-style="Clave"} | Sí · DGETD | Opción. Valores y transiciones de la sección 7.2. |
| [G10]{custom-style="Clave"} | Observaciones [observaciones]{custom-style="Clave"} | No · DGETD | Texto largo, 2,000. En un «Duplicado», anota la clave del catálogo con el que coincide. |
| [G11]{custom-style="Clave"} | Confirmación del área [confirmacion_area]{custom-style="Clave"} | Al confirmar · área | Texto, 255. Nombre de quien confirma y fecha (AAAA-MM-DD). |

: Tabla 5.4. Metadatos complementarios de gestión

Los campos opcionales de diagnóstico de F-CAT-01 (sección F) no forman parte de la ficha. Sirven para preparar el plan de adecuación del Transitorio QUINTO.

| ID | Dato y nombre técnico | Tipo y longitud | Valores permitidos |
|--------|------------------------------|--------------|------------------------------------------------|
| [F1]{custom-style="Clave"} | Dónde vive la lista [ubicacion_lista]{custom-style="Clave"} | Opción | En un sistema o base de datos · En una hoja de cálculo en carpeta compartida · En una hoja de cálculo en el equipo de una persona · En papel · Otro |
| [F2]{custom-style="Clave"} | Tamaño aproximado [tamano_aproximado]{custom-style="Clave"} | Opción | Menos de 50 · De 50 a 500 · De 501 a 5,000 · Más de 5,000 · No sé |
| [F3]{custom-style="Clave"} | Clave de cada renglón [clave_elementos]{custom-style="Clave"} | Opción | Sí, y la clave tiene significado (incluye año, lugar, materia u otro dato) · Sí, y es un número sin significado · No tiene clave · No sé |
| [F4]{custom-style="Clave"} | Listas parecidas [listas_parecidas]{custom-style="Clave"} | Texto, 255 | Texto libre. |
| [F5]{custom-style="Clave"} | Problema actual [problema_actual]{custom-style="Clave"} | Texto largo, 1,000 | Texto libre. |

: Tabla 5.4.b. Datos opcionales de diagnóstico (no forman parte de la ficha)

## 5.5 Subcampos y casillas

| Metadato | Subcampo o casilla | Nombre técnico | Tipo y longitud |
|------------------|----------------------------|--------------------------------|----------------------|
| Persona enlace ([A2]{custom-style="Clave"}) | Nombre completo · puesto · correo institucional · extensión | [enlace_nombre]{custom-style="Clave"}, [enlace_puesto]{custom-style="Clave"}, [enlace_correo]{custom-style="Clave"}, [enlace_extension]{custom-style="Clave"} | Texto: 150, 150, 254 y 10 |
| Persona titular ([A3]{custom-style="Clave"}) | Nombre completo · puesto | [titular_nombre]{custom-style="Clave"}, [titular_puesto]{custom-style="Clave"} | Texto: 150 y 150 |
| Custodio ([C2]{custom-style="Clave"}) | Persona de contacto del custodio | [custodio_contacto]{custom-style="Clave"} | Persona |
| Sistemas consumidores ([D1]{custom-style="Clave"}) | «No conozco todos. Que la DGETD complete la lista.» | [sistemas_por_dgetd]{custom-style="Clave"} | Sí o no |
| Frecuencia ([D2]{custom-style="Clave"}) | Hecho que dispara el cambio, si la frecuencia es «Cada vez que ocurre un cambio» | [frecuencia_disparador]{custom-style="Clave"} | Texto, 255 |
| Fecha de última actualización ([D4]{custom-style="Clave"}) | «Está en un sistema; que la DGETD obtenga la fecha.» | [fecha_en_sistema]{custom-style="Clave"} | Sí o no |

: Tabla 5.5. Subcampos y casillas de la ficha

::: {custom-style="Pendiente"}
**Por confirmar.** (1) Las longitudes máximas son una propuesta de la DGETD; se verifican contra el formulario en línea, la plantilla de Excel y la lista de SharePoint durante el piloto. (2) Falta definir la fuente de la lista oficial de áreas y órganos que usan [A1]{custom-style="Clave"}, [C1]{custom-style="Clave"} y [C2]{custom-style="Clave"}, y quién la mantiene.
:::

# 6. Clave de catálogo y folio de registro

::: {custom-style="Norma"}
**Lo que dice la norma.** Todo catálogo tiene un «código único que identifica al catálogo dentro del Órgano» (artículo 8, fracción I, de los Lineamientos). Los catálogos usan «identificadores únicos y estables a lo largo del tiempo» (art. 25 fr. I). Para los registros de cada catálogo, el art. 7 fr. I exige persistencia, unicidad global y neutralidad semántica; este estándar aplica los mismos criterios a la clave de catálogo.
:::

## 6.1 Clave de catálogo

1. **Formato.** La clave se forma con el prefijo [CAT-]{custom-style="Clave"} y un correlativo de 4 dígitos con ceros a la izquierda: de [CAT-0001]{custom-style="Clave"} a [CAT-9999]{custom-style="Clave"}. Se escribe en mayúsculas, con guion (carácter U+002D) y sin espacios. Expresión de validación: `^CAT-([0-9]{4}|[1-9][0-9]{4})$`.
2. **Asignación.** La DGETD asigna la clave al recibir el registro, en el orden en que llegan los registros, y la comunica en el acuse junto con el folio. El área no propone ni elige la clave.
3. **Neutralidad.** La clave no contiene siglas de área, fechas, materias, lugares ni ningún otro significado. El número solo indica el orden de asignación; ningún sistema deriva información de él.
4. **Persistencia.** La clave no cambia aunque el catálogo cambie de nombre, de propietario, de custodio o de estatus en el inventario.
5. **No reutilización.** La clave de un catálogo retirado, duplicado o de uso local no se asigna a otro catálogo.
6. **Unicidad.** La DGETD asigna las claves desde un único consecutivo en el inventario. Una lista registrada por error dos veces conserva ambas claves; una de ellas pasa a «Duplicado» (sección 7.2).
7. **Crecimiento.** Después de [CAT-9999]{custom-style="Clave"} sigue [CAT-10000]{custom-style="Clave"}, sin renumerar las claves anteriores. Los sistemas guardan la clave como texto, con el prefijo y los ceros a la izquierda, y aceptan 5 dígitos.
8. **Claves internas.** La clave interna que el área ya usa ([B1b]{custom-style="Clave"}) se conserva como referencia y no sustituye a la clave de catálogo.

::: {custom-style="Compromiso"}
**Compromiso DGETD.** La DGETD asigna la clave de catálogo y envía al área un acuse con el folio de registro y la fecha de recepción.
:::

| Ejemplo | Resultado | Motivo |
|--------------------|----------------|------------------------------------------------------|
| [CAT-0042]{custom-style="Clave"} | Válida | Prefijo y 4 dígitos. |
| [CAT-10000]{custom-style="Clave"} | Válida | Primera clave de 5 dígitos, después de [CAT-9999]{custom-style="Clave"}. |
| [CAT-DGRH-01]{custom-style="Clave"} | No válida | Contiene siglas de área. Si el área cambia de nombre o la lista cambia de área, la clave dejaría de ser correcta, y no puede cambiar. Además, no tiene 4 dígitos. |
| [CAT-2027-0042]{custom-style="Clave"} | No válida | Codifica el año de registro. |
| [CAT-PEN-0042]{custom-style="Clave"} | No válida | Codifica una materia. |
| [CAT-42]{custom-style="Clave"} | No válida | Tiene menos de 4 dígitos. Se escribe [CAT-0042]{custom-style="Clave"}. |
| [cat-0042]{custom-style="Clave"} | No válida | Está en minúsculas. |
| [CAT 0042]{custom-style="Clave"} | No válida | Tiene un espacio en lugar del guion. |
| [CAT-09999]{custom-style="Clave"} | No válida | Tiene 5 dígitos con cero a la izquierda; equivale a [CAT-9999]{custom-style="Clave"}. |
| [RC-2027-0118]{custom-style="Clave"} | No válida como clave | Es un folio de registro: identifica un trámite, no un catálogo. |

: Ejemplos de claves de catálogo válidas y no válidas

::: {custom-style="Pendiente"}
**Por confirmar.** El consecutivo de claves se genera de forma automática en la lista de SharePoint solo si se confirma que Power Automate está habilitado. Si no lo está, la DGETD asigna la clave de forma manual desde el mismo consecutivo, y el acuse deja de ser inmediato.
:::

## 6.2 Folio de registro

1. **Formato.** El folio se forma con el prefijo [RC-]{custom-style="Clave"}, el año de recepción con 4 dígitos y un correlativo anual de 4 dígitos con ceros a la izquierda. Expresión de validación: `^RC-[0-9]{4}-([0-9]{4}|[1-9][0-9]{4})$`.
2. **Qué identifica.** El folio identifica el trámite de registro, no al catálogo. Cada envío de registro recibe un folio.
3. **Correlativo anual.** El correlativo empieza en 0001 con el primer registro recibido en cada año. Si en un año se rebasan 9999 trámites, el correlativo pasa a 5 dígitos sin renumerar.
4. **Relación con la clave.** Un catálogo conserva su clave aunque tenga varios folios; por ejemplo, el del registro inicial y el de una corrección posterior.
5. **Carga por plantilla.** Una plantilla de Excel con varias listas genera un folio y una clave por cada lista, porque cada lista es un registro.
6. **Año en el folio.** El folio sí contiene el año. No contraviene la neutralidad del capítulo 10 porque no identifica a un catálogo ni a un elemento, y ningún sistema consumidor lo usa como referencia.

| Ejemplo | Resultado | Motivo |
|--------------------|----------------|------------------------------------------------------|
| [RC-2027-0118]{custom-style="Clave"} | Válido | Trámite 118 recibido en 2027. |
| [RC-2026-0001]{custom-style="Clave"} | Válido | Primer trámite recibido en 2026. |
| [RC-27-0118]{custom-style="Clave"} | No válido | El año tiene 2 dígitos. |
| [RC-2027-118]{custom-style="Clave"} | No válido | El correlativo tiene menos de 4 dígitos. |
| [CAT-0042]{custom-style="Clave"} | No válido como folio | Es una clave de catálogo. |

: Ejemplos de folios de registro válidos y no válidos

## 6.3 Comparación entre clave y folio

| Característica | Clave de catálogo | Folio de registro |
|----------------------------|----------------------------------|----------------------------------|
| Identifica | Al catálogo | Al trámite de registro |
| Formato | [CAT-NNNN]{custom-style="Clave"} | [RC-AAAA-NNNN]{custom-style="Clave"} |
| Cuántos tiene un catálogo | Una | Uno o más |
| Contiene significado | No | Sí: el año de recepción |
| Cambia | Nunca | Cada trámite tiene el suyo |
| Quién lo asigna | DGETD | DGETD |

: Diferencias entre la clave de catálogo y el folio de registro

# 7. Estatus

Un catálogo registrado tiene dos estatus independientes. El estatus del registro indica en qué paso está el trámite identificado con un folio. El estatus en el inventario indica la situación de la lista dentro del inventario que lleva la DGETD con las listas registradas conforme al Transitorio CUARTO de los Lineamientos. Los catálogos autorizados (artículo 4, fracción IV) integran el inventario institucional de catálogos autorizados que el artículo 14, fracción I, encarga a la DGETD. Las listas con estatus «Registrado», «En dictamen», «Uso local» o «Duplicado» no son catálogos autorizados (vacío V4). Una transición que no aparece en las tablas de este capítulo no está permitida.

## 7.1 Estatus del registro

| Valor | Significado |
|--------------------|--------------------------------------------------------------------------|
| Recibido | Llegó el registro; se envió acuse con folio y clave. |
| En revisión | La DGETD revisa, prellena lo que conoce y, si falta algo, contacta al enlace. |
| Ficha enviada | La DGETD envió la ficha prellenada para que el área la confirme. |
| Confirmado | El área confirmó la ficha. El registro está completo. |

: Valores del estatus del registro ([G8]{custom-style="Clave"})

| De | A | Condición | Quién la ejecuta |
|--------------------|--------------------|------------------------------------------|----------------------|
| (registro nuevo) | Recibido | Llega un registro con área, nombre y descripción. Se asignan folio y clave y se envía el acuse. | DGETD |
| Recibido | En revisión | La DGETD inicia la revisión y el prellenado. | DGETD |
| En revisión | Ficha enviada | La ficha está prellenada y los datos faltantes se resolvieron con el enlace o quedaron «por confirmar». | DGETD |
| Ficha enviada | En revisión | El área pide corregir la ficha antes de confirmarla. | DGETD, a solicitud del área |
| Ficha enviada | Confirmado | El área confirma la ficha y anota nombre y fecha en [G11]{custom-style="Clave"}. | Área |

: Transiciones permitidas del estatus del registro

1. «Confirmado» es el estatus final de un folio. Una corrección posterior a la confirmación se presenta como un registro nuevo, con folio nuevo y la misma clave de catálogo.
2. Ningún folio regresa a «Recibido».

::: {custom-style="Compromiso"}
**Compromiso DGETD.** Cada bloque de áreas tiene una persona de contacto con nombre en la DGETD. Las correcciones a la ficha no tienen costo para el área hasta el dictamen.
:::

::: {custom-style="Pendiente"}
**Por definir.** (1) Plazo para enviar la ficha de confirmación desde la recepción: [plazo por definir según capacidad de la DGETD]{custom-style="Marcador"}. (2) Plazo de respuesta a dudas: [plazo por definir según capacidad de la DGETD]{custom-style="Marcador"}. Mientras no se definan, no forman parte del compromiso de la DGETD.
:::

## 7.2 Estatus en el inventario

| Valor | Significado |
|--------------------|--------------------------------------------------------------------------|
| Registrado | Está en el inventario por el registro del Transitorio CUARTO. Aún no es catálogo autorizado. |
| En dictamen | La DGETD analiza si cumple los criterios del art. 6 y prepara el dictamen. |
| Autorizado | Aprobado por el Comité y publicado en la Plataforma de Acceso a la Información Institucional (art. 4 fr. IV). |
| En adecuación | Autorizado o en proceso, con ajustes pendientes conforme al plan del Transitorio QUINTO. |
| Uso local | No cumple los criterios del art. 6 para ser institucional. Queda documentado y lo sigue llevando el área. |
| Duplicado | Repite otro catálogo registrado; se indica la clave del catálogo con el que coincide. |
| Retirado | Se dejó de usar de forma controlada. Su clave no se reutiliza. |

: Valores del estatus en el inventario ([G9]{custom-style="Clave"})

| De | A | Condición | Quién la ejecuta |
|--------------------|--------------------|------------------------------------------|----------------------|
| (registro nuevo) | Registrado | La DGETD recibe el registro y asigna la clave. | DGETD |
| Registrado | En dictamen | El registro está «Confirmado». La DGETD inicia el análisis de los criterios del art. 6. | DGETD |
| Registrado | Duplicado | El registro está «Confirmado» y la lista repite otro catálogo registrado. | DGETD, con aviso a las áreas involucradas |
| Registrado | Retirado | El área informa que la lista dejó de usarse. | DGETD, a solicitud del área |
| En dictamen | Autorizado | El Comité aprueba el catálogo (art. 12) y el catálogo se publica (art. 4 fr. IV). | DGETD, tras el acuerdo del Comité |
| En dictamen | En adecuación | Cumple el art. 6 y requiere ajustes conforme al plan del Transitorio QUINTO. | DGETD |
| En dictamen | Uso local | El dictamen concluye que no cumple los criterios del art. 6. | DGETD |
| En dictamen | Duplicado | El dictamen identifica que repite otro catálogo registrado. | DGETD, con aviso a las áreas involucradas |
| En adecuación | Autorizado | Concluyen los ajustes, el Comité aprueba y el catálogo se publica. | DGETD, tras el acuerdo del Comité |
| Autorizado | En adecuación | El plan del Transitorio QUINTO asigna ajustes a un catálogo ya autorizado. | DGETD |
| Autorizado o En adecuación | Retirado | Retiro controlado (art. 9 fr. VIII). | Según PR-CAT-01 |
| Uso local | En dictamen | Cambian las condiciones de uso; por ejemplo, otro sistema empieza a usar la lista. | DGETD, de oficio o a solicitud del área |
| Uso local | Retirado | El área informa que la lista dejó de usarse. | DGETD, a solicitud del área |
| Duplicado | Retirado | La lista se sustituye por el catálogo con el que coincide. | DGETD, con acuerdo del área |

: Transiciones permitidas del estatus en el inventario

1. «Retirado» es un estatus final. La clave del catálogo retirado no se reutiliza.
2. En un «Duplicado», la DGETD anota en [G10]{custom-style="Clave"} la clave del catálogo con el que coincide. La DGETD determina, con las áreas involucradas, cuál de los dos registros se marca como «Duplicado».
3. Cada cambio de estatus queda en el inventario con su fecha y la persona que lo ejecutó.

::: {custom-style="Pendiente"}
**Por confirmar.** (1) Si la DGETD puede asignar «Uso local» por sí misma o si requiere conocimiento del Comité, dado que el art. 6 fr. I deja algunos casos «a juicio del Comité». (2) Si un catálogo que concluye su adecuación pasa a «Autorizado» con o sin acuerdo del Comité (vacío V4). (3) Quién solicita y quién aprueba el retiro de un catálogo autorizado (vacío V10); se define en PR-CAT-01. (4) Si una lista retirada que vuelve a usarse recupera su clave o se registra con una nueva. (5) Si un registro puede pasar a «Confirmado» con metadatos que siguen «por confirmar». (6) Qué ocurre si el área no confirma la ficha (vacío V12). (7) Ningún catálogo puede llegar a «Autorizado» mientras no se verifique que la Plataforma de Acceso a la Información Institucional opera (vacío V2).
:::

# 8. Valores permitidos

Este capítulo fija los valores permitidos de los metadatos que se responden con una opción. Un valor que no aparece en estas tablas se rechaza. La ficha guarda el valor tal como se escribe en la columna «Valor».

## 8.1 Clasificación

::: {custom-style="Norma"}
**Lo que dice la norma.** Los catálogos institucionales se clasifican en catálogos de entidades, de clasificación, de parámetros y de relación (artículo 5, fracciones I a IV, de los Lineamientos). La clasificación es un metadato obligatorio (art. 8 fr. VI).
:::

| Valor | Art. 5 | Pregunta en F-CAT-01 | Ejemplos |
|------------------|----------|----------------------------------------|----------------------------------|
| Entidades | Fr. I | Una lista de personas, lugares o cosas de la institución | Órganos jurisdiccionales, inmuebles, cargos |
| Clasificación | Fr. II | Una lista de opciones para clasificar información | Tipos de documento, sentidos de resolución, entidades federativas |
| Parámetros | Fr. III | Valores de configuración que usa un sistema | Plazos, montos, porcentajes, umbrales |
| Relación | Fr. IV | Una tabla que une dos listas | Qué órgano pertenece a qué circuito |
| Por confirmar | — | No estoy seguro | — |

: Valores permitidos de [clasificacion]{custom-style="Clave"}

1. Cada catálogo tiene un solo valor de clasificación.
2. El área propone un valor ([C3]{custom-style="Clave"}). La DGETD revisa la respuesta y registra la clasificación propuesta ([G4]{custom-style="Clave"}), que es la que queda en la ficha.
3. La DGETD propone el tipo de catálogo en el dictamen técnico. El Comité formaliza al propietario y al custodio al aprobar el catálogo (art. 12) y determina si es estratégico u operativo (art. 5, último párrafo; sección 8.2).

::: {custom-style="Pendiente"}
**Por confirmar.** Los Lineamientos no dicen quién fija el tipo de catálogo (art. 5 fr. I a IV): si basta la propuesta de la DGETD en el dictamen técnico o si el Comité la formaliza al aprobar el catálogo.
:::

## 8.2 Alcance

::: {custom-style="Norma"}
**Lo que dice la norma.** Los catálogos «podrán distinguirse en estratégicos» u «operativos o de alcance acotado». La clasificación de cada catálogo como estratégico u operativo «será determinada por el Comité al momento de su aprobación, a propuesta de la DGETD» (art. 5, último párrafo).
:::

| Valor | Cuándo se usa |
|----------------------------------|----------------------------------------------------------|
| Estratégico | Alto impacto institucional y transversalidad amplia (art. 5). |
| Operativo o de alcance acotado | Su uso se limita a procesos o sistemas específicos (art. 5). |
| Por determinar | La DGETD todavía no cuenta con información para proponer el alcance. |

: Valores permitidos de [alcance]{custom-style="Clave"}

El alcance no se pregunta al área. Lo propone la DGETD en [G5]{custom-style="Clave"} y lo determina el Comité.

::: {custom-style="Pendiente"}
**Por confirmar.** Los criterios objetivos para distinguir un catálogo estratégico de uno operativo (vacío V7). La DGETD los propone como parte de la metodología del dictamen técnico (F-CAT-04).
:::

## 8.3 Frecuencia de actualización

| Valor | Regla de uso |
|----------------------------------|----------------------------------------------------------|
| Cada vez que ocurre un cambio | La lista cambia cuando ocurre un hecho; por ejemplo, cuando se crea o se readscribe un órgano. Se anota el hecho en [frecuencia_disparador]{custom-style="Clave"}. |
| Diaria · Semanal · Mensual · Trimestral · Semestral · Anual | Periodicidad con la que la lista cambia en la práctica. |
| Casi nunca cambia | La lista no tiene periodicidad y sus cambios son excepcionales. |
| No hay una periodicidad definida | La lista cambia, sin un patrón identificable. |
| Por confirmar | El área no conoce la frecuencia. |

: Valores permitidos de [frecuencia]{custom-style="Clave"}

La frecuencia registrada describe lo que ocurre hoy, no lo que debería ocurrir.

::: {custom-style="Pendiente"}
**Por confirmar.** La frecuencia «establecida» con la que el custodio mantiene el catálogo (art. 16 fr. I) no la fija ningún artículo (vacío V8). Se propone fijarla en el dictamen técnico y formalizarla con la aprobación del Comité.
:::

## 8.4 Nivel de acceso

::: {custom-style="Norma"}
**Lo que dice la norma.** El nivel de acceso es la «clasificación de privacidad y restricciones de acceso conforme a la normativa aplicable» (art. 8 fr. XI). El acceso se controla con mecanismos de autenticación y autorización según la sensibilidad de la información (art. 23).
:::

| Valor | Descripción | Orden de restricción |
|------------------|----------------------------------------------------------|------------------|
| Pública | Cualquier persona puede consultarla. | 1 (menor) |
| Interna | Todo el personal del OAJ puede consultarla. | 2 |
| Restringida | Solo ciertas áreas o personas pueden consultarla. | 3 |
| Clasificada | Contiene información reservada o confidencial conforme a la normativa de transparencia. | 4 (mayor) |
| Por confirmar | No estoy seguro. | — |

: Valores permitidos de [nivel_acceso]{custom-style="Clave"}

1. Ante la duda entre dos valores, el área elige el de mayor orden de restricción.
2. Registrar una lista no la publica, cualquiera que sea su nivel de acceso.
3. Si la lista contiene información reservada o confidencial, el área la marca como «Clasificada». La DGETD no revisa esa clasificación, que se rige por la normativa de transparencia. Solo la usa para proteger la ficha en el inventario y, cuando la lista sea catálogo institucional, para que los controles de acceso del art. 23 correspondan a ella.

::: {custom-style="Pendiente"}
**Por confirmar.** (1) Estos valores son una propuesta de la DGETD. Deben alinearse con el Acuerdo General del OAJ en materia de transparencia, acceso a la información y protección de datos personales, con la unidad de transparencia competente, antes de la versión 1.0 de este estándar. (2) Si la instancia de transparencia participa en las listas «Clasificadas» y cómo; se confirma con ella.
:::

## 8.5 Datos personales

| Valor | Efecto en la ficha |
|------------------|----------------------------------------------------------------------|
| Sí | La lista contiene datos personales. La DGETD revisa con el área el nivel de acceso antes del dictamen. |
| No | La lista no contiene datos personales. |
| No sé | La DGETD revisa con el área si la lista contiene datos personales y su nivel de acceso antes del dictamen. |

: Valores permitidos de [datos_personales]{custom-style="Clave"}

1. El área no entrega los datos personales; solo informa si existen.
2. La respuesta no determina por sí sola el nivel de acceso. Una lista con datos personales cumple la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados y la normativa del OAJ que cita el art. 23.

# 9. Estructura mínima de los registros

## 9.1 Lo que ya fijan los Lineamientos

::: {custom-style="Norma"}
**Lo que dice la norma.** Todo catálogo institucional contiene, como mínimo, estos atributos por registro: identificador único; descripción; estatus de vigencia, que «podrá ser activo, inactivo u obsoleto»; fechas de vigencia (fecha de incorporación y, cuando aplique, inicio y fin de vigencia); metadatos de gestión (fecha de última actualización y persona responsable), y atributos específicos documentados en el diccionario de datos (artículo 7, fracciones I a VI, de los Lineamientos). El diccionario especifica para cada atributo nombre técnico, descripción, tipo de dato, longitud, restricciones, obligatoriedad y valores permitidos (art. 11).
:::

## 9.2 Lo que este estándar definirá

1. El nombre técnico, el tipo de dato y la longitud de cada atributo mínimo del art. 7, con la misma convención de nombres de la sección 5.1.
2. Las reglas de las fechas de vigencia: formato ISO 8601, relación entre fecha de incorporación, inicio y fin, y el tratamiento de una fecha de fin vacía.
3. La forma de identificar a la persona responsable de la última actualización (art. 7 fr. V).
4. Los requisitos mínimos de los atributos específicos en el diccionario de datos (F-CAT-03).
5. La definición de los estatus de vigencia y sus transiciones (sección 9.3).

## 9.3 Propuesta: estatus de vigencia de los registros

| Estatus | Definición propuesta | Uso en registros nuevos | Puede volver a «activo» |
|--------------|------------------------------------------------|------------------|------------------|
| Activo | El elemento existe y está vigente. | Sí | — |
| Inactivo | El elemento deja de usarse de forma temporal. Se conserva para consulta y para interpretar registros anteriores. Ejemplo ilustrativo: un inmueble que el OAJ deja de ocupar mientras se remodela. | No | Sí |
| Obsoleto | El elemento dejó de existir o se sustituyó de forma definitiva. Se conserva para interpretar registros anteriores. Si se sustituyó, se indica el identificador del elemento que lo sustituye. Ejemplo ilustrativo: un órgano que se fusionó con otro. | No | No |

: Propuesta de definición de los estatus de vigencia (art. 7 fr. III)

Los Lineamientos nombran los tres estatus, pero no los definen ni los distinguen (vacío V10). La tabla anterior es una propuesta de la DGETD para validar.

Reglas propuestas:

1. Transiciones permitidas: de activo a inactivo, de inactivo a activo, de activo a obsoleto y de inactivo a obsoleto. «Obsoleto» es final.
2. Un elemento nunca se borra del catálogo. Su identificador no se reutiliza, cualquiera que sea su estatus.
3. El cambio de estatus de un elemento es un cambio menor de contenido: el custodio lo registra en la bitácora (F-CAT-06) y no genera versión (capítulo 11).

## 9.4 Decisiones pendientes

::: {custom-style="Pendiente"}
**Por confirmar.** (1) Validar la propuesta de estatus de vigencia de la sección 9.3. (2) Cómo se identifica a la persona responsable de la última actualización sin publicar datos personales cuando el catálogo es público (art. 7 fr. V frente al art. 21). (3) Si las fechas de vigencia se registran por día o admiten solo mes y año en catálogos existentes.
:::

# 10. Identificador único de registro

## 10.1 Lo que ya fijan los Lineamientos

::: {custom-style="Norma"}
**Lo que dice la norma.** Cada registro de un catálogo tiene un «código alfanumérico único e inmutable» que cumple cuatro criterios: persistencia durante todo su ciclo de vida, unicidad global en el ámbito institucional del Órgano, neutralidad semántica («no deberá codificar información contextual como fechas, lugares u otra interpretación semántica») y formato estandarizado conforme a las especificaciones de la DGETD (artículo 7, fracción I, incisos a) a d), de los Lineamientos). Los catálogos usan identificadores únicos y estables a lo largo del tiempo (art. 25 fr. I).
:::

## 10.2 Lo que este estándar definirá

1. El formato estandarizado del inciso d): juego de caracteres, longitud y estructura.
2. El mecanismo que asegura la unicidad global en todo el OAJ, y no solo dentro de cada catálogo.
3. Quién asigna el identificador a cada nuevo elemento: la DGETD o el custodio con un mecanismo central.
4. La regla de no reutilización de identificadores de elementos inactivos u obsoletos.
5. El régimen de transición para los identificadores heredados que tienen significado (por ejemplo, una clave de órgano que incluye circuito y materia): tablas de equivalencia entre la clave anterior y la nueva, y un periodo de convivencia de ambas, conforme al plan del Transitorio QUINTO.

## 10.3 Decisiones pendientes

::: {custom-style="Pendiente"}
**Por confirmar.** (1) Si el identificador lleva un prefijo que indique el catálogo al que pertenece y si ese prefijo es compatible con la neutralidad semántica. (2) Si el identificador incluye un dígito verificador. (3) Si la asignación es central o por rangos asignados a cada custodio. (4) Cómo se relacionan el identificador de registro y la clave de catálogo en las referencias entre sistemas.
:::

# 11. Versionamiento

## 11.1 Lo que ya fijan los Lineamientos

::: {custom-style="Norma"}
**Lo que dice la norma.** Los cambios se distinguen en dos tipos. Los cambios estructurales mayores modifican la estructura, los atributos o las reglas de negocio del catálogo y requieren una nueva versión formal. Los cambios menores de contenido (altas, bajas o modificaciones de elementos que no alteran la estructura) los registra el custodio en la bitácora, «sin requerir nueva versión ni intervención del Comité». Todo cambio estructural mayor se solicita por el propietario a la DGETD, se evalúa por su impacto en los sistemas consumidores, recibe un nuevo número de versión «siguiendo el esquema establecido por la DGETD», se documenta y se comunica a todos los sistemas consumidores con anticipación suficiente (artículo 13, fracciones I a V, de los Lineamientos). El versionamiento asigna identificadores únicos a cada versión (art. 4 fr. XIX).
:::

## 11.2 Propuesta: esquema MAYOR.MENOR

La DGETD propone identificar cada versión con dos números enteros separados por un punto: MAYOR.MENOR. El esquema solo cuenta cambios estructurales mayores en el sentido del art. 13; los cambios menores de contenido no modifican el número de versión.

| Número | Se incrementa cuando | Efecto en los sistemas consumidores |
|--------------|------------------------------------------------|------------------------------------|
| MAYOR | El cambio estructural mayor obliga a los sistemas consumidores a adaptarse: se elimina o renombra un atributo, cambia su tipo, se reduce su longitud o cambia una regla de negocio que altera el significado de los valores. El número MENOR vuelve a 0. | Deben adaptarse antes de la fecha de entrada en vigor de la versión. |
| MENOR | El cambio estructural mayor no obliga a los sistemas consumidores a adaptarse: se agrega un atributo opcional o se amplía la longitud de un atributo. | Pueden seguir operando sin cambios. |
| Sin cambio | Cambio menor de contenido: alta, baja o modificación de un elemento, incluido el cambio de su estatus de vigencia. Se registra en la bitácora (F-CAT-06) y se actualiza la fecha de última actualización (art. 8 fr. X). | No se requiere aviso formal de versión. |

: Propuesta de esquema de versiones

Los dos incrementos son versiones formales: ambos siguen las fracciones I a V del art. 13. La diferencia entre MAYOR y MENOR comunica a los sistemas consumidores si tienen que adaptarse.

| Cambio (ejemplo ilustrativo en el Catálogo de inmuebles del OAJ) | Tipo de cambio (art. 13) | Versión |
|----------------------------------------------|--------------------------|--------------------------|
| Alta de un inmueble nuevo | Menor de contenido | 1.0, sin cambio |
| Corrección del domicilio de un inmueble | Menor de contenido | 1.0, sin cambio |
| Un inmueble pasa a «inactivo» | Menor de contenido | 1.0, sin cambio |
| Se agrega el atributo opcional «superficie» | Estructural mayor | 1.0 a 1.1 |
| Se amplía la longitud del atributo «domicilio» | Estructural mayor | 1.1 a 1.2 |
| Se elimina el atributo «uso» | Estructural mayor | 1.2 a 2.0 |
| Cambia la regla que define qué inmueble se considera ocupado | Estructural mayor | 2.0 a 3.0 |

: Ejemplos de aplicación del esquema propuesto

## 11.3 Lo que este estándar definirá

1. El esquema de versiones definitivo, a partir de la propuesta de la sección 11.2.
2. La versión inicial de los catálogos existentes: 1.0 cuando el área no maneja versiones ([D3]{custom-style="Clave"}, [G7]{custom-style="Clave"}) y la regla de conversión cuando sí las maneja.
3. Cómo se identifica el estado del contenido entre dos versiones, ya que los cambios menores no generan versión.
4. Qué se documenta de cada versión formal y dónde se conserva el historial de versiones.

## 11.4 Decisiones pendientes

::: {custom-style="Pendiente"}
**Por confirmar.** (1) Validar el esquema MAYOR.MENOR. (2) Los días de «anticipación suficiente» del art. 13 fr. V; se fijan en PR-CAT-01. (3) Quién evalúa el impacto, documenta y comunica el cambio, porque las fracciones II, IV y V del art. 13 no lo dicen, y si el Comité interviene en los cambios estructurales mayores (vacío V5). (4) Si las versiones que ya usa un área (por ejemplo, v2.3) se conservan o se convierten al esquema institucional durante la adecuación.
:::

# 12. Publicación y formatos abiertos

## 12.1 Lo que ya fijan los Lineamientos

::: {custom-style="Norma"}
**Lo que dice la norma.** Todo catálogo autorizado se publica en la Plataforma de Acceso a la Información Institucional junto con sus metadatos y su diccionario de datos, salvo los que contengan información reservada o confidencial (artículo 21 de los Lineamientos). Los catálogos se publican «en formatos estructurados abiertos que faciliten su lectura automática e interoperabilidad, conforme a los estándares técnicos establecidos por la DGETD» (art. 22). Los catálogos usan estándares técnicos abiertos y ampliamente adoptados (art. 25 fr. IV).
:::

## 12.2 Lo que este estándar definirá

1. Los formatos de publicación obligatorios entre los formatos estructurados abiertos; por ejemplo, CSV o JSON.
2. La codificación de caracteres, el separador, el formato de fechas y la representación de valores vacíos.
3. La convención de nombres de los archivos publicados, con la clave de catálogo y la versión.
4. Cómo se publican juntos el catálogo, su ficha de metadatos y su diccionario de datos.
5. La fecha de corte de cada publicación y cómo se reflejan los cambios menores de contenido en lo publicado.
6. Si la bitácora de cambios menores se publica para consulta.

## 12.3 Decisiones pendientes

::: {custom-style="Pendiente"}
**Por confirmar.** (1) No está verificado que la Plataforma de Acceso a la Información Institucional opere (vacío V2); este estándar no fija reglas que dependan de ella hasta que se verifique. (2) Cómo se publica un catálogo reservado o confidencial, si un catálogo autorizado se define como «publicado» (art. 4 fr. IV frente a los arts. 21 y 23; vacío V6). (3) Qué formatos se adoptan como obligatorios.
:::

# 13. Interoperabilidad y catálogos de relación

## 13.1 Lo que ya fijan los Lineamientos

::: {custom-style="Norma"}
**Lo que dice la norma.** Los catálogos se diseñan con cuatro principios: identificadores únicos y estables, uso de catálogos existentes antes de crear nuevos, relaciones explícitas entre catálogos cuando sea necesario y estándares técnicos abiertos (artículo 25, fracciones I a IV, de los Lineamientos). Los catálogos de relación contienen datos que establecen vínculos entre dos o más catálogos institucionales (art. 5 fr. IV).
:::

## 13.2 Lo que este estándar definirá

1. La regla para que un catálogo haga referencia a otro: por el identificador único del registro y la clave de catálogo, no por la descripción.
2. La estructura mínima de un catálogo de relación: identificador de cada lado de la relación y fechas de vigencia de la relación. Ejemplo ilustrativo: qué órgano pertenece a qué circuito y desde cuándo.
3. El criterio para decidir cuándo una relación se publica como catálogo de relación y cuándo como atributo de un catálogo de entidades.
4. La verificación contra el inventario de que no existe un catálogo que satisfaga la necesidad antes de crear uno nuevo (art. 25 fr. II).
5. Cómo guardan los sistemas consumidores la referencia a un valor de catálogo.

## 13.3 Decisiones pendientes

::: {custom-style="Pendiente"}
**Por confirmar.** (1) El criterio de la sección 13.2, punto 3. (2) Si los catálogos de relación tienen identificador único propio por registro o se identifican por la combinación de los identificadores que relacionan. (3) La relación con las interfaces de programación de aplicaciones (API) que la DGETD «promoverá» (art. 26); su desarrollo es una posibilidad, no una obligación con plazo.
:::

# 14. Control de versiones de este estándar

Los Lineamientos obligan a publicar este estándar (artículo 14, fracción II, y Transitorio TERCERO de los Lineamientos), pero no dicen cómo se modifica ni si requiere aprobación del Comité (vacío V13). Este capítulo fija las reglas para cambiar el propio estándar.

## 14.1 Reglas

1. **Numeración.** El estándar usa el esquema MAYOR.MENOR. Las versiones 0.x son borradores. La versión 1.0 es la que se publica para cumplir el Transitorio TERCERO.
2. **Versión MAYOR.** Se incrementa cuando el cambio obliga a las áreas, a los custodios o a los sistemas a hacer algo distinto: un metadato obligatorio nuevo, un valor permitido que se elimina, un formato de clave o de folio que cambia o un capítulo que se completa con reglas obligatorias.
3. **Versión MENOR.** Se incrementa con precisiones de redacción, ejemplos, valores permitidos que se agregan o correcciones que no cambian ninguna obligación.
4. **Quién lo cambia.** La DGETD elabora y publica cada versión (art. 14 fr. II). Cualquier área, propietario o custodio puede pedir un cambio en [correo, extensión y horario de la asesoría DGETD]{custom-style="Marcador"}.
5. **Cambios en la ficha.** Un cambio en los capítulos 5 a 8 o en el Anexo A se aplica al mismo tiempo en F-CAT-01, PR-CAT-04, el formulario en línea, la plantilla de Excel y la lista de SharePoint «Inventario de catálogos».
6. **Efecto sobre lo ya registrado.** Una versión nueva no modifica las claves ni los folios ya asignados. Los registros recibidos con una versión anterior conservan su validez.
7. **Vigencia.** Cada versión rige desde su publicación y sustituye a la anterior.

::: {custom-style="Pendiente"}
**Por confirmar.** (1) Si cada versión MAYOR se presenta al Comité para su conocimiento o para su aprobación; los Lineamientos solo exigen publicarla. (2) El medio de publicación del estándar: portal de Intranet del OAJ, Sistema de Administración de Documentos Normativos Administrativos o ambos, como en el Transitorio SEGUNDO.
:::

## 14.2 Historial de versiones

| Versión | Fecha | Descripción del cambio | Elaboró |
|------------|----------------|--------------------------------------------------|------------|
| 0.1 | Noviembre de 2026 | Borrador inicial. Capítulos 1 a 8, 14 y Anexo A con contenido para el registro del Transitorio CUARTO. Capítulos 9 a 13 con estructura, propuestas y decisiones pendientes. | DGETD |

: Historial de versiones de ET-CAT-01

# Anexo A. Correspondencia entre la ficha y F-CAT-01

| Fr. | Metadato y nombre técnico | Campos | Pregunta en F-CAT-01 |
|------|--------------------------------|------------|--------------------------------------------------|
| I | Identificador del catálogo [id_catalogo]{custom-style="Clave"} | [B1]{custom-style="Clave"} · [G2]{custom-style="Clave"} | No se pregunta: la DGETD asigna la clave al recibir el registro. |
| II | Nombre oficial [nombre_oficial]{custom-style="Clave"} | [B2]{custom-style="Clave"} | ¿Cómo se llama esta lista? Escriba el nombre completo, sin siglas. |
| III | Descripción y propósito [descripcion]{custom-style="Clave"} | [B3]{custom-style="Clave"} | ¿Qué contiene esta lista y para qué la usan? |
| IV | Propietario [propietario]{custom-style="Clave"} | [C1]{custom-style="Clave"} | ¿Qué área decide qué entra y qué sale de esta lista, y con qué reglas? |
| V | Custodio [custodio]{custom-style="Clave"} | [C2]{custom-style="Clave"} | ¿Qué área mantiene la lista al día en la práctica: da de alta, corrige y da de baja? |
| VI | Clasificación [clasificacion]{custom-style="Clave"} | [C3]{custom-style="Clave"} · [G4]{custom-style="Clave"} | ¿A qué se parece más su lista? |
| VII | Sistemas consumidores [sistemas_consumidores]{custom-style="Clave"} | [D1]{custom-style="Clave"} · [G6]{custom-style="Clave"} | ¿Qué sistemas, aplicaciones, archivos o reportes usan esta lista? |
| VIII | Frecuencia de actualización [frecuencia]{custom-style="Clave"} | [D2]{custom-style="Clave"} | En la práctica, ¿cada cuánto se agrega, quita o corrige algo en esta lista? |
| IX | Versión vigente [version_vigente]{custom-style="Clave"} | [D3]{custom-style="Clave"} · [G7]{custom-style="Clave"} | ¿Su lista maneja versiones numeradas (por ejemplo, v2.3)? |
| X | Fecha de última actualización [fecha_actualizacion]{custom-style="Clave"} | [D4]{custom-style="Clave"} | ¿Cuándo fue la última vez que se agregó, quitó o corrigió algo en esta lista? |
| XI | Nivel de acceso [nivel_acceso]{custom-style="Clave"} | [E1]{custom-style="Clave"} | ¿Quién debería poder consultar esta lista? |
| XI | Datos personales [datos_personales]{custom-style="Clave"} | [E2]{custom-style="Clave"} | ¿La lista contiene datos personales, como nombres, RFC, CURP, domicilios particulares o teléfonos? |

: Correspondencia entre los metadatos del art. 8 y los campos de F-CAT-01

::: {custom-style="Pequeno"}
La letra de cada campo indica la sección de F-CAT-01; la sección G la llena la DGETD. Los campos que no corresponden a un metadato del art. 8 están en las tablas 5.4 y 5.4.b.
:::
