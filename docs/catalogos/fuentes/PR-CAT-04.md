---
codigo: PR-CAT-04
titulo: Procedimiento de registro de catálogos existentes
subtitulo: Cómo registran las áreas y los órganos jurisdiccionales las listas que ya llevan
tipo: Procedimiento
version: "0.1"
fecha: "Noviembre de 2026"
estatus: Borrador para revisión · no vigente
responsable: Dirección General de Estrategia y Transformación Digital (DGETD)
fundamento: "LGCI, art. 14 fr. IX y Transitorios TERCERO y CUARTO"
portada: completa
---

# 1. Objetivo

Establecer cómo las áreas administrativas y los órganos jurisdiccionales registran ante la Dirección General de Estrategia y Transformación Digital (DGETD) las listas de información que ya administran, con los metadatos mínimos del artículo 8 de los Lineamientos Generales de Catálogos Institucionales (LGCI, en adelante «los Lineamientos»).

El procedimiento busca un resultado concreto: un inventario de catálogos con una ficha confirmada por cada lista, una clave asignada por la DGETD y un estatus que indique si la lista es candidata a catálogo institucional. Ese inventario es el insumo del plan de adecuación que la DGETD presenta al Comité de Gobernanza Digital (el Comité) conforme al Transitorio QUINTO.

::: {custom-style="Nota"}
**Qué no hace este procedimiento.** No autoriza catálogos, no publica listas, no cambia quién las administra ni modifica ningún sistema. Tampoco es una auditoría: pide datos sobre cada lista (metadatos), no su contenido.
:::

Este procedimiento tiene un resumen visual de dos páginas, «PR-CAT-04 en una mirada», para personas titulares, el Comité y las áreas. En caso de diferencia entre el resumen y este procedimiento, manda el procedimiento.

# 2. Alcance

**A quién aplica.** A las áreas administrativas y a los órganos jurisdiccionales a cargo del Órgano de Administración Judicial (OAJ), conforme al artículo 3 de los Lineamientos, que hoy administren listas de información. También aplica a la DGETD, que recibe y administra el registro.

**Qué listas.** Las que el Transitorio CUARTO llama «catálogos de información». Como orientación, la DGETD recomienda registrar toda lista que el área lleve y que otra área, un sistema, un reporte o un trámite use o copie, o que dependa de una sola persona. Ante la duda, se registra. Por ejemplo: la lista de inmuebles que ocupa el OAJ, la de órganos jurisdiccionales, la de tipos de documento o la de sentidos de resolución.

El término «catálogos de información» es más amplio que «catálogo institucional» (art. 4 fr. III), y los Lineamientos no lo definen. Por eso el registro recibe todas las listas; después, la DGETD revisa cada una con los criterios del art. 6 y propone su estatus en el inventario (sección 6.10).

**Qué queda fuera.** El contenido de las listas, los datos personales que contengan y la propuesta de catálogos nuevos. Las listas que se creen después del cierre siguen el trámite de propuesta de nuevo catálogo (PR-CAT-01 Procedimiento de gestión del ciclo de vida de catálogos y F-CAT-02 Propuesta de nuevo catálogo).

**Vigencia.** Es un procedimiento transitorio. Opera desde su publicación hasta el cierre del registro y la entrega del inventario depurado a la DGETD para elaborar el plan de adecuación del Transitorio QUINTO (actividad 26).

# 3. Fundamento

::: {custom-style="Norma"}
**Lo que dice la norma.** «Las áreas administrativas y órganos jurisdiccionales que actualmente administren catálogos de información deberán registrarlos ante la DGETD dentro de los noventa días naturales siguientes a la entrada en vigor de estos Lineamientos, proporcionando los metadatos mínimos establecidos en el artículo 8» (Transitorio CUARTO de los Lineamientos).
:::

| Disposición | Para qué se usa en este procedimiento |
|:-----------------------------------|:---------------------------------------------------|
| Lineamientos, art. 3 | Áreas y órganos obligados. |
| Lineamientos, art. 4 | Definiciones de catálogo institucional, propietario, custodio, sistema consumidor y demás términos. |
| Lineamientos, art. 5 | Clasificación de catálogos (entidades, clasificación, parámetros y relación). El Comité determina si un catálogo es estratégico u operativo, a propuesta de la DGETD. |
| Lineamientos, art. 6 | Criterios para considerar institucional una lista; base de la depuración. |
| Lineamientos, art. 7 fr. I | Neutralidad de los identificadores; se aplica por analogía a la clave de catálogo. |
| Lineamientos, art. 8 fr. I a XI | Los 11 metadatos que se piden en el registro. |
| Lineamientos, art. 12 | El Comité formaliza propietario y custodio al aprobar un catálogo. |
| Lineamientos, art. 14 fr. I, V y IX | Inventario de catálogos autorizados (fr. I), asesoría técnica a propietarios y custodios (fr. V) y emisión de formatos y procedimientos (fr. IX) por la DGETD. |
| Lineamientos, art. 17 | Custodia preferente de la DGETD cuando el catálogo sea transversal, se integre en la arquitectura institucional de datos o se administre en la Plataforma; el Comité puede designar a otra área. |
| Lineamientos, art. 23 | Control de acceso y protección de datos personales. |
| Lineamientos, Transitorios TERCERO, CUARTO y QUINTO | Plazos de 60, 90 y 120 días naturales. |
| Lineamientos, Transitorios SEXTO y SÉPTIMO | Normativa anterior sin efectos; el Comité resuelve lo no previsto. |
| Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados | Aplicable a listas con datos personales (art. 23). |
| Acuerdo General del Pleno del Órgano de Administración Judicial que establece las disposiciones en materia de transparencia, acceso a la información pública y protección de datos personales | Aplicable al nivel de acceso de cada lista (art. 23). |

: Disposiciones que sustentan el procedimiento

# 4. Definiciones y siglas

Los términos «catálogo institucional», «catálogo autorizado», «propietario de catálogo», «custodio de catálogo», «metadatos», «sistema consumidor» y los demás del artículo 4 de los Lineamientos tienen el significado que ahí se establece. Las reglas de estructura, identificación y versionamiento están en ET-CAT-01 Estándar técnico de estructura, identificación, versionamiento y publicación de catálogos. Para este procedimiento se usan además los siguientes términos.

| Término | Significado en este procedimiento |
|:----------------------|:------------------------------------------------------------|
| Lista | Nombre que este procedimiento da a lo que el Transitorio CUARTO llama «catálogo de información»: un conjunto de valores de referencia que un área administra, como inmuebles, órganos o tipos de documento. El término no agrega requisitos al Transitorio CUARTO. |
| Registro | Trámite por el que un área informa a la DGETD los metadatos de una lista. Se hace un registro por cada lista. |
| Folio de registro | Identifica el trámite, no la lista. Tiene la forma [RC-AAAA-NNNN]{custom-style="Clave"}, por ejemplo [RC-2027-0118]{custom-style="Clave"}. Una corrección antes de confirmar la ficha se hace en el mismo folio. Una corrección después de «Confirmado» se presenta como registro nuevo, con folio nuevo y la misma clave de catálogo. |
| Clave de catálogo | Identifica la lista en el inventario. Tiene la forma [CAT-NNNN]{custom-style="Clave"}, por ejemplo [CAT-0042]{custom-style="Clave"}. La asigna la DGETD, no tiene significado y no se reutiliza ni cambia. |
| Acuse | Correo con folio, clave y fecha de recepción. Es la constancia del registro. |
| Ficha de confirmación | La ficha de la lista con lo que el área registró y lo que la DGETD prellenó. El área la revisa y la confirma. |
| Registro presentado | Criterio operativo de la DGETD: el registro que trae, como mínimo, el área, el nombre de la lista y su descripción, y que la DGETD recibe y tramita. Si basta para el plazo del Transitorio CUARTO está por confirmar (sección 6.9). |
| Registro completo | El que el área confirmó en la ficha de confirmación. |
| Persona enlace | Persona que designa la persona titular del área para llenar y dar seguimiento a los registros. |
| Inventario de catálogos | Lista de SharePoint donde la DGETD lleva todos los registros, con su estatus. |
| Día N | Día natural número N contado a partir de la entrada en vigor de los Lineamientos. El día 90 es el último del plazo del Transitorio CUARTO. |

: Términos propios del procedimiento

| Sigla | Significado |
|:----------|:------------------------------------------------------------|
| CJF | Consejo de la Judicatura Federal (extinto) |
| DGETD | Dirección General de Estrategia y Transformación Digital |
| LGCI | Lineamientos Generales de Catálogos Institucionales |
| OAJ | Órgano de Administración Judicial del Poder Judicial de la Federación |
| TI | Tecnologías de la información |

: Siglas

# 5. Responsabilidades

| Responsable | Responsabilidades | Origen |
|:---------------------|:---------------------------------------------|:------------------------------|
| DGETD | Recibir el registro. | Transitorio CUARTO |
| | Asignar la clave de catálogo. | Art. 8 fr. I y art. 14 fr. IX; este procedimiento fija la asignación para cumplir el art. 8 fr. I |
| | Llevar el inventario del registro. | Transitorio CUARTO y art. 14 fr. IX; para catálogos autorizados, art. 14 fr. I |
| | Emitir este procedimiento y el formato F-CAT-01. | Art. 14 fr. IX; Transitorio TERCERO |
| | Dar asesoría técnica durante el registro. | Art. 14 fr. V, extendida a los propietarios y custodios propuestos |
| | Prellenar, enviar la ficha de confirmación, depurar con el art. 6, aplicar la contingencia del día 75, someter el informe de cierre a consideración del Comité y devolver resultados a las áreas. | Este procedimiento |
| | Elaborar el plan de adecuación con el inventario depurado. | Transitorio QUINTO |
| Personas titulares de las áreas | Registrar las listas que su área administra. | Transitorio CUARTO |
| | Designar a la persona enlace y validar los registros de su área (campo [A3]{custom-style="Clave"}). | Este procedimiento |
| Personas enlace | Identificar las listas del área, registrarlas, atender las consultas de la DGETD y confirmar la ficha. | Este procedimiento |
| Órganos jurisdiccionales | Registrar las listas propias que administren. | Transitorio CUARTO |
| | Revisar la lista de verificación. Si no llevan listas propias, no tienen que hacer nada más. | Este procedimiento |
| Áreas de TI que operan sistemas | Informar a la DGETD qué sistemas leen cada lista registrada. | Este procedimiento |
| Comité de Gobernanza Digital | Formalizar propietario y custodio al aprobar un catálogo. | Art. 12 |
| | Determinar si un catálogo es estratégico u operativo, a propuesta de la DGETD. | Art. 5 |
| | Velar por el cumplimiento de los Lineamientos, emitir opinión sobre ellos y resolver lo no previsto. | Transitorio SÉPTIMO |
| | Aprobar el plan de adecuación. | Transitorio QUINTO |

: Responsabilidades por actor

::: {custom-style="Nota"}
**Atribuciones del Comité.** Las filas del Comité reproducen atribuciones que le dan los Lineamientos. Este procedimiento no le asigna obligaciones: prevé que la DGETD le someta el informe de cierre (actividad 24), y lo que el Comité resuelva sobre ese informe corresponde a sus propias atribuciones.
:::

::: {custom-style="Pendiente"}
**Por confirmar.** La columna «Origen» distingue lo que establecen los Lineamientos de lo que asigna este procedimiento con base en el artículo 14, fracción IX, de los Lineamientos. Las responsabilidades marcadas «Este procedimiento» requieren validación de la DGETD antes de publicar, en especial la de las áreas de TI, que no tiene un artículo que la respalde de forma expresa.
:::

# 6. Políticas de operación

## 6.1 Una ficha por cada lista

Cada lista se registra por separado. Un área con varias listas hace varios registros, o usa la plantilla de Excel si tiene más de 5. Ante la duda, el área registra la lista: la DGETD revisa después si es catálogo institucional (artículo 6 de los Lineamientos). Registrar no es autorizar.

## 6.2 Se piden metadatos, no contenido

El registro pide los 11 metadatos del art. 8 y algunas preguntas opcionales de diagnóstico. El área no adjunta la lista ni datos personales. Registrar no publica la lista, no cambia quién la administra y no modifica ningún sistema.

## 6.3 Propuestas, no decisiones

Lo que el área anota como propietario, custodio y clasificación son propuestas. El Comité formaliza al propietario y al custodio cuando aprueba el catálogo (art. 12) y determina si es estratégico u operativo (art. 5). La pregunta sobre si el área preferiría que la DGETD se encargue del mantenimiento ([C2b]{custom-style="Clave"}) solo registra un interés: la custodia la decide el Comité (art. 17).

## 6.4 «Por confirmar» es una respuesta válida

Los campos que lo permiten aceptan «Por confirmar». La DGETD ayuda a completarlos durante la revisión. El área no tiene que inventar datos que no conoce, en especial los sistemas consumidores ([D1]{custom-style="Clave"}), que la DGETD rastrea con las áreas de TI.

## 6.5 Tres canales, una sola base de datos

El área elige uno de tres canales. Los tres alimentan la misma lista de SharePoint «Inventario de catálogos».

| Canal | Para quién | Cómo funciona |
|:--------------------|:-------------------|:------------------------------------------------|
| Formulario en línea | Canal principal | Microsoft Forms de grupo, un envío por lista. El área se elige de la lista oficial de áreas y órganos, no se escribe a mano. Liga: [liga al formulario de registro]{custom-style="Marcador"}. |
| Plantilla de Excel | Áreas con más de 5 listas | Las mismas columnas que el formulario, con listas desplegables. Se sube a la carpeta de SharePoint, no por correo: [liga a la carpeta de SharePoint para plantillas de Excel]{custom-style="Marcador"}. |
| Registro acompañado | Quien lo solicite; prioritario para órganos jurisdiccionales | Sesión por Teams o llamada telefónica. La DGETD captura mientras el área responde. |

: Canales de registro

La versión en Word de F-CAT-01 es el formato de referencia: permite conocer y preparar las preguntas y sirve como constancia imprimible. No es un canal de captura.

::: {custom-style="Pendiente"}
**Por confirmar.** Antes de publicar, la DGETD verifica que Power Automate esté habilitado y que los órganos jurisdiccionales tengan cuenta de Microsoft 365. Si no es así, el registro acompañado es el canal de respaldo.
:::

## 6.6 Acuse con folio y clave

Cada registro recibe un acuse con el folio de registro, la clave de catálogo y la fecha de recepción. El acuse llega a la persona enlace con copia a la persona titular que valida ([A3]{custom-style="Clave"}). Con el acuse, el estatus del registro es «Recibido» y el estatus en el inventario es «Registrado».

La fecha de recepción es la del envío del formulario, la de carga de la plantilla de Excel a la carpeta de SharePoint o la de la sesión de registro acompañado. No depende de cuándo la DGETD procese la plantilla. En la plantilla de Excel, el acuse sale cuando la DGETD procesa el archivo: uno por archivo, con un folio y una clave por cada lista. En el registro acompañado, sale al terminar la captura.

::: {custom-style="Compromiso"}
**Compromiso DGETD.** Acuse con folio, clave y fecha de recepción. En el formulario en línea, el acuse es automático si se confirma que Power Automate está habilitado. La DGETD asigna la clave de catálogo ([CAT-NNNN]{custom-style="Clave"}) al recibir el registro. La clave es un correlativo sin significado que no cambia aunque la lista cambie de nombre o de área, y no se reutiliza aunque la lista se retire (art. 8 fr. I; art. 7 fr. I por analogía).
:::

::: {custom-style="Pendiente"}
**Por confirmar.** Si Power Automate no está habilitado, la DGETD asigna la clave a mano desde el mismo consecutivo y el acuse del formulario deja de ser automático (ET-CAT-01, sección 6.1). El tiempo entre el envío y el acuse se medirá en el piloto (actividad 3).
:::

## 6.7 Revisión y prellenado

La DGETD revisa cada registro (estatus «En revisión») y prellena lo que ya conoce: sistemas consumidores detectados con las áreas de TI ([G6]{custom-style="Clave"}), fecha de última actualización cuando la lista vive en un sistema, versión inicial 1.0 cuando la lista no maneja versiones ([G7]{custom-style="Clave"}), clasificación propuesta ([G4]{custom-style="Clave"}) y alcance propuesto ([G5]{custom-style="Clave"}). Si falta algo que solo el área sabe, la persona de contacto de la DGETD llama a la persona enlace.

::: {custom-style="Compromiso"}
**Compromiso DGETD.** La DGETD prellena lo que ya conoce y asigna una persona de contacto con nombre por bloque de áreas, que se informa en el acuse. Asesoría general: [correo, extensión y horario de la asesoría DGETD]{custom-style="Marcador"}. La DGETD no volverá a pedir al área lo que ya entregó. Este compromiso cubre solo las solicitudes de la DGETD.
:::

::: {custom-style="Pendiente"}
**Por definir.** Plazo de respuesta a dudas: [plazo por definir según capacidad de la DGETD]{custom-style="Marcador"}.
:::

## 6.8 Ficha de confirmación

La DGETD envía a la persona enlace la ficha de confirmación (sección G de F-CAT-01), con lo que el área registró y lo que la DGETD prellenó. El estatus del registro pasa a «Ficha enviada». La persona enlace revisa la ficha. Si pide corregir algo, el registro regresa a «En revisión» con el mismo folio, la DGETD hace el ajuste y reenvía la ficha. Cuando la ficha está correcta, la persona enlace la confirma con su nombre y la fecha ([G11]{custom-style="Clave"}) y el estatus pasa a «Confirmado».

::: {custom-style="Pendiente"}
**Por definir.** Plazo para enviar la ficha de confirmación desde la recepción: [plazo por definir según capacidad de la DGETD]{custom-style="Marcador"}.
:::

## 6.9 Registro presentado y registro completo

Como criterio operativo, la DGETD recibe y da trámite a todo registro que traiga el área, el nombre de la lista y su descripción ([A1]{custom-style="Clave"}, [B2]{custom-style="Clave"} y [B3]{custom-style="Clave"}). Le asigna folio y clave y anota como fecha de recepción la del envío. Los demás campos pueden llegar «Por confirmar»; la DGETD los completa con el área durante la revisión, hasta reunir los metadatos del art. 8. El registro queda completo cuando el área confirma la ficha.

::: {custom-style="Pendiente"}
**Por confirmar.** Si un registro que llega con metadatos del art. 8 «Por confirmar» se tiene por presentado en tiempo para el Transitorio CUARTO, que pide registrar «proporcionando los metadatos mínimos establecidos en el artículo 8». Se propone someterlo al Comité, que resuelve lo no previsto (Transitorio SÉPTIMO), antes de abrir el registro.
:::

## 6.10 Depuración con los criterios del artículo 6

Todo registro entra al inventario como «Registrado». Cuando el registro está «Confirmado», la DGETD depura la lista con las transiciones de ET-CAT-01, sección 7.2:

- **Registrado a En dictamen.** La DGETD revisa la lista contra los cuatro criterios del art. 6: uso por dos o más sistemas o procesos, necesidad de uniformidad institucional, naturaleza estable con actualizaciones planificadas y alcance que rebasa el uso particular de un área. Si la lista cumple los criterios o requiere más análisis, sigue «En dictamen» y pasa al diagnóstico del plan de adecuación.
- **Registrado a Duplicado.** La lista repite otra ya registrada. La DGETD anota la clave del catálogo con el que coincide y avisa a las áreas involucradas. El registro y su clave se conservan.
- **Registrado a Retirado.** El área informa que la lista dejó de usarse.
- **En dictamen a Uso local o Duplicado.** Es el resultado del análisis cuando concluye que la lista no cumple los criterios del art. 6, o que repite otra lista. Una lista de «Uso local» queda documentada y el área la sigue llevando como hasta ahora.

La DGETD revisa y propone; no aprueba catálogos. La aprobación de un catálogo institucional corresponde al Comité, con base en el dictamen técnico de la DGETD (art. 12). Cuando una lista la usa un solo sistema pero puede tener impacto institucional, el art. 6 fr. I deja la decisión «a juicio del Comité»: la DGETD la deja «En dictamen» y la señala en el informe de cierre. La DGETD comunica a cada área el estatus de sus listas y el motivo.

::: {custom-style="Pendiente"}
**Por confirmar.** Si la DGETD puede asignar «Uso local» por sí misma o si requiere conocimiento del Comité, dado que el art. 6 fr. I deja algunos casos «a juicio del Comité» (ET-CAT-01, sección 7.2). Mientras se decide, la DGETD incluye en el informe de cierre las listas que propone como «Uso local».
:::

## 6.11 Datos personales y nivel de acceso

El registro no pide datos personales ni el contenido de la lista. Solo pregunta si la lista los contiene ([E2]{custom-style="Clave"}), para protegerla, y quién debería poder consultarla ([E1]{custom-style="Clave"}). Si la lista contiene información reservada o confidencial, el área la marca como «Clasificada». Esa clasificación se rige por la normativa de transparencia; el registro solo la usa para proteger la ficha y aplicar los controles de acceso (art. 23).

::: {custom-style="Pendiente"}
**Por confirmar.** Los valores de nivel de acceso (Pública, Interna, Restringida, Clasificada y Por confirmar) son una propuesta de la DGETD. Deben alinearse con el Acuerdo General del Pleno del Órgano de Administración Judicial que establece las disposiciones en materia de transparencia, acceso a la información pública y protección de datos personales (art. 23), con la unidad de transparencia competente, antes de la versión 1.0.
:::

## 6.12 Órganos jurisdiccionales

La comunicación a los órganos jurisdiccionales llega por el conducto institucional del OAJ, no por oficio de la DGETD a personas juzgadoras. El órgano revisa la lista de verificación. Si no lleva listas propias, no tiene que hacer nada más; confirmarlo es opcional, toma un clic y no genera seguimiento. Tampoco necesita designar a una persona enlace, y el informe de cierre no lo cuenta como faltante (sección 6.15). Si lleva alguna, la registra por cualquier canal; el registro acompañado es prioritario para estos órganos.

Un catálogo es una lista de valores de referencia y no fija criterios para resolver asuntos. Cuando el contenido de una lista deriva de la función jurisdiccional, el propietario es el área administrativa competente, que recaba la opinión de los órganos jurisdiccionales involucrados (art. 4 fr. XVII).

::: {custom-style="Pendiente"}
**Por confirmar.** Conducto institucional que llega a los órganos jurisdiccionales y autoridad que lo emite: [autoridad que emite la circular]{custom-style="Marcador"}.
:::

## 6.13 Información previa verificable

La DGETD usa para prellenar la información previa que exista y esté verificada. Por ejemplo, la que se haya generado con los Lineamientos Generales para la Consolidación de Catálogos Institucionales del extinto CJF, que quedaron sin efectos (Transitorio SEXTO). Si esa información no existe o no se puede verificar, no se usa y la lista se registra como cualquier otra. Las listas consolidadas con la norma anterior también se registran; su tratamiento se define en el plan de adecuación.

::: {custom-style="Pendiente"}
**Por confirmar.** Si existe un inventario de la consolidación del extinto CJF, en qué estado está y quién lo resguarda.
:::

## 6.14 Contingencia a partir del día 75

A partir del día 75, la DGETD revisa qué listas conoce y no se han registrado: por sus propios sistemas, por información previa verificada o porque otra área las mencionó en su registro (por ejemplo, en [D1]{custom-style="Clave"} o [F4]{custom-style="Clave"}). Para cada una, envía al área una ficha prellenada que pide solo los campos que solo el área conoce: persona enlace y persona titular ([A2]{custom-style="Clave"} y [A3]{custom-style="Clave"}), confirmación del nombre y la descripción ([B2]{custom-style="Clave"} y [B3]{custom-style="Clave"}), propietario y custodio propuestos ([C1]{custom-style="Clave"} y [C2]{custom-style="Clave"}), frecuencia de actualización ([D2]{custom-style="Clave"}), nivel de acceso ([E1]{custom-style="Clave"}) y datos personales ([E2]{custom-style="Clave"}). Cuando el área devuelve la ficha, la DGETD la recibe como registro presentado (sección 6.9) y sigue el trámite normal desde la revisión.

::: {custom-style="Pendiente"}
**Por confirmar.** Con la fecha supuesta de entrada en vigor, el día 75 es el [jueves 31 de diciembre de 2026, por confirmar]{custom-style="Marcador"}, dentro del periodo vacacional de fin de año. Conviene decidir si la contingencia se adelanta a antes del receso o se aplica el primer día hábil de enero.
:::

## 6.15 Cierre del registro y casos no registrados

El registro cierra el día 90: [viernes 15 de enero de 2027, por confirmar]{custom-style="Marcador"}. Ese día la DGETD hace el corte del inventario. Los registros que lleguen después se reciben con su fecha real de recepción y se identifican como extemporáneos en el inventario.

Los Lineamientos no establecen un trámite específico para las listas que no se registren. La DGETD somete al Comité, en el informe de cierre, las áreas administrativas sin enlace designado, las áreas administrativas sin registros y las listas conocidas que no se registraron, para que, en su caso, determine lo conducente (Transitorio SÉPTIMO). El informe no incluye como faltantes a los órganos jurisdiccionales sin listas propias, hayan confirmado o no.

## 6.16 Correcciones sin costo hasta el dictamen

El área puede corregir su registro sin costo hasta el dictamen técnico de la lista. Antes de confirmar la ficha, la corrección se hace en el mismo trámite: el registro regresa de «Ficha enviada» a «En revisión» con el mismo folio. Después de «Confirmado», la corrección se presenta como registro nuevo, con folio nuevo y la misma clave de catálogo (ET-CAT-01, sección 7.1).

::: {custom-style="Pendiente"}
**Por confirmar.** Hasta cuándo puede corregir el área las listas que no llegan a dictamen técnico: las que pasan de «Registrado» a «Duplicado» o a «Retirado» (sección 6.10).
:::

::: {custom-style="Compromiso"}
**Compromiso DGETD.** El registro no es una auditoría. Los errores se corrigen sin costo hasta el dictamen, y durante la transición la DGETD informará la calidad en cifras agregadas, no por área.
:::

## 6.17 Resultados y devolución a las áreas

Al cierre, la DGETD prevé devolver a cada área su ficha validada y el estatus de cada una de sus listas en el inventario, en [plazo por definir según capacidad de la DGETD]{custom-style="Marcador"}. Los resultados del registro (número de listas, avance por estatus, canales usados) se informan en cifras agregadas durante la transición.

## 6.18 Asesoría técnica

El art. 14 fr. V obliga a la DGETD a dar asesoría técnica a propietarios y custodios de catálogos. Durante la transición todavía no están formalizados (art. 12), así que la DGETD extiende esa asesoría a las áreas que mantienen las listas registradas, que son los propietarios y custodios propuestos. La da durante todo el registro, por el contacto asignado a cada bloque de áreas y en el registro acompañado.

# 7. Descripción de actividades

| No. | Responsable | Actividad | Formato o registro |
|:------|:--------------------|:----------------------------------------------------|:--------------------|
| 1 | DGETD | Confirma la fecha de entrada en vigor de los Lineamientos y fija las fechas del calendario (capítulo 11). | Calendario del registro |
| 2 | DGETD | Prepara los canales: formulario, plantilla de Excel, carpeta de SharePoint y lista «Inventario de catálogos». Carga la lista oficial de áreas y órganos. Verifica Power Automate y las cuentas de Microsoft 365. | Lista de SharePoint «Inventario de catálogos» |
| 3 | DGETD | Hace un piloto con 3 perfiles: un área de alta madurez digital, una de baja y un órgano jurisdiccional o su área competente. Mide el tiempo de llenado y ajusta formulario, plantilla y guía. | Notas del piloto |
| 4 | DGETD | Publica PR-CAT-04, F-CAT-01 (Word, plantilla de Excel y formulario) y el kit de registro: guía, ficha de ejemplo, lista de verificación y preguntas frecuentes. | F-CAT-01; kit de registro |
| 5 | DGETD | Asigna una persona de contacto con nombre a cada bloque de áreas y publica el directorio. | Directorio de contactos |
| 6 | DGETD | Sostiene reuniones bilaterales con titulares de áreas que llevan listas críticas (personal, adscripciones, inmuebles, órganos) y un taller técnico con las áreas de TI. | Minutas |
| 7 | DGETD | Gestiona el oficio a titulares, que pide designar a una persona enlace, y la comunicación a los órganos jurisdiccionales por el conducto institucional. | Oficio; circular |
| 8 | Persona titular | Designa a la persona enlace y lo comunica a la DGETD. | Designación de enlace |
| 9 | DGETD | Registra la designación y envía el kit de registro a la persona enlace. | Correo; inventario |
| 10 | Persona enlace | Identifica las listas que lleva el área. Ante la duda, incluye la lista. | Guía de registro |
| 11 | Persona enlace | Registra cada lista por el canal elegido: formulario, plantilla de Excel o registro acompañado. | F-CAT-01 |
| 12 | Órgano jurisdiccional | Revisa la lista de verificación. Si lleva listas propias, sigue la actividad 11. Si no, concluye; confirmarlo es opcional. | Lista de verificación |
| 13 | DGETD | Envía el acuse con folio, clave y fecha de recepción a la persona enlace, con copia a la persona titular. Estatus: «Recibido» y «Registrado». | Acuse |
| 14 | DGETD | Revisa el registro y prellena lo que conoce. Si falta un dato que solo el área sabe, la persona de contacto llama a la persona enlace. Estatus: «En revisión». | Inventario |
| 15 | Áreas de TI | Informan a la DGETD qué sistemas leen la lista. | Correo; inventario |
| 16 | DGETD | Envía la ficha de confirmación a la persona enlace. Estatus: «Ficha enviada». | Ficha de confirmación |
| 17 | Persona enlace | Revisa la ficha. Si pide corregir algo, sigue la actividad 14 con el mismo folio (estatus «En revisión»). Si está correcta, la confirma. Estatus: «Confirmado». | Ficha de confirmación |
| 18 | DGETD | Depura la lista con las transiciones de ET-CAT-01, sección 7.2: la pasa a «En dictamen» y la revisa contra los criterios del artículo 6 de los Lineamientos; según el resultado, sigue «En dictamen» o pasa a «Uso local» o «Duplicado». Si repite otra lista, puede pasar de «Registrado» a «Duplicado». | Inventario |
| 19 | DGETD | Actualiza el inventario y comunica al área el estatus de cada lista y su motivo. | Inventario; correo |
| 20 | DGETD | A partir del día 75, identifica listas conocidas sin registro y envía al área una ficha prellenada de contingencia. Si no hay, sigue la actividad 22. | Ficha prellenada de contingencia |
| 21 | Persona enlace | Completa los campos que solo el área conoce y devuelve la ficha. Sigue la actividad 14. | Ficha prellenada de contingencia |
| 22 | DGETD | Cierra el registro el día 90 y hace el corte del inventario. Recibe los registros extemporáneos con su fecha real. | Corte del inventario |
| 23 | DGETD | Elabora el informe de cierre: cifras agregadas, áreas administrativas sin enlace o sin registro, listas conocidas no registradas, listas propuestas como «Uso local» y listas que requieren juicio del Comité (art. 6 fr. I). | Informe de cierre |
| 24 | DGETD | Somete el informe de cierre a consideración del Comité, que en su caso determina lo conducente (Transitorio SÉPTIMO). | Informe de cierre |
| 25 | DGETD | Devuelve a cada área su ficha validada y el estatus de sus listas en el inventario. | Ficha de confirmación; correo |
| 26 | DGETD | Entrega el inventario depurado como insumo del plan de adecuación del Transitorio QUINTO. Termina el procedimiento. | Inventario de catálogos |

: Actividades del procedimiento

# 8. Diagrama de flujo

![Diagrama de flujo de carriles, parte 1 de 2, con tres columnas: Área u órgano jurisdiccional, DGETD y Comité de Gobernanza Digital, este último fuera de este procedimiento. La DGETD prepara canales, piloto y kit (1–7). La persona titular designa a la persona enlace (8) y la DGETD le envía el kit (9). El área identifica sus listas; el órgano jurisdiccional usa la lista de verificación (10). Rombo 12: ¿el órgano lleva listas propias? Si no, concluye y confirmarlo es opcional. Si sí, registra cada lista por formulario, Excel o registro acompañado (11). La DGETD envía el acuse con folio y clave (13), revisa y prellena con las áreas de TI (14–15) y envía la ficha de confirmación (16). El área revisa la ficha y la confirma o pide corregirla (17); si pide corregir, el registro vuelve a revisión (14). Con la ficha confirmada, el flujo sigue en la figura 2.](img/pr-cat-04-flujo-1.png){width=100%}\

::: {custom-style="Pequeno"}
Figura 1. Flujo del registro, parte 1: de la preparación a la confirmación de la ficha (actividades 1 a 17). Los números corresponden a las actividades del capítulo 7; después de la figura 2, los mismos pasos en texto.
:::

![Diagrama de flujo de carriles, parte 2 de 2, con las mismas tres columnas. Viene de la ficha confirmada (17). La DGETD depura con el artículo 6: la lista pasa a «En dictamen» y, en su caso, a «Uso local» o «Duplicado» (18–19). En el día 75 decide si hay listas conocidas sin registro (20); si las hay, el área completa una ficha prellenada (21) y el registro vuelve a revisión (14–15, figura 1). Si no, la DGETD cierra el registro el día 90 (22), elabora el informe de cierre y lo somete al Comité (23–24), que lo considera y, en su caso, determina lo conducente. La DGETD devuelve a cada área su ficha y estatus (25), entrega el inventario para el plan de adecuación (26), que aprueba el Comité, y el procedimiento termina.](img/pr-cat-04-flujo-2.png){width=100%}\

::: {custom-style="Pequeno"}
Figura 2. Flujo del registro, parte 2: de la depuración a la entrega del inventario (actividades 18 a 26).
:::

1. **Preparación (1 a 7).** La DGETD fija el calendario, prepara los canales, hace el piloto, publica el procedimiento, el formato y el kit, asigna contactos y gestiona el oficio a titulares y la comunicación a los órganos jurisdiccionales.
2. **Designación (8 y 9).** La persona titular designa a la persona enlace. La DGETD registra la designación y le envía el kit.
3. **Registro (10 a 12).** La persona enlace identifica las listas del área y registra cada una por el canal que elija. El órgano jurisdiccional revisa la lista de verificación: si no lleva listas propias, concluye aquí y confirmarlo es opcional; si lleva alguna, la registra.
4. **Acuse (13).** La DGETD envía el acuse con folio, clave y fecha de recepción.
5. **Revisión y prellenado (14 y 15).** La DGETD revisa y prellena; las áreas de TI informan los sistemas que leen la lista.
6. **Confirmación (16 y 17).** La DGETD envía la ficha de confirmación. La persona enlace la confirma o pide corregirla; si pide corregir, el registro vuelve a la revisión (14) con el mismo folio.
7. **Depuración (18 y 19).** Con la ficha confirmada, la DGETD pasa la lista a «En dictamen», la revisa con los criterios del artículo 6 de los Lineamientos y, en su caso, la pasa a «Uso local» o «Duplicado». Actualiza el inventario y comunica el estatus al área.
8. **Contingencia (20 y 21).** A partir del día 75, si hay listas conocidas sin registro, la DGETD envía una ficha prellenada; el área completa los campos que solo ella conoce y el registro vuelve a la revisión (14). Si no las hay, el flujo sigue al cierre.
9. **Cierre e informe (22 a 24).** La DGETD cierra el registro el día 90, hace el corte, elabora el informe de cierre y lo somete a consideración del Comité.
10. **Devolución y entrega (25 y 26).** La DGETD prevé devolver a cada área su ficha validada y el estatus de sus listas, y entrega el inventario depurado para el plan de adecuación. Termina el procedimiento. El Comité aprueba ese plan fuera de este procedimiento.

# 9. Formatos y registros

| Formato o registro | Para qué sirve | Quién lo llena | Dónde se guarda |
|:----------------------|:----------------------------------------|:---------------------|:--------------------|
| F-CAT-01 Registro de catálogo existente (Word) | Formato de referencia con todas las preguntas; sirve para preparar el registro y como constancia imprimible. | Persona enlace | Área |
| F-CAT-01 en formulario en línea | Canal principal de captura: un envío por lista. | Persona enlace | Lista «Inventario de catálogos» |
| F-CAT-01 plantilla de Excel | Carga de varias listas a la vez (más de 5). | Persona enlace | Carpeta de SharePoint y lista «Inventario de catálogos» |
| Acuse | Constancia del registro con folio, clave y fecha de recepción. | DGETD | Correo del enlace y de la persona titular |
| Ficha de confirmación | Revisión y confirmación de los datos de la lista (sección G de F-CAT-01). | DGETD prellena; enlace confirma | Lista «Inventario de catálogos» |
| Ficha prellenada de contingencia | Registro de listas conocidas sin registro a partir del día 75. | DGETD prellena; enlace completa | Lista «Inventario de catálogos» |
| Lista de SharePoint «Inventario de catálogos» | Registro maestro de todos los registros, folios, claves y estatus. | DGETD | SharePoint de la DGETD |
| Informe de cierre | Resultados del registro para el Comité. | DGETD | Expediente del Comité |

: Formatos y registros del procedimiento

# 10. Indicadores del procedimiento

Los indicadores miden cómo funciona el registro, no la calidad de las listas. Se calculan con la lista «Inventario de catálogos» y se informan en cifras agregadas.

| Indicador | Cómo se calcula | Frecuencia |
|:-------------------------|:------------------------------------------------------|:---------------|
| Áreas con enlace designado | Áreas administrativas con enlace designado entre el total de áreas administrativas, por 100. No incluye a los órganos jurisdiccionales, que no necesitan designar enlace si no llevan listas propias. | Semanal |
| Registros confirmados | Registros con estatus «Confirmado» entre registros recibidos, por 100. | Semanal |
| Días de recepción a ficha | Promedio de días naturales entre la fecha de recepción y el envío de la ficha de confirmación. | Semanal |
| Días de ficha a confirmación | Promedio de días naturales entre el envío de la ficha y la confirmación del área. | Semanal |
| Campos «Por confirmar» al recibir | Campos con «Por confirmar» entre campos que lo admiten, en los registros recibidos, por 100. | Al cierre |
| Registros por canal | Registros recibidos por cada canal entre el total, por 100. | Al cierre |
| Listas depuradas | Listas que ya salieron de «Registrado» (están «En dictamen», «Uso local», «Duplicado» o «Retirado») entre listas con registro «Confirmado», por 100. | Al cierre |

: Indicadores del procedimiento

::: {custom-style="Pendiente"}
**Por definir.** Las metas de cada indicador se fijan después del piloto. El tiempo de llenado se medirá en el piloto.
:::

# 11. Calendario

Todos los plazos corren desde la entrada en vigor, que es el día siguiente a la publicación (Transitorio PRIMERO de los Lineamientos). Las fechas suponen que la publicación fue el 16 de octubre de 2026 y deben confirmarse: [fecha de entrada en vigor por confirmar]{custom-style="Marcador"}.

| Hito | Fecha | Día |
|:----------------------|:--------------------------------------------------------------|:------|
| Entrada en vigor de los Lineamientos | [fecha de entrada en vigor por confirmar]{custom-style="Marcador"} | 0 |
| Piloto con 3 perfiles | [segunda quincena de noviembre de 2026, por confirmar]{custom-style="Marcador"} | — |
| Publicación anticipada de PR-CAT-04 y F-CAT-01 (propuesta) | [fines de noviembre de 2026, por confirmar]{custom-style="Marcador"} | — |
| Reuniones bilaterales y oficio a titulares | [primera semana de diciembre de 2026, por confirmar]{custom-style="Marcador"} | — |
| Designación de personas enlace | [fecha por definir]{custom-style="Marcador"} | — |
| Plazo para publicar formatos y procedimientos (Transitorio TERCERO) | [miércoles 16 de diciembre de 2026, por confirmar]{custom-style="Marcador"} | 60 |
| Inicio de la contingencia | [jueves 31 de diciembre de 2026, por confirmar]{custom-style="Marcador"} | 75 |
| Cierre del registro (Transitorio CUARTO) | [viernes 15 de enero de 2027, por confirmar]{custom-style="Marcador"} | 90 |
| Informe de cierre al Comité | [fecha de sesión del Comité por confirmar]{custom-style="Marcador"} | — |
| Plan de adecuación aprobado (Transitorio QUINTO) | [domingo 14 de febrero de 2027, por confirmar]{custom-style="Marcador"} | 120 |

: Calendario del registro

::: {custom-style="Alerta"}
**Atención.** Si F-CAT-01 y este procedimiento se publican hasta el día 60, la ventana real de registro se reduce a unos 10 días hábiles de enero. Por eso se propone publicarlos antes que el resto del paquete. El día 120 cae en domingo: el plan debe estar aprobado en una sesión anterior del Comité.
:::

# 12. Control de cambios

| Versión | Fecha | Descripción del cambio | Elaboró |
|:------------|:--------------------|:----------------------------------------------|:------------|
| 0.1 | Noviembre de 2026 | Primera versión para revisión interna. No vigente. | DGETD |

: Control de cambios del documento
