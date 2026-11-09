---
titulo: Especificación de implementación del registro de catálogos en Microsoft 365
subtitulo: Formulario, flujos, listas, plantilla de Excel, acuse y ficha de confirmación del registro de catálogos existentes (Transitorio CUARTO de los Lineamientos Generales de Catálogos Institucionales)
tipo: Especificación técnica
version: "0.1"
fecha: "Noviembre de 2026"
estatus: Borrador para revisión · uso interno de la DGETD, no se publica
responsable: Dirección General de Estrategia y Transformación Digital (DGETD)
fundamento: "LGCI, art. 14 fr. I y IX; Transitorio CUARTO"
portada: completa
---

# Cómo leer este documento

| Dato | Valor |
|:---------------------|:------------------------------------------------------------|
| Para quién | Equipo técnico de la Dirección General de Estrategia y Transformación Digital (DGETD) que monta el registro |
| Fuente de verdad | `spec/registro.yaml` v0.1 (campos, preguntas, valores, claves, estatus y marcadores) |
| Se apoya en | ET-CAT-01, capítulos 5 a 7 (nombres técnicos, clave, folio y estatus), y PR-CAT-04 (canales, acuse, ficha, contingencia y cierre) |

: Alcance de la especificación

- Los campos de `registro.yaml` se citan por su identificador (`A1`, `C2b`, `G8`). Los nombres técnicos de columna van en código (`nombre_oficial`).
- Los datos por confirmar van resaltados, igual que en el resto del paquete: [liga al formulario de registro]{custom-style="Marcador"}. Ninguno se publica sin sustituirlo.
- Los recuadros «Por confirmar» y «Decisión del equipo» requieren validación antes del piloto. El capítulo 13 los reúne.
- Este documento no agrega compromisos. Los compromisos de la DGETD son solo los de PR-CAT-04: acuse con folio, clave asignada, prellenado de lo que conoce, persona de contacto con nombre, no volver a pedir lo ya entregado y correcciones sin costo hasta el dictamen.

| Sigla | Significado |
|:-------------|:------------------------------------------------------------|
| DGETD | Dirección General de Estrategia y Transformación Digital |
| DLP | Directivas de prevención de pérdida de datos de Power Platform |
| HTML | Lenguaje de marcado de las páginas web y de los correos con formato |
| ID | Identificador interno que SharePoint asigna a cada elemento de una lista |
| JSON | Formato de texto para datos estructurados (JavaScript Object Notation) |
| LGCI | Lineamientos Generales de Catálogos Institucionales |
| M365 | Microsoft 365 |
| OData | Sintaxis de filtros que usa SharePoint en «Obtener elementos» |
| OAJ | Órgano de Administración Judicial del Poder Judicial de la Federación |
| TI | Tecnologías de la información |
| WCAG | Pautas de Accesibilidad para el Contenido Web (versión 2.2, nivel AA) |

: Siglas

# 1. Arquitectura

## 1.1 Componentes

El registro se monta solo con herramientas de M365 y conectores estándar de Power Automate. No usa conectores premium, ni Dataverse para guardar datos, ni la Plataforma de Acceso a la Información Institucional, que no está verificada (vacío V2).

| Componente | Qué es | Dueño | Notas |
|:------------------------|:--------------------------------------------|:--------------------|:------------------------------|
| Formulario «Registro de catálogo existente» | Microsoft Forms de grupo. Canal principal y canal del registro acompañado. | Grupo de M365 de la DGETD | Nunca en la cuenta personal de una persona servidora pública. |
| Formulario «Mi órgano no lleva listas propias» | Microsoft Forms de grupo con una sola pregunta. Confirmación opcional de un clic para órganos jurisdiccionales. | Grupo de M365 de la DGETD | Sin flujo y sin seguimiento (sección 5.6). |
| Sitio «Registro de catálogos» | Sitio de SharePoint del grupo de la DGETD. | Grupo de M365 de la DGETD | Zona horaria (UTC-06:00) Guadalajara, Ciudad de México, Monterrey. Idioma español. |
| Lista «Inventario de catálogos» | Un elemento por lista registrada. Guarda la ficha y la clave `CAT-NNNN`. | DGETD | Sección 2. |
| Lista «Registros» | Un elemento por trámite. Guarda el folio `RC-AAAA-NNNN` y la respuesta original. | DGETD | Sección 3. |
| Lista «Áreas y órganos» | Lista oficial de áreas y órganos, con contacto DGETD por bloque y correo de la persona titular. | DGETD | Sección 3.4. |
| Lista «Parámetros» | Valores de configuración que leen los flujos. | DGETD | Sección 3.5. |
| Biblioteca «Recepción de plantillas» | Carpeta donde las áreas suben la plantilla de Excel. | DGETD | Sección 7. |
| Biblioteca «Plantillas procesadas» | Destino privado de cada plantilla después de leerla. | DGETD | Sección 7. |
| Libro «Consolidado de plantillas» | Libro de Excel con Power Query que junta todas las plantillas para validarlas. | DGETD | Sección 7.4. |
| Buzón compartido del registro | Remitente del acuse y de la ficha; recibe respuestas y alertas. | DGETD | [correo, extensión y horario de la asesoría DGETD]{custom-style="Marcador"} |
| Flujos REG-01 a REG-06 | Flujos de Power Automate con conectores estándar. | Cuenta de servicio o grupo de la DGETD | Sección 6. |

: Componentes del registro

Conectores que se usan, todos estándar: Microsoft Forms, SharePoint, Office 365 Outlook, Excel Online (Business), Office 365 Groups, Microsoft Teams y Aprobaciones. OneDrive para la Empresa es opcional (sección 8.4).

## 1.2 Diagrama

![Diagrama de tres carriles: Área u órgano (persona enlace), Power Automate y SharePoint de la DGETD. La persona enlace registra cada lista en el formulario de Forms (o la DGETD captura con el área en el registro acompañado) y el envío llega a REG-01, que crea el catálogo y el trámite y calcula clave y folio. La persona enlace sube la plantilla F-CAT-01 a «Recepción de plantillas» y el archivo llega a REG-02, que hace lo mismo por renglón y envía un acuse por archivo. REG-01 y REG-02 escriben en las listas «Inventario de catálogos» (un elemento por lista, clave CAT-NNNN) y «Registros» (un elemento por trámite, folio RC-AAAA-NNNN), consultan la lista «Áreas y órganos» y envían el acuse por el buzón compartido; la persona enlace recibe el acuse con copia a la persona titular. REG-02 mueve cada archivo a «Plantillas procesadas», que alimenta el libro «Consolidado de plantillas» con Power Query. REG-03 lee la ficha del inventario, la envía a la persona enlace, recibe su respuesta y actualiza el estatus en el inventario.](../fuentes/img/impl-registro-arquitectura.png){width=100%}\

::: {custom-style="Pequeno"}
Figura 1. Componentes del registro y su relación. Abajo, los mismos pasos en texto.
:::

1. La persona enlace registra cada lista en el formulario de grupo. En el registro acompañado, una persona de la DGETD llena el mismo formulario mientras el área responde.
2. REG-01 lee la respuesta, consulta «Áreas y órganos», crea el elemento del catálogo en «Inventario de catálogos» y el del trámite en «Registros», calcula clave y folio, y envía el acuse desde el buzón compartido a la persona enlace con copia a la persona titular.
3. Las áreas con más de 5 listas suben la plantilla de Excel a «Recepción de plantillas». REG-02 lee cada renglón, hace lo mismo que REG-01 por renglón, mueve el archivo a «Plantillas procesadas» y envía un acuse por archivo.
4. El libro «Consolidado de plantillas» junta con Power Query todas las plantillas procesadas para validar y conciliar contra «Registros».
5. La DGETD revisa y prellena en el inventario. REG-03 lee la ficha, la envía a la persona enlace y, con su respuesta (confirma o pide corregir), actualiza el estatus en el inventario.

## 1.3 Reglas de diseño

1. **Una sola base de datos.** Los tres canales escriben en las mismas dos listas (PR-CAT-04, sección 6.5).
2. **Nada pertenece a una persona.** Formulario, sitio y buzón son del grupo de M365 de la DGETD. Los flujos tienen al menos dos propietarios (sección 9.1).
3. **Nada se borra.** Un elemento creado por error cambia de estatus; no se elimina (sección 4.4).
4. **La clave y el folio se calculan una vez y se guardan.** Nunca se recalculan a partir del ID después de guardados.
5. **Todo flujo se puede volver a ejecutar sin duplicar.** Cada paso busca primero si ya hizo su trabajo, por medio de `id_origen` (sección 6.3).
6. **Primero en listas de prueba.** El desarrollo y las pruebas se hacen en un sitio de pruebas. Las listas de producción no reciben elementos de prueba, para que `CAT-0001` sea el primer registro real (sección 4.4).

# 2. Lista «Inventario de catálogos»

## 2.1 Configuración

- Crear la lista vacía, sin plantilla. Desactivar los datos adjuntos: el registro no recibe el contenido de las listas.
- Historial de versiones activado, sin límite bajo (por ejemplo, 100 versiones). Así queda la fecha y la persona de cada cambio de estatus (ET-CAT-01, sección 7.2, regla 3).
- La columna `Title` se usa como clave de catálogo (`id_catalogo`). SharePoint no permite cambiar su nombre interno. Se le cambia el nombre visible a «Clave de catálogo», se marca como no obligatoria, se indexa y se activa «Aplicar valores únicos».
- Crear cada columna primero con su nombre interno (sin espacios, sin acentos, en minúsculas y con guion bajo, como pide ET-CAT-01, sección 5.1, regla 6) y después cambiar el nombre visible. SharePoint fija el nombre interno al crear la columna.
- En todas las columnas de elección: sin valor predeterminado (SharePoint propone el primer valor; hay que borrarlo), sin «Permitir valores de relleno» y con un valor por línea.
- Obligatorias en SharePoint: solo `area_registra`, `nombre_oficial` y `descripcion`, que son las indispensables para que la DGETD reciba y dé trámite al registro (PR-CAT-04, sección 6.9). El resto no se marca obligatorio en SharePoint porque el flujo crea el elemento con lo que llegó y escribe «Por confirmar» donde aplica.
- Índices: `Title`, `id_origen`, `area_registra`, `estatus_registro` y `estatus_inventario`.

## 2.2 Columnas

En la columna «Oblig.» (obligatoria): **Sí** es obligatorio; **Sí o PC** es obligatorio pero acepta «Por confirmar»; **No** es opcional; **DGETD** lo llena la DGETD; **Flujo** lo escribe un flujo. Entre paréntesis, junto al nombre visible, va el campo de `registro.yaml` que guarda la columna. Las columnas se crean en el orden de las cuatro tablas, que siguen las secciones de `registro.yaml`.

| Nombre interno | Nombre visible (campo) | Tipo | Oblig. | Valores de elección |
|:------------------------------------------------|:---------------------------|:----------------------|:---------------|:---------------------------------|
| `Title` | Clave de catálogo (`B1` · `G2`) | Una línea de texto, valores únicos | Flujo | `CAT-NNNN` (sección 4) |
| `area_registra` | Área que registra (`A1`) | Búsqueda en «Áreas y órganos» | Sí | Lista oficial |
| `enlace_nombre` | Persona enlace: nombre completo (`A2`) | Una línea de texto (150) | Sí | — |
| `enlace_puesto` | Persona enlace: puesto (`A2`) | Una línea de texto (150) | Sí | — |
| `enlace_correo` | Persona enlace: correo institucional (`A2`) | Una línea de texto (254) | Sí | — |
| `enlace_extension` | Persona enlace: extensión (`A2`) | Una línea de texto (10) | Sí | — |
| `titular_nombre` | Persona titular que valida: nombre completo (`A3`) | Una línea de texto (150) | Sí | — |
| `titular_puesto` | Persona titular que valida: puesto (`A3`) | Una línea de texto (150) | Sí | — |
| `clave_interna` | Clave interna actual (`B1b`) | Una línea de texto (50) | No | — |
| `nombre_oficial` | Nombre oficial (`B2`) | Una línea de texto (200) | Sí | — |
| `descripcion` | Descripción y propósito (`B3`) | Varias líneas de texto, sin formato | Sí | — |

: Columnas del inventario, secciones A y B (quién registra y su lista)

| Nombre interno | Nombre visible (campo) | Tipo | Oblig. | Valores de elección |
|:------------------------------------------------|:---------------------------|:----------------------|:---------------|:---------------------------------|
| `propietario` | Propietario propuesto (`C1`) | Búsqueda en «Áreas y órganos» | Sí o PC | Lista oficial y el elemento «Por confirmar» |
| `custodio` | Custodio propuesto (`C2`) | Búsqueda en «Áreas y órganos» | Sí o PC | Lista oficial y el elemento «Por confirmar» |
| `custodio_contacto` | Custodio propuesto: persona de contacto (`C2` (subcampo)) | Una línea de texto (255) | No | — |
| `preferencia_custodia` | Preferencia de custodia (`C2b`) | Elección | No | Sí · No · No sé |
| `clasificacion_area` | Clasificación (tipo de lista) (`C3`) | Elección | Sí o PC | Entidades · Clasificación · Parámetros · Relación · Por confirmar |
| `sistemas_consumidores` | Sistemas consumidores (`D1`) | Varias líneas de texto, sin formato | Sí o PC | — |
| `sistemas_por_dgetd` | Sistemas consumidores: que la DGETD complete la lista (`D1` (casilla)) | Sí o no | No | — |
| `frecuencia` | Frecuencia de actualización (`D2`) | Elección | Sí o PC | Cada vez que ocurre un cambio · Diaria · Semanal · Mensual · Trimestral · Semestral · Anual · Casi nunca cambia · No hay una periodicidad definida · Por confirmar |
| `frecuencia_disparador` | Frecuencia: hecho que dispara el cambio (`D2` (subcampo)) | Una línea de texto (255) | No | — |
| `maneja_versiones` | Versión vigente: respuesta del área (`D3`) | Elección | Sí o PC | Sí (indique cuál es la actual) · No · Por confirmar |
| `version_area` | Versión vigente: versión actual que indica el área (`D3` (subcampo)) | Una línea de texto (20) | No | — |
| `fecha_actualizacion` | Fecha de última actualización (`D4`) | Una línea de texto (13) | Sí o PC | `AAAA-MM`, `AAAA-MM-DD` o «Por confirmar» |
| `fecha_en_sistema` | Fecha: que la DGETD la obtenga del sistema (`D4` (casilla)) | Sí o no | No | — |

: Columnas del inventario, secciones C y D (propietario, custodio, uso y cambios)

| Nombre interno | Nombre visible (campo) | Tipo | Oblig. | Valores de elección |
|:------------------------------------------------|:---------------------------|:----------------------|:---------------|:---------------------------------|
| `nivel_acceso` | Nivel de acceso (`E1`) | Elección | Sí o PC | Pública · Interna · Restringida · Clasificada · Por confirmar |
| `datos_personales` | Datos personales (`E2`) | Elección | Sí | Sí · No · No sé |
| `ubicacion_lista` | Dónde vive la lista (`F1`) | Elección | No | En un sistema o base de datos · En una hoja de cálculo en carpeta compartida · En una hoja de cálculo en el equipo de una persona · En papel · Otro |
| `tamano_aproximado` | Tamaño aproximado (`F2`) | Elección | No | Menos de 50 · De 50 a 500 · De 501 a 5,000 · Más de 5,000 · No sé |
| `clave_elementos` | Clave de cada renglón (`F3`) | Elección | No | Sí, y la clave tiene significado (incluye año, lugar, materia u otro dato) · Sí, y es un número sin significado · No tiene clave · No sé |
| `listas_parecidas` | Listas parecidas (`F4`) | Una línea de texto (255) | No | — |
| `problema_actual` | Problema actual (`F5`) | Varias líneas de texto, sin formato | No | — |

: Columnas del inventario, secciones E y F (acceso y diagnóstico opcional)

| Nombre interno | Nombre visible (campo) | Tipo | Oblig. | Valores de elección |
|:------------------------------------------------|:---------------------------|:----------------------|:---------------|:---------------------------------|
| `folio_registro` | Folio de registro (`G1`) | Una línea de texto (13) | Flujo | `RC-AAAA-NNNN` del trámite vigente |
| `fecha_recepcion` | Fecha de recepción (`G3`) | Fecha y hora, solo fecha | Flujo | — |
| `clasificacion` | Clasificación propuesta (art. 5 fr. I–IV) (`G4`) | Elección | DGETD | Entidades · Clasificación · Parámetros · Relación · Por confirmar |
| `alcance` | Alcance propuesto (estratégico u operativo) (`G5`) | Elección | DGETD | Estratégico · Operativo o de alcance acotado · Por determinar |
| `sistemas_dgetd` | Sistemas consumidores detectados por la DGETD (`G6`) | Varias líneas de texto, sin formato | DGETD | — |
| `version_vigente` | Versión inicial registrada (`G7`) | Una línea de texto (20) | DGETD | — |
| `estatus_registro` | Estatus del registro (`G8`) | Elección | Flujo y DGETD | Recibido · En revisión · Ficha enviada · Confirmado |
| `estatus_inventario` | Estatus en el inventario (`G9`) | Elección | Flujo y DGETD | Registrado · En dictamen · Autorizado · En adecuación · Uso local · Duplicado · Retirado |
| `observaciones` | Observaciones (`G10`) | Varias líneas de texto, sin formato, «Anexar cambios al texto existente» | DGETD y flujo | — |
| `confirmacion_area` | Confirmación del área (nombre, fecha) (`G11`) | Una línea de texto (255) | Flujo | — |
| `extemporaneo` | Registro extemporáneo | Sí o no | Flujo | — |
| `id_origen` | Origen del registro | Una línea de texto (255), indexada | Flujo | — |
| `posible_duplicado` | Posible duplicado | Sí o no | Flujo y DGETD | — |
| `registro_por_error` | Registro hecho por error | Sí o no | DGETD | — |

: Columnas del inventario, sección G y columnas de control

Notas de las tablas:

1. **Dos campos, una columna en la ficha.** ET-CAT-01 asigna un solo nombre técnico a pares de campos del área y de la DGETD: `clasificacion` a `C3` y `G4`, `version_vigente` a `D3` y `G7`, y `sistemas_consumidores` a `D1` y `G6` (tabla 5.3.a y anexo A). La regla de este documento: en clasificación y versión, el nombre de ET-CAT-01 va a la columna que queda en la ficha (`G4` y `G7`, como dice ET-CAT-01, tabla 5.3.b), y la respuesta del área se guarda aparte (`clasificacion_area`, `maneja_versiones` y `version_area`). En sistemas consumidores, el nombre de ET-CAT-01 se queda con la respuesta del área (`D1`) y lo que detecta la DGETD va en `sistemas_dgetd` (`G6`); la ficha muestra las dos columnas juntas.
2. **Nombres que no están en ET-CAT-01.** `clasificacion_area`, `maneja_versiones`, `version_area` y `sistemas_dgetd` son propuestas de este documento. ET-CAT-01, sección 5.5, todavía no tiene los subcampos de `D3` ni la regla de pares de la nota 1, aunque el formulario y la plantilla de Excel ya separan esas respuestas (secciones 5.2 y 7.3).
3. **Columnas de control.** `extemporaneo`, `id_origen`, `posible_duplicado` y `registro_por_error` no vienen de un campo de `registro.yaml` ni forman parte de la ficha. `extemporaneo` cumple PR-CAT-04, sección 6.15; `id_origen` es un control técnico (sección 6.3); `posible_duplicado` y `registro_por_error` sirven para filtrar vistas, porque SharePoint no filtra vistas por columnas de varias líneas como `observaciones` (secciones 4.4 y 6.4).
4. **«Por confirmar» en `D3`.** `registro.yaml` define para `D3` solo «Sí (indique cuál es la actual)» y «No», pero el campo acepta «por confirmar». Por ET-CAT-01, sección 5.1, regla 5, un metadato que acepta «por confirmar» y llega vacío se registra como «Por confirmar»; por eso la columna admite ese valor.
5. **Áreas con «Por confirmar».** `propietario` y `custodio` son búsquedas. Para que acepten «Por confirmar», la lista «Áreas y órganos» tiene un elemento con ese nombre y tipo «Valor de control», que no aparece en `A1`.
6. **`fecha_actualizacion` es texto, no fecha.** ET-CAT-01 pide año y mes (`AAAA-MM`). Una columna de fecha de SharePoint exige el día. El flujo valida el formato (sección 6.4).
7. **`folio_registro` y `fecha_recepcion` son del trámite vigente.** Cuando una corrección abre un folio nuevo, el inventario muestra el nuevo; el histórico está en «Registros». Un catálogo solo tiene un trámite abierto a la vez, porque el folio nuevo se abre cuando el anterior está «Confirmado» (ET-CAT-01, sección 7.1, regla 1).
8. **`estatus_inventario` sigue a `registro.yaml`.** Si el equipo aprueba el valor «Anulado» que propone la sección 4.4, se agrega a esta columna después de agregarlo a `registro.yaml` y a ET-CAT-01, sección 7.2.

::: {custom-style="Pendiente"}
**Decisión del equipo, antes del piloto.** Validar los cuatro nombres técnicos nuevos de la nota 2 y la regla de pares de la nota 1, e incorporarlos a ET-CAT-01: los subcampos de `D3` (`maneja_versiones` y `version_area`) en la sección 5.5, y los pares `C3`/`G4`, `D3`/`G7` y `D1`/`G6` en la tabla 5.3.a y el anexo A. Mientras ET-CAT-01 no los incluya, el estándar y los canales usan nombres técnicos distintos para el mismo dato.
:::

## 2.3 Formulario del elemento y vistas

El formulario del elemento se agrupa en secciones A a G con el formato de diseño del formulario de lista («Configurar diseño» > «Cuerpo»), que no requiere licencia adicional. Las columnas de control (`extemporaneo`, `id_origen`, `posible_duplicado` y `registro_por_error`) van en una sección final plegada.

| Vista | Filtro | Para qué |
|:----------------------|:--------------------------------------------|:----------------------------------------|
| Por revisar | `estatus_registro` = Recibido | Bandeja de entrada de la DGETD. Ordenada por `Title`. |
| En revisión por contacto | `estatus_registro` = En revisión, agrupada por contacto DGETD del área | Trabajo de cada persona de contacto. |
| Fichas sin confirmar | `estatus_registro` = Ficha enviada | Seguimiento de confirmaciones. |
| Por confirmar | Algún campo de la ficha con «Por confirmar» | Campos que la DGETD debe completar con el área. |
| Posibles duplicados | `posible_duplicado` = Sí | Depuración (PR-CAT-04, sección 6.10). |
| Pendientes de clave | `Title` empieza con «PEND-» | Red de seguridad: elementos sin clave por una falla (sección 6.6). |
| Ficha | Todas las columnas de A a G, en el orden de `registro.yaml` | Revisión de una ficha completa y exportación. |
| Indicadores | `registro_por_error` = No, agrupada por `estatus_registro` y `estatus_inventario` | Cifras agregadas de PR-CAT-04, capítulo 10. Deja fuera los registros hechos por error (sección 4.4). |

: Vistas de «Inventario de catálogos»

# 3. Lista «Registros» y listas de apoyo

## 3.1 Por qué dos listas y no una

Se usan dos listas relacionadas por búsqueda: «Inventario de catálogos» (un elemento por lista registrada) y «Registros» (un elemento por trámite). Las razones:

1. **Un catálogo tiene varios folios.** El folio identifica el trámite, no el catálogo; una corrección posterior a la confirmación genera un folio nuevo con la misma clave (ET-CAT-01, secciones 6.2 y 7.1). Con una sola lista, el segundo folio no tendría elemento propio.
2. **Cada identificador sale del ID de su propia lista.** La clave sale del ID del inventario y el folio sale del ID de «Registros» (sección 4). Con una sola lista, el folio de una corrección no tendría un ID nuevo del cual derivarse.
3. **Separación entre lo que llegó y la ficha vigente.** «Registros» guarda la respuesta tal como llegó y no se edita. El inventario guarda la ficha que la DGETD revisa y prellena. Así la DGETD puede comprobar lo que el área ya entregó sin volver a pedirlo.
4. **Indicadores por trámite.** PR-CAT-04, capítulo 10, mide días de recepción a ficha y de ficha a confirmación por trámite.

La DGETD trabaja solo en el inventario. «Registros» lo escriben los flujos; las personas lo consultan.

## 3.2 Configuración

- Mismas reglas que el inventario (sección 2.1): `Title` como folio de registro, con valores únicos e indexado; historial de versiones; sin datos adjuntos; columnas de elección sin valor predeterminado.
- Índices: `Title`, `id_origen` (con valores únicos), `anio_folio` y `inventario`.
- La búsqueda `inventario` muestra además `nombre_oficial` y `area_registra` del catálogo. Comportamiento al eliminar el catálogo: «Restringir eliminación», para que nadie borre un catálogo con trámites.

## 3.3 Columnas

| Nombre interno | Nombre visible | Tipo y valores | Oblig. | Campo o fuente |
|:----------------------------------------------|:------------------------|:----------------------------------|:---------------|:----------------------------|
| `Title` | Folio de registro | Una línea de texto, valores únicos: `RC-AAAA-NNNN` (sección 4) | Flujo | `G1` |
| `inventario` | Catálogo | Búsqueda en «Inventario de catálogos» (`Title`) | Flujo | `B1` · `G2` |
| `anio_folio` | Año del folio | Número, sin decimales | Flujo | `G1` (año de recepción) |
| `fecha_recepcion` | Fecha de recepción | Fecha y hora, solo fecha | Flujo | `G3` |
| `canal` | Canal | Elección: Formulario en línea · Plantilla de Excel · Registro acompañado | Flujo | PR-CAT-04, sección 6.5 |
| `es_correccion` | Corrección de un registro confirmado | Sí o no | Flujo | ET-CAT-01, sección 7.1, regla 1 |
| `es_contingencia` | Ficha de contingencia del día 75 | Sí o no | Flujo | PR-CAT-04, sección 6.14 (sección 5.5) |
| `estatus_registro` | Estatus del registro | Elección: Recibido · En revisión · Ficha enviada · Confirmado | Flujo | `G8` (copia del inventario) |
| `confirmacion_area` | Confirmación del área (nombre, fecha) | Una línea de texto (255) | Flujo | `G11` (copia del inventario) |
| `fecha_ficha_enviada` | Fecha de envío de la ficha | Fecha y hora | Flujo | PR-CAT-04, capítulo 10 |
| `fecha_confirmacion` | Fecha de confirmación | Fecha y hora | Flujo | PR-CAT-04, capítulo 10 |
| `persona_captura` | Cuenta que envió el registro | Una línea de texto (254) | Flujo | Forms (correo de quien responde) o autor del archivo |
| `id_origen` | Origen del registro | Una línea de texto (255), valores únicos | Flujo | Control técnico (sección 6.3) |
| `archivo_origen` | Archivo de origen | Hipervínculo | Flujo | Solo plantilla de Excel |
| `respuesta_original` | Respuesta original | Varias líneas de texto, sin formato | Flujo | `A1` a `F5` tal como llegaron, en JSON |
| `acuse_enviado` | Acuse enviado | Sí o no | Flujo | Control técnico |
| `fecha_acuse` | Fecha y hora del acuse | Fecha y hora | Flujo | Control técnico |
| `error_flujo` | Error del flujo | Varias líneas de texto, sin formato | Flujo | Control técnico |
| `notas_tramite` | Notas del trámite | Varias líneas de texto, sin formato | DGETD | Uso interno |

: Columnas de la lista «Registros»

::: {custom-style="Pendiente"}
**Por confirmar.** (1) Los valores de `canal` vienen de PR-CAT-04, sección 6.5; no están en `registro.yaml`. Si se aceptan, conviene agregarlos a `registro.yaml` para que la plantilla y los indicadores los lean de ahí. (2) Las fichas de contingencia del día 75 las captura la DGETD y quedarían como «Registro acompañado». Para que no distorsionen el indicador «Registros por canal» (PR-CAT-04, capítulo 10) ni la medición de capacidad del registro acompañado, este documento las marca con `es_contingencia` = Sí y el indicador las informa aparte. La alternativa es un cuarto valor de `canal`, «Contingencia», que obliga a ajustar PR-CAT-04, sección 6.5, donde los canales son tres.
:::

## 3.4 Lista «Áreas y órganos»

Es la lista oficial de áreas y órganos que alimenta `A1`, `C1` y `C2` en los tres canales. ET-CAT-01, sección 5.5, deja pendiente de qué fuente sale y quién la mantiene.

| Nombre interno | Nombre visible | Tipo | Notas |
|:----------------------------------------------|:------------------------|:------------------------|:------------------------------------|
| `Title` | Área u órgano (nombre oficial completo) | Una línea de texto, valores únicos | El mismo texto que la opción de Forms y que la hoja «Áreas» de la plantilla. |
| `tipo_area` | Tipo | Elección: Área administrativa · Órgano jurisdiccional · Valor de control | «Valor de control» solo para el elemento «Por confirmar». |
| `activa` | Activa | Sí o no | Las inactivas no se ofrecen en el formulario. |
| `bloque` | Bloque de áreas | Una línea de texto | Agrupa áreas por persona de contacto. |
| `contacto_dgetd` | Persona de contacto DGETD | Persona | Nombre que aparece en el acuse (compromiso de PR-CAT-04, sección 6.7). |
| `titular_correo` | Correo de la persona titular | Una línea de texto (254) | Sale de la designación de enlace. Se usa para la copia del acuse. |
| `enlace_nombre_designado` | Persona enlace designada: nombre | Una línea de texto (150) | Salen de la designación de enlace. Sirven para los vínculos prellenados (sección 5.3). |
| `enlace_puesto_designado` | Persona enlace designada: puesto | Una línea de texto (150) | Sale de la designación de enlace. |
| `enlace_correo_designado` | Persona enlace designada: correo | Una línea de texto (254) | Sale de la designación de enlace. |
| `enlace_ext_designado` | Persona enlace designada: extensión | Una línea de texto (10) | Sale de la designación de enlace. |
| `liga_prellenada` | Vínculo prellenado | Hipervínculo | Se envía a la persona enlace con el kit. |

: Columnas de la lista «Áreas y órganos»

::: {custom-style="Pendiente"}
**Por confirmar.** `A3` solo pide nombre y puesto de la persona titular; no pide su correo. La copia del acuse se envía al `titular_correo` que la DGETD registra con la designación de enlace (PR-CAT-04, actividades 8 y 9). Si falta, el acuse sale sin copia y el flujo lo anota en `notas_tramite`. La alternativa es agregar un subcampo de correo a `A3` en `registro.yaml`.
:::

## 3.5 Lista «Parámetros»

Una lista de dos columnas (`Title` como nombre del parámetro y `valor` como texto) evita escribir valores fijos dentro de los flujos.

| Parámetro | Valor inicial |
|:----------------------------------|:------------------------------------------------------------|
| `fecha_cierre_registro` | [viernes 15 de enero de 2027, por confirmar]{custom-style="Marcador"}, como `2027-01-15` |
| `buzon_registro` | Dirección del buzón compartido |
| `contacto_general` | [correo, extensión y horario de la asesoría DGETD]{custom-style="Marcador"} |
| `plazo_ficha` | [plazo por definir según capacidad de la DGETD]{custom-style="Marcador"} |
| `plazo_dudas` | [plazo por definir según capacidad de la DGETD]{custom-style="Marcador"} |
| `dominio_institucional` | [dominio institucional]{custom-style="Marcador"}, para validar correos |
| `grupo_captura_dgetd` | Identificador del grupo de M365 cuyas personas hacen registro acompañado |
| `liga_formulario` | [liga al formulario de registro]{custom-style="Marcador"} |
| `liga_sharepoint` | [liga a la carpeta de SharePoint para plantillas de Excel]{custom-style="Marcador"} |
| `captura_diferida_cuenta` | Vacío. Correo de la persona de la DGETD que hace una captura diferida (sección 5.5) |
| `captura_diferida_tipo` | Vacío. «Plan B de plantilla» o «Contingencia» |
| `captura_diferida_fecha` | Vacío. Fecha de recepción real, como `AAAA-MM-DD` |
| `captura_diferida_archivo` | Vacío. Liga al archivo de origen, solo en el plan B de la plantilla |

: Parámetros que leen los flujos

# 4. Clave de catálogo y folio de registro

## 4.1 La regla

- **Clave de catálogo:** `CAT-` seguido del ID del elemento en «Inventario de catálogos», con 4 dígitos y ceros a la izquierda. El elemento con ID 42 recibe `CAT-0042`; el ID 10000 recibe `CAT-10000`.
- **Folio de registro:** `RC-`, el año de recepción y la posición del trámite dentro de ese año en «Registros», con 4 dígitos. La posición es el número de elementos de «Registros» con el mismo `anio_folio` y un ID menor o igual al del trámite.

Expresiones de Power Automate (los nombres de acción son los de la sección 6.2):

```text
Clave:   concat('CAT-', formatNumber(int(outputs('Crear_catalogo')?['body/ID']), '0000'))

Folio:   concat('RC-', string(variables('anio')), '-',
                formatNumber(length(outputs('Contar_tramites_del_anio')?['body/value']), '0000'))

Contar_tramites_del_anio (SharePoint, Obtener elementos, lista «Registros»):
         Consulta de filtro:  anio_folio eq @{variables('anio')} and ID le @{outputs('Crear_tramite')?['body/ID']}
         Paginación activada, umbral 5000; limitar columnas a una vista que solo tenga ID.
```

## 4.2 Por qué el ID de SharePoint

1. **Evita la carrera del «último número más uno».** Si el flujo leyera la última clave y le sumara 1, dos envíos al mismo tiempo leerían el mismo número y saldrían dos claves iguales. SharePoint asigna el ID al guardar el elemento: dos envíos simultáneos reciben ID distintos sin que el flujo coordine nada.
2. **Es único y correlativo dentro de la lista.** SharePoint no reutiliza un ID, ni siquiera el de un elemento eliminado. Eso cumple la regla de no reutilización (ET-CAT-01, sección 6.1, regla 5).
3. **No tiene significado.** El número solo dice el orden de creación. Cumple la neutralidad que ET-CAT-01, sección 6.1, regla 3, toma del art. 7 fr. I c) de los Lineamientos.
4. **No requiere una lista de contadores** ni bloqueos, que con conectores estándar no se pueden hacer de forma atómica.

Para el folio, el conteo dentro del año es estable por la misma razón: solo cuenta elementos con ID menor o igual, que ya existen cuando el flujo cuenta, y `anio_folio` se escribe al crear el trámite y no cambia. Dos trámites del mismo año con ID 120 y 121 siempre dan conteos distintos.

Ejemplo ilustrativo: los trámites de 2026 tienen ID 1 a 40 y reciben `RC-2026-0001` a `RC-2026-0040`. El primer trámite de enero, con ID 41 y `anio_folio` 2027, cuenta 1 elemento y recibe `RC-2027-0001`. Una plantilla subida el 31 de diciembre que se procesa el 4 de enero conserva `anio_folio` 2026 (año de la fecha de recepción); si recibe el ID 57, cuenta 41 elementos de 2026 y recibe `RC-2026-0041`, sin chocar con nadie.

Tres protecciones adicionales:

- `Title` tiene «Aplicar valores únicos» en las dos listas. Si por cualquier causa se repitiera una clave o un folio, SharePoint rechaza la actualización, el flujo falla y avisa (sección 6.5). Nunca queda un duplicado guardado.
- REG-01 y REG-02 tienen el control de simultaneidad del desencadenador en 1: procesan un envío a la vez. No es necesario para la regla, pero reduce todavía más el riesgo y hace que el orden de las claves siga el orden de llegada.
- Al crear el elemento, el flujo escribe en `Title` un valor temporal único, `PEND-` seguido de `id_origen`, y lo reemplaza por la clave o el folio en el paso siguiente. Así ningún elemento queda con `Title` vacío y la vista «Pendientes de clave» muestra los que no terminaron.

::: {custom-style="Pendiente"}
**Por confirmar.** ET-CAT-01, sección 6.1, regla 2, dice que la clave se asigna «en el orden en que llegan los registros». Con esta regla, el orden es el de creación del elemento. Una plantilla de Excel se procesa minutos después de subirla, así que un formulario enviado en esos minutos puede recibir una clave menor. La fecha de recepción no cambia. Conviene ajustar la redacción de ET-CAT-01 a «en el orden en que el inventario los recibe».
:::

## 4.3 Qué no hacer

- No usar columnas calculadas con `[ID]`: SharePoint no llena el ID en una columna calculada al crear el elemento.
- No recalcular claves ni folios guardados. Si alguna vez la lista se migra, la clave viaja como texto en `Title`; el ID de la lista nueva ya no coincide y no importa.
- No volver a crear la lista de producción ni crear otra con el mismo propósito: el ID empezaría en 1 y repetiría claves ya entregadas.
- No crear elementos de prueba en producción.

## 4.4 Qué pasa si se borra un elemento

Nunca se borra. Si alguien lo borrara:

- **En el inventario,** la clave queda sin ficha y el catálogo desaparece del inventario, aunque el área tenga el acuse. SharePoint no reutiliza el ID, así que la clave no se repite, pero se pierde la constancia.
- **En «Registros»,** el conteo del año baja en 1. Los folios ya guardados no cambian, pero un flujo que todavía no guardaba su folio, o que se vuelve a ejecutar, podría calcular uno repetido. La regla de valores únicos lo detiene y el flujo avisa.
- **Remedio:** restaurar el elemento desde la papelera de reciclaje del sitio, que conserva el ID, en lugar de crear uno nuevo.

Para que no ocurra:

- El equipo de registro trabaja con un nivel de permiso «Colaborar sin eliminar» (copia de «Colaborar» sin el permiso «Eliminar elementos»). Solo las personas propietarias del sitio pueden eliminar, y no lo hacen.
- Un registro hecho por error se resuelve con estatus, no se borra. Si repite otra lista, pasa a «Duplicado» y `observaciones` anota la clave con la que coincide (ET-CAT-01, sección 6.1, regla 6).
- Si no corresponde a ninguna lista real (por ejemplo, un envío de prueba o una lista que el área no lleva), no se usa «Retirado». Ese valor significa que una lista real se dejó de usar de forma controlada (artículo 9, fracción VIII, de los Lineamientos; ET-CAT-01, sección 7.2) y contaría en las cifras de retiro que se informen al Comité. Mientras se decide el tratamiento definitivo, la DGETD deja el elemento en «Registrado», marca `registro_por_error` = Sí y anota en `observaciones` «Registro hecho por error» con la fecha y la persona que lo detectó. La clave no se reutiliza. La vista «Indicadores», las cifras agregadas y el informe de cierre dejan fuera esos elementos.

::: {custom-style="Pendiente"}
**Decisión del equipo, antes del piloto.** Se propone agregar a `registro.yaml` (`estatus_inventario`) y a ET-CAT-01, sección 7.2, el valor «Anulado», con la descripción «Registro hecho por error; no corresponde a ninguna lista. Su clave no se reutiliza.», como estatus final y con la transición Registrado → Anulado, que ejecuta la DGETD con aviso al área. Conviene resolverlo antes del piloto, que se hace en producción (capítulo 11). Mientras no se apruebe, aplica el tratamiento provisional de arriba.
:::

# 5. Formulario de Microsoft Forms

## 5.1 Configuración del formulario

| Opción | Valor | Por qué |
|:--------------------------|:------------------------|:------------------------------------------------------|
| Dónde se crea | Forms de grupo, en el grupo de M365 de la DGETD | El formulario no depende de una persona. Si alguien lo creó en su cuenta, se mueve al grupo antes de publicar la liga. |
| Quién puede responder | Solo las personas de mi organización | Exige cuenta institucional y deja el correo de quien responde. |
| Registrar nombre | Activado | Da `persona_captura` y permite detectar el registro acompañado. |
| Una respuesta por persona | Desactivado | La persona enlace hace un envío por lista. |
| Editar respuestas después de enviar | Desactivado | El flujo solo se dispara con respuestas nuevas; una edición no llegaría al inventario. Las correcciones van por la DGETD (sección 6.6). |
| Recibo de respuesta de Forms | Desactivado | El acuse con folio y clave lo envía REG-01. |
| Notificación de cada respuesta | Desactivada | Evita correos al grupo por cada envío. |
| Fecha de inicio y fin | Sin fecha de fin | Después del cierre se reciben registros extemporáneos (PR-CAT-04, sección 6.15). |
| Tema | Fondo liso, sin imagen, con contraste AA | Sección 9.3. |
| Barra de progreso | Activada | La persona sabe en qué sección va. |

: Configuración del formulario de registro

**Texto de introducción del formulario** (descripción, arriba de la primera sección):

> Registre aquí cada lista que lleve su área y que otra área, un sistema, un reporte o un trámite consulte o copie. Haga un envío por cada lista. Pedimos datos sobre la lista, no la lista: no adjunte su contenido ni datos personales. Registrar no publica la lista, no cambia quién la administra ni modifica ningún sistema. «Por confirmar» es una respuesta válida en las preguntas que lo ofrecen. Si se le acerca la fecha límite, envíe lo que sepa: el área, el nombre y la descripción de la lista son indispensables. Fecha límite: [viernes 15 de enero de 2027, por confirmar]{custom-style="Marcador"}. Dudas: [correo, extensión y horario de la asesoría DGETD]{custom-style="Marcador"}. Aviso de privacidad: [liga al aviso de privacidad simplificado, por definir con la unidad de transparencia]{custom-style="Marcador"}.

**Mensaje de agradecimiento** (al enviar):

> Recibimos su registro. Le enviaremos el acuse con el folio y la clave de catálogo al correo de la persona enlace, con copia a la persona titular. Si su área lleva otra lista, abra de nuevo su liga y haga un envío por ella.

El mensaje no da el folio porque Forms no puede mostrar un dato que calcula el flujo.

## 5.2 Secciones y preguntas

- El **título** de cada pregunta es la `pregunta` de `registro.yaml` sin cambios. Los subcampos usan el texto de la plantilla de Excel (`build/plantilla_excel.py`), para que los tres canales digan lo mismo.
- El **subtítulo** de cada pregunta es la `ayuda` de `registro.yaml` sin cambios, salvo donde la columna «Subtítulo» dice otra cosa.
- **Obligatoriedad.** En las preguntas de opción que aceptan «por confirmar», la opción «Por confirmar» (o «No estoy seguro», que se guarda como «Por confirmar») es una alternativa explícita y la pregunta es obligatoria en Forms. En las preguntas de texto que aceptan «por confirmar», Forms no puede ofrecer una opción; la pregunta es no obligatoria en Forms y el flujo guarda «Por confirmar» si llega vacía (ET-CAT-01, sección 5.1, regla 5).
- Las preguntas de área son de **opción con lista desplegable**. Las opciones se pegan desde la columna `Title` de «Áreas y órganos» (solo las activas).

| No. | ID | Pregunta (título) | Tipo en Forms | Oblig. | Subtítulo, ramificación y notas |
|:--------|:--------|:--------------------------------|:----------------------|:-----------|:--------------------------------------|
| | **A** | **Sección «Quién registra»** | Sección | — | Descripción: «Datos de su área y de las personas que responden por este registro.» |
| 1 | `A1` | ¿Qué área o qué órgano jurisdiccional registra esta lista? | Opción, lista desplegable | Sí | Opciones: áreas y órganos activos, sin «Por confirmar». Llega prellenada en el vínculo del área. |
| 2 | `A2` | ¿Quién es la persona de contacto para este registro? Escriba su nombre completo. | Texto, respuesta corta | Sí | Subtítulo: `ayuda` de `A2`. Prellenada. |
| 3 | `A2` | Puesto de la persona enlace. | Texto, respuesta corta | Sí | Prellenada. |
| 4 | `A2` | Correo institucional de la persona enlace. | Texto, respuesta corta | Sí | Forms no valida correos; lo valida el flujo. Prellenada. |
| 5 | `A2` | Extensión telefónica de la persona enlace. | Texto, respuesta corta | Sí | Prellenada. |
| 6 | `A3` | ¿Qué persona titular del área conoce y respalda este registro? Escriba el nombre completo de la persona titular. | Texto, respuesta corta | Sí | Subtítulo: `ayuda` de `A3`. Prellenada. |
| 7 | `A3` | Puesto de la persona titular. | Texto, respuesta corta | Sí | Prellenada. |
| | **B** | **Sección «Su lista»** | Sección | — | Descripción: la `pregunta` y la `ayuda` de `B1` («No tiene que responder: la DGETD asigna la clave…»). `B1` no es pregunta. |
| 8 | `B1b` | (Opcional) ¿Su lista ya tiene una clave o código interno? Escríbalo aquí. | Texto, respuesta corta | No | |
| 9 | `B2` | ¿Cómo se llama esta lista? Escriba el nombre completo, sin siglas. | Texto, respuesta corta | Sí | |
| 10 | `B3` | ¿Qué contiene esta lista y para qué la usan? | Texto, respuesta larga | Sí | |
| | **C** | **Sección «Quién decide y quién la mantiene»** | Sección | — | Descripción: la `nota` de la sección C. |
| 11 | `C1` | ¿Qué área decide qué entra y qué sale de esta lista, y con qué reglas? | Opción, lista desplegable | Sí | Opciones: «Por confirmar» primero y luego solo las áreas administrativas de la lista oficial. Llega prellenada con el área de `A1` solo si es área administrativa; si `A1` es un órgano jurisdiccional, llega en «Por confirmar». |
| 12 | `C2` | ¿Qué área mantiene la lista al día en la práctica: da de alta, corrige y da de baja? | Opción, lista desplegable | Sí | Opciones: «Por confirmar» y solo las áreas administrativas de la lista oficial. Sin prellenado. |
| 13 | `C2` | Persona de contacto del área que mantiene la lista. | Texto, respuesta corta | No | Subtítulo: «Indique nombre, puesto, correo institucional y extensión de una persona del área que mantiene la lista.» |
| 14 | `C2b` | (Opcional) ¿Le interesaría que la DGETD se encargue del mantenimiento operativo de esta lista? | Opción | No | Sí · No · No sé. |
| 15 | `C3` | ¿A qué se parece más su lista? | Opción | Sí | Opciones con el texto de F-CAT-01 (pregunta `C3`) y de la tabla de traducción de esta sección. «No estoy seguro» se guarda como «Por confirmar». |
| | **D** | **Sección «Quién la usa y cada cuánto cambia»** | Sección | — | |
| 16 | `D1` | ¿Qué sistemas, aplicaciones, archivos o reportes usan esta lista? | Texto, respuesta larga | No | Vacía se guarda como «Por confirmar». |
| 17 | `D1` | (casilla de `D1`) | Opción, varias respuestas, una sola opción | No | Título y opción: «No conozco todos. Que la DGETD complete la lista.» |
| 18 | `D2` | En la práctica, ¿cada cuánto se agrega, quita o corrige algo en esta lista? | Opción | Sí | Los 10 valores de `frecuencia`. Ramificación: «Cada vez que ocurre un cambio» va a la 19; las demás van a la 20. |
| 19 | `D2` | Si eligió «Cada vez que ocurre un cambio», ¿qué hecho dispara el cambio? | Texto, respuesta corta | No | Subtítulo: «Por ejemplo: cuando se crea o se readscribe un órgano.» |
| 20 | `D3` | ¿Su lista maneja versiones numeradas (por ejemplo, v2.3)? | Opción | Sí | Sí (indique cuál es la actual) · No · Por confirmar. Ramificación: «Sí…» va a la 21; las demás van a la 22. |
| 21 | `D3` | Si respondió «Sí», ¿cuál es la versión actual? | Texto, respuesta corta | No | Subtítulo: «Escriba la versión como la usan hoy, por ejemplo v2.3.» |
| 22 | `D4` | ¿Cuándo fue la última vez que se agregó, quitó o corrigió algo en esta lista? | Texto, respuesta corta | No | Subtítulo: `ayuda` de `D4` más «Escriba año y mes así: 2026-09 (formato AAAA-MM).» No se usa la pregunta de fecha de Forms porque exige el día. Vacía se guarda como «Por confirmar». |
| 23 | `D4` | (casilla de `D4`) | Opción, varias respuestas, una sola opción | No | Título y opción: «Está en un sistema; que la DGETD obtenga la fecha.» |
| | **E** | **Sección «Quién puede verla»** | Sección | — | |
| 24 | `E1` | ¿Quién debería poder consultar esta lista? | Opción | Sí | Opciones con el texto de F-CAT-01 (pregunta `E1`) y de la tabla de traducción de esta sección. |
| 25 | `E2` | ¿La lista contiene datos personales, como nombres, RFC, CURP, domicilios particulares o teléfonos? | Opción | Sí | Sí · No · No sé. |
| | **F** | **Sección «Para entender mejor su lista (opcional)»** | Sección | — | Descripción: la `nota` de la sección F. |
| 26 | `F1` | ¿Dónde está hoy la lista? | Opción | No | Valores de `F1`. |
| 27 | `F2` | ¿Cuántos renglones (elementos) tiene, aproximadamente? | Opción | No | Valores de `F2`. |
| 28 | `F3` | ¿Cada renglón de la lista tiene una clave? | Opción | No | Valores de `F3`. |
| 29 | `F4` | ¿Sabe de otra área que lleve una lista parecida? | Texto, respuesta corta | No | Sin `ayuda` en `registro.yaml`; sin subtítulo. |
| 30 | `F5` | ¿Qué problema le causa hoy esta lista? | Texto, respuesta larga | No | |

: Secciones y preguntas del formulario, en orden

Cada sección repite al final de su descripción la misma línea de ayuda: «¿Dudas? Asesoría DGETD: [correo, extensión y horario de la asesoría DGETD]{custom-style="Marcador"}». WCAG 2.2 pide que la ayuda esté en el mismo lugar en cada página (criterio 3.2.6).

| Campo | Texto de la opción en Forms (F-CAT-01) | Valor que guarda el flujo |
|:----------|:------------------------------------------------------------|:----------------------|
| `C3` | Una lista de personas, lugares o cosas de la institución (Entidades): órganos jurisdiccionales, inmuebles, cargos. | Entidades |
| `C3` | Una lista de opciones para clasificar información (Clasificación): tipos de documento, sentidos de resolución, entidades federativas. | Clasificación |
| `C3` | Valores de configuración que usa un sistema (Parámetros): plazos, montos, porcentajes, umbrales. | Parámetros |
| `C3` | Una tabla que une dos listas (Relación): qué órgano pertenece a qué circuito. | Relación |
| `C3` | No estoy seguro | Por confirmar |
| `E1` | Pública. Cualquier persona puede consultarla. | Pública |
| `E1` | Interna. Todo el personal del OAJ puede consultarla. | Interna |
| `E1` | Restringida. Solo ciertas áreas o personas pueden consultarla. | Restringida |
| `E1` | Clasificada. Contiene información reservada o confidencial conforme a la normativa de transparencia. | Clasificada |
| `E1` | Por confirmar. No estoy seguro. | Por confirmar |

: Opciones de Forms que el flujo traduce a valores de registro.yaml

En las demás preguntas de opción, el texto en Forms es exactamente el valor de `registro.yaml` y no hay traducción.

::: {custom-style="Pendiente"}
**Decisión del equipo.** (1) La propuesta del kit habla de «5 pasos cortos»; aquí hay 5 secciones obligatorias (A a E) y una opcional (F). (2) Para enviar, la persona pasa por la sección F aunque no la responda. Si en el piloto eso estorba, se agrega al final de E una pregunta de navegación («¿Quiere responder 5 preguntas opcionales?») que salte al final; no se guarda.
:::

## 5.3 Vínculos prellenados

Los vínculos prellenados cumplen dos compromisos a la vez: prellenar lo que la DGETD ya conoce y no volver a pedir lo que el área ya entregó. Además reducen la entrada repetida que WCAG 2.2 pide evitar (criterio 3.3.7), porque la persona enlace no reescribe sus datos en cada envío.

1. En Forms, «…» > «Obtener vínculo previamente rellenado». Llenar `A1`, `A2`, `A3` y `C1` con datos de prueba y copiar la liga.
2. Identificar en la liga el parámetro de cada pregunta.
3. En «Áreas y órganos», armar la liga de cada área con los datos de la designación de enlace (columnas `*_designado`) y guardarla en `liga_prellenada`. Se puede hacer con una fórmula de Excel sobre la lista exportada o con un flujo manual.
4. Enviar a cada persona enlace su liga con el kit. La persona usa la misma liga para cada lista que registre.

La persona puede cambiar los valores prellenados. El formato de los parámetros no está documentado por Microsoft y puede cambiar: se prueba antes del piloto y otra vez antes de enviar las ligas.

## 5.4 Límites de Forms que el diseño considera

| Límite | Consecuencia | Cómo se resuelve |
|:--------------------------------|:--------------------------------|:----------------------------------------|
| Un envío registra una lista; Forms no tiene secciones repetibles. | Un área con varias listas hace varios envíos. | Liga prellenada reutilizable; plantilla de Excel para más de 5 listas. |
| No hay validación entre preguntas ni obligatoriedad condicional. | No se puede exigir `D1` solo si la casilla no está marcada. | `D1` es opcional en Forms y el flujo aplica la regla de «Por confirmar». |
| No hay validación de formato en texto, salvo números. | Correos y fechas `AAAA-MM` pueden llegar mal escritos. | El flujo valida y anota en `observaciones` (sección 6.4). |
| La ramificación solo avanza y solo sale de preguntas de opción. | No hay «regresar a». | Las preguntas condicionales (19 y 21) van justo después de su pregunta de opción. |
| Las opciones no se leen de SharePoint. | La lista oficial se copia a mano en `A1`, `C1` y `C2`. | Un responsable actualiza las opciones cuando cambia «Áreas y órganos» y lo anota. |
| Número máximo de opciones por pregunta y longitud máxima de las respuestas. | La lista oficial con todos los órganos jurisdiccionales puede rebasar el límite. `B3` admite 1,000 caracteres y `D1` 2,000 en ET-CAT-01. | Verificar los límites vigentes en el inquilino (sección 10). Si la lista rebasa el límite, `A1` se divide en dos preguntas por tipo, con ramificación. El flujo no corta textos largos; los guarda completos y lo anota. |
| Guardar y seguir después. | No se debe prometer. | La persona prepara sus respuestas con F-CAT-01 en Word. Se prueba en el piloto. |
| Las respuestas quedan también en Forms. | Hay una segunda copia de los datos personales de enlaces y titulares. | Regla de conservación (sección 9.2). |
| El formulario no puede mostrar el folio. | El folio llega solo por correo. | Mensaje de agradecimiento de la sección 5.1. |

: Límites de Forms y cómo se resuelven

## 5.5 Registro acompañado

La DGETD captura en el mismo formulario, con la liga prellenada del área, mientras la persona enlace responde por Teams o por teléfono.

1. La persona de la DGETD abre la liga prellenada del área. Si el área no tiene liga, elige el área en `A1` y escribe los datos de la persona enlace que le dicte el área.
2. Lee cada pregunta tal como está y anota lo que el área responde. Si el área no sabe un dato, elige «Por confirmar» o deja vacía la pregunta de texto. No completa con suposiciones: el prellenado se hace después, en la revisión.
3. Al enviar, REG-01 detecta que la cuenta que respondió pertenece al grupo de captura de la DGETD (`grupo_captura_dgetd`) y guarda `canal` = «Registro acompañado». El acuse va al correo de la persona enlace (`A2`), no a la cuenta de la DGETD.
4. La propuesta del kit prevé sesiones de 30 minutos; la duración real se mide en el piloto.

La ficha prellenada de contingencia del día 75 (PR-CAT-04, sección 6.14) no se crea en el inventario antes de que el área la devuelva. Cuando el área la devuelve, la DGETD la captura en el formulario como captura diferida de tipo «Contingencia». Así la clave se asigna cuando el registro se tiene por presentado, la fecha de recepción es la de la devolución y el trámite queda marcado con `es_contingencia` = Sí.

### Captura diferida

Dos casos se capturan en el formulario con datos que el área entregó antes: la ficha de contingencia (arriba) y el plan B de la plantilla (sección 7.4). En los dos, la fecha de recepción tiene que ser la real y no la del envío del formulario, porque de ella salen el año del folio (ET-CAT-01, sección 6.2, regla 1) y la marca de extemporáneo.

1. Antes de capturar, la persona de la DGETD escribe en «Parámetros» su correo en `captura_diferida_cuenta`, el tipo en `captura_diferida_tipo`, la fecha de recepción real en `captura_diferida_fecha` y, en el plan B, la liga al archivo en `captura_diferida_archivo`.
2. REG-01 usa esos valores solo si la cuenta que respondió es `captura_diferida_cuenta` (paso 6 de la sección 6.2). Toma `fechaRecepcion` y `anio` de `captura_diferida_fecha` antes de crear el trámite y de calcular el folio. Con «Plan B de plantilla» guarda `canal` = «Plantilla de Excel» y `archivo_origen`; con «Contingencia» guarda `canal` = «Registro acompañado» y `es_contingencia` = Sí. En `notas_tramite` anota el tipo y la fecha que usó.
3. Al terminar, la persona vacía los cuatro parámetros. Mientras `captura_diferida_tipo` tenga valor, REG-05 lo recuerda cada día en el canal de alertas, para que ningún registro acompañado normal reciba una fecha que no es suya.

## 5.6 Formulario «Mi órgano no lleva listas propias»

La lista de verificación para órganos jurisdiccionales ofrece confirmar con un clic que el órgano no lleva listas propias ([liga para confirmar, por definir]{custom-style="Marcador"}).

- Forms de grupo, solo cuenta institucional, una pregunta: el órgano, como opción de lista desplegable, prellenada en la liga de cada órgano. Mensaje de agradecimiento: «Gracias. No tiene que hacer nada más.»
- No tiene flujo ni genera seguimiento. Las respuestas solo se cuentan al cierre, en cifras agregadas.

# 6. Flujos de Power Automate

## 6.1 Inventario de flujos

| Flujo | Desencadenador | Qué hace |
|:--------------------------|:------------------------------------|:--------------------------------------------|
| REG-01 Registro desde formulario | Forms: «Cuando se envía una respuesta nueva» | Crea catálogo y trámite, calcula clave y folio, envía acuse. |
| REG-02 Registro desde plantilla | SharePoint: «Cuando se crea un archivo (solo propiedades)» en «Recepción de plantillas» | Lo mismo por cada renglón; mueve el archivo; un acuse por archivo (sección 7). |
| REG-03 Ficha de confirmación | SharePoint: «Para un elemento seleccionado» en el inventario | Envía la ficha y registra la confirmación (sección 8). |
| REG-04 Sincronizar estatus | SharePoint: «Cuando se crea o modifica un elemento» en el inventario | Copia `estatus_registro` y `confirmacion_area` al trámite vigente en «Registros». |
| REG-05 Revisión diaria | Periódico, cada día hábil a las 8:00 | Completa claves y folios pendientes, reenvía acuses no enviados y avisa errores. |
| REG-06 Folio de corrección | SharePoint: «Para un elemento seleccionado» en el inventario | Abre un folio nuevo para un catálogo «Confirmado» que el área pide corregir. |

: Flujos del registro

## 6.2 REG-01 paso a paso

Todo el cuerpo del flujo, de los pasos 3 a 14, va dentro de un ámbito «Intentar». El manejo de errores está en la sección 6.5.

| Paso | Acción (conector) | Configuración |
|:--------|:------------------------------|:------------------------------------------------------------------|
| 1 | Cuando se envía una respuesta nueva (Microsoft Forms) | Formulario de registro. Si el formulario de grupo no aparece en la lista, escribir su identificador como valor personalizado (sale de la URL del formulario en modo de edición). Control de simultaneidad activado, grado 1. |
| 2 | Obtener los detalles de la respuesta (Microsoft Forms) | Id. de respuesta del desencadenador. |
| 3 | Inicializar variables | `idOrigen` = `concat('FORMS-', <Id. de respuesta>)`. `fechaRecepcion` = fecha de envío convertida a hora de la Ciudad de México. `anio` = año de `fechaRecepcion`. `notas` = cadena vacía. |
| 4 | Obtener elementos (SharePoint) en «Parámetros» | Lee todos los parámetros a un objeto. |
| 5 | Obtener elementos (SharePoint) en «Áreas y órganos», tres veces | Filtro por `Title` igual a la respuesta de `A1`, de `C1` y de `C2`. Si no hay coincidencia, se usa el elemento «Por confirmar» y se agrega una nota. |
| 6 | Enumerar miembros del grupo (Office 365 Groups) | Grupo `grupo_captura_dgetd`. Si el correo de quien respondió está en el grupo, `canal` = «Registro acompañado»; si no, «Formulario en línea». Captura diferida: si además ese correo es `captura_diferida_cuenta` y `captura_diferida_tipo` tiene valor, reemplaza `fechaRecepcion` y `anio` con `captura_diferida_fecha` y fija `canal`, `es_contingencia` y `archivo_origen` según el tipo (sección 5.5). |
| 7 | Redactar «Ficha normalizada» (Datos: Redactar) | Objeto con los nombres técnicos de la sección 2.2 y los valores ya traducidos y validados (sección 6.4). |
| 8 | Obtener elementos en el inventario, filtro `id_origen eq '<idOrigen>'` | Si ya existe, se usa ese elemento y se salta el paso 9. |
| 9 | Crear elemento (SharePoint) en el inventario | Todas las columnas de la ficha normalizada. `Title` = `concat('PEND-', idOrigen)`. `estatus_registro` = Recibido. `estatus_inventario` = Registrado. `fecha_recepcion`. `extemporaneo` = `fechaRecepcion` posterior a `fecha_cierre_registro`. `version_vigente` = `version_area` si `D3` es «Sí…»; «1.0» si es «No»; vacío en otro caso. |
| 10 | Obtener elementos en «Registros», filtro `id_origen eq '<idOrigen>'` | Si ya existe, se usa ese elemento y se salta el paso 11. |
| 11 | Crear elemento (SharePoint) en «Registros» | `Title` = `concat('PEND-', idOrigen)`. `inventario` = ID del paso 9. `anio_folio`, `fecha_recepcion`, `canal`, `persona_captura`, `id_origen`. `es_correccion` = No. `es_contingencia` según el paso 6. `archivo_origen` si lo hay. `estatus_registro` = Recibido. `respuesta_original` = `string(body('Obtener_los_detalles_de_la_respuesta'))`. |
| 12 | Calcular clave y folio | Si `Title` del catálogo empieza con «PEND-», calcular la clave; si `Title` del trámite empieza con «PEND-», contar y calcular el folio (sección 4.1). |
| 13 | Actualizar elemento, dos veces | Trámite: `Title` = folio. Catálogo: `Title` = clave, `folio_registro` = folio. Si hubo notas, se anexan a `observaciones`. |
| 14 | Enviar acuse | Si `acuse_enviado` del trámite no es Sí: «Enviar un correo electrónico desde un buzón compartido (V2)» (Office 365 Outlook) con la plantilla de la sección 6.7. Después, actualizar el trámite: `acuse_enviado` = Sí y `fecha_acuse`. |

: Pasos de REG-01

Destinatarios del acuse:

- **Para:** `enlace_correo` si pasa la validación; si no, el correo de quien respondió en Forms, con una nota en `notas_tramite`.
- **CC:** `titular_correo` del área en «Áreas y órganos», si existe.
- **Responder a:** el buzón compartido. La copia queda en «Elementos enviados» del buzón.

Expresiones útiles:

```text
Fecha local:      convertTimeZone(outputs('Obtener_los_detalles_de_la_respuesta')?['body/submitDate'],
                                  'UTC', 'Central Standard Time (Mexico)', 'yyyy-MM-dd')
Año:              int(substring(variables('fechaRecepcion'), 0, 4))
Comillas OData:   replace(<texto>, '''', '''''')       (un apóstrofo en un nombre de área rompe el filtro)
Casilla marcada:  contains(<respuesta de la casilla>, 'No conozco todos')
Fecha en acuse:   formatDateTime(variables('fechaRecepcion'), 'dddd d ''de'' MMMM ''de'' yyyy', 'es-MX')
```

La casilla de Forms llega como texto con formato de arreglo (`["No conozco todos. Que la DGETD complete la lista."]`); por eso se revisa con `contains`.

## 6.3 Idempotencia

Cada registro tiene un `id_origen` único: `FORMS-<Id. de respuesta>` en el formulario y `XLSX-<nombre del archivo procesado>#<renglón>` en la plantilla. Antes de crear, el flujo busca por `id_origen`; antes de calcular, revisa si `Title` todavía empieza con «PEND-»; antes de enviar, revisa `acuse_enviado`. Por eso una ejecución fallida se puede volver a enviar desde el historial del flujo, sin crear otro catálogo, sin gastar otra clave y sin mandar dos acuses.

## 6.4 Normalización y validaciones

El flujo nunca rechaza un registro que tenga área, nombre y descripción. Lo que no pasa la validación se guarda de forma segura y se anota para la revisión.

| Situación | Qué hace el flujo |
|:--------------------------------------------|:------------------------------------------------------------|
| Pregunta de texto que acepta «por confirmar» llega vacía (`D1`, `D4`) | Guarda «Por confirmar». En `D1`, si la casilla está marcada, guarda «Por confirmar» y `sistemas_por_dgetd` = Sí. |
| Opción de `C3` o `E1` con texto de F-CAT-01 | La traduce al valor de la tabla de la sección 5.2. |
| `D4` no tiene forma `AAAA-MM` ni `AAAA-MM-DD`, o es posterior a la fecha de recepción | Guarda «Por confirmar» y anota en `observaciones` lo que escribió el área. |
| Correo de `A2` sin «@» o con otro dominio | Lo guarda como llegó, envía el acuse a quien respondió y anota. |
| Área que no está en la lista oficial | Usa el elemento «Por confirmar» y anota el texto recibido. Solo ocurre en la plantilla, donde se puede pegar texto. |
| Texto más largo que la longitud de ET-CAT-01 | Lo guarda completo y anota. Las longitudes son propuesta hasta el piloto (ET-CAT-01, sección 5.5). |
| Ya existe un catálogo con la misma área y el mismo nombre oficial (sin distinguir mayúsculas ni acentos) | Registra igual y anota «Posible duplicado de CAT-NNNN». La DGETD decide (ET-CAT-01, sección 6.1, regla 6). |

: Normalización y validaciones de REG-01 y REG-02

## 6.5 Manejo de errores y reintentos

- **Reintentos:** las acciones de SharePoint y Outlook usan la directiva exponencial predeterminada (4 reintentos). «Enumerar filas de una tabla» de Excel usa intervalo fijo de 1 minuto y 5 reintentos, porque un archivo recién subido puede estar bloqueado.
- **Ámbito «Avisar error»:** se ejecuta si «Intentar» falla o agota el tiempo. Escribe el error en `error_flujo` del trámite (si ya existe), publica un mensaje en el canal de Teams «Registro · Alertas» de la DGETD y envía un correo al buzón. Ambos llevan la liga a la ejecución:

```text
concat('https://make.powerautomate.com/environments/', workflow()?['tags']?['environmentName'],
       '/flows/', workflow()?['name'], '/runs/', workflow()?['run']?['name'])
```

- Al final, «Finalizar» con estado «Con errores», para que la ejecución se vea como fallida en el historial.
- **Qué hace la persona de guardia:** abre la ejecución, corrige la causa (por ejemplo, una conexión vencida) y usa «Volver a enviar». La idempotencia de la sección 6.3 evita duplicados.
- **Conexiones:** si una conexión vence, el desencadenador de Forms deja de disparar sin avisar. REG-05 lo detecta con la conciliación semanal de la sección 7.4 y la DGETD vuelve a enviar las respuestas que falten.
- **Historial:** Power Automate conserva el historial de ejecuciones por tiempo limitado. Los errores quedan además en `error_flujo` y en Teams.

## 6.6 Flujos complementarios

**REG-04 Sincronizar estatus.** Cuando cambia un catálogo, busca en «Registros» el trámite con `Title` igual a `folio_registro` y copia `estatus_registro` y `confirmacion_area`. Al pasar a «Ficha enviada» escribe `fecha_ficha_enviada`; al pasar a «Confirmado», `fecha_confirmacion`. Solo escribe si el valor cambió, para no generar versiones vacías.

**REG-05 Revisión diaria.** Busca en las dos listas elementos con `Title` que empiece con «PEND-» y les calcula clave o folio con la misma regla. Busca trámites con `acuse_enviado` distinto de Sí y más de una hora de antigüedad, y reenvía el acuse. Publica en Teams un resumen: registros del día, pendientes y errores. Si `captura_diferida_tipo` tiene valor, lo recuerda en el resumen (sección 5.5).

**REG-06 Folio de corrección.** Para un catálogo «Confirmado» cuyo dueño pide corregir algo. La persona de la DGETD selecciona el catálogo y escribe, en la entrada del desencadenador, qué pidió corregir el área. El flujo crea un trámite con `es_correccion` = Sí, `canal` = el que indique la persona de la DGETD y `respuesta_original` = la descripción; calcula el folio; actualiza el catálogo (`folio_registro` nuevo, `estatus_registro` = Recibido) y envía el acuse con la misma clave. La DGETD hace la corrección en la ficha y sigue el trámite normal.

::: {custom-style="Nota"}
**Nota.** REG-06 solo se usa después de «Confirmado». Antes de confirmar, la corrección se hace en el mismo trámite: el registro regresa de «Ficha enviada» a «En revisión» con el mismo folio. Es la regla de ET-CAT-01, sección 7.1, que también siguen PR-CAT-04, sección 6.16, y la guía de registro.
:::

## 6.7 Acuse

Asunto: `Registro de catálogo recibido · Folio RC-AAAA-NNNN`, con el folio real.

Versión HTML, para el cuerpo de «Enviar un correo electrónico desde un buzón compartido (V2)». Los valores entre llaves dobles se sustituyen en el flujo. Los colores son los de texto del paquete, que cumplen contraste AA sobre blanco.

```html
<div lang="es-MX" style="font-family:'Source Sans 3',Calibri,Arial,sans-serif;font-size:16px;line-height:1.5;color:#161A1D;max-width:600px">
  <h1 style="font-size:22px;line-height:1.3;color:#2A7370;margin:0 0 16px">Recibimos el registro de su lista</h1>
  <p style="margin:0 0 16px">Lista: <strong>{{nombre_oficial}}</strong><br>Área: {{area_registra}}</p>
  <table style="border-collapse:collapse;margin:0 0 16px">
    <tr><th scope="row" style="text-align:left;padding:4px 16px 4px 0;font-weight:600">Folio de registro</th>
        <td style="font-family:'Source Code Pro',Consolas,monospace">{{folio}}</td></tr>
    <tr><th scope="row" style="text-align:left;padding:4px 16px 4px 0;font-weight:600">Clave de catálogo</th>
        <td style="font-family:'Source Code Pro',Consolas,monospace">{{clave}}</td></tr>
    <tr><th scope="row" style="text-align:left;padding:4px 16px 4px 0;font-weight:600">Fecha de recepción</th>
        <td>{{fecha_larga}}</td></tr>
  </table>
  <p style="margin:0 0 16px">La DGETD recibió su registro. Guarde este correo como constancia de la fecha de recepción. Use la clave cuando nos escriba sobre esta lista.</p>
  <h2 style="font-size:18px;color:#2A7370;margin:0 0 8px">Qué sigue</h2>
  <ol style="margin:0 0 16px;padding-left:24px">
    <li>Revisamos su registro y prellenamos lo que la DGETD ya conoce de la lista.</li>
    <li>Le enviaremos la ficha de confirmación para que la revise y la confirme. Plazo: {{plazo_ficha}}.</li>
    <li>Si algo cambia, avísenos: los errores se corrigen sin costo hasta el dictamen. La DGETD no le volverá a pedir lo que ya entregó.</li>
  </ol>
  <p style="margin:0 0 16px">Registrar no publica su lista, no cambia quién la administra ni modifica ningún sistema.</p>
  <h2 style="font-size:18px;color:#2A7370;margin:0 0 8px">Contacto</h2>
  <p style="margin:0 0 16px">Su persona de contacto en la DGETD es {{contacto_nombre}}. Asesoría: {{contacto_general}}. Puede responder este correo.</p>
  <p style="font-size:14px;color:#575F71;margin:0">Dirección General de Estrategia y Transformación Digital · Órgano de Administración Judicial. Correo enviado por el registro de catálogos; la persona titular del área recibe copia.</p>
</div>
```

Versión en texto. Es el contenido de referencia: se usa para revisar la redacción y la accesibilidad, para leerlo en el registro acompañado y si el equipo decide enviar el acuse en texto simple.

```text
Asunto: Registro de catálogo recibido · Folio {{folio}}

Recibimos el registro de su lista

Lista: {{nombre_oficial}}
Área: {{area_registra}}

Folio de registro: {{folio}}
Clave de catálogo: {{clave}}
Fecha de recepción: {{fecha_larga}}

La DGETD recibió su registro. Guarde este correo como constancia de la fecha de recepción.
Use la clave cuando nos escriba sobre esta lista.

Qué sigue
1. Revisamos su registro y prellenamos lo que la DGETD ya conoce de la lista.
2. Le enviaremos la ficha de confirmación para que la revise y la confirme. Plazo: {{plazo_ficha}}.
3. Si algo cambia, avísenos: los errores se corrigen sin costo hasta el dictamen.
   La DGETD no le volverá a pedir lo que ya entregó.

Registrar no publica su lista, no cambia quién la administra ni modifica ningún sistema.

Contacto
Su persona de contacto en la DGETD es {{contacto_nombre}}.
Asesoría: {{contacto_general}}. Puede responder este correo.

Dirección General de Estrategia y Transformación Digital · Órgano de Administración Judicial
```

| Marcador | Origen |
|:------------------------------|:------------------------------------------------------------|
| `{{folio}}`, `{{clave}}` | Pasos 12 y 13 de REG-01 |
| `{{fecha_larga}}` | `fechaRecepcion` con formato largo en es-MX, por ejemplo «lunes 11 de enero de 2027» |
| `{{nombre_oficial}}`, `{{area_registra}}` | Ficha normalizada |
| `{{plazo_ficha}}` | Parámetro `plazo_ficha`: [plazo por definir según capacidad de la DGETD]{custom-style="Marcador"} |
| `{{contacto_nombre}}` | `contacto_dgetd` del área en «Áreas y órganos» |
| `{{contacto_general}}` | Parámetro `contacto_general`: [correo, extensión y horario de la asesoría DGETD]{custom-style="Marcador"} |

: Marcadores de la plantilla del acuse

::: {custom-style="Pendiente"}
**Por confirmar.** El acuse no sale a producción mientras `plazo_ficha` y `contacto_general` tengan el texto del marcador. REG-01 revisa que no empiecen con «[»; si empiezan, no envía y avisa.
:::

# 7. Carga desde Excel (plantilla masiva)

## 7.1 Carpeta y convención de nombre

- Las áreas suben la plantilla F-CAT-01 (`entregables/F-CAT-01-plantilla-masiva.xlsx`) a la biblioteca «Recepción de plantillas»: [liga a la carpeta de SharePoint para plantillas de Excel]{custom-style="Marcador"}. No se recibe por correo.
- Nombre sugerido del archivo: `F-CAT-01_<nombre corto del área>_<AAAA-MM-DD>.xlsx`, sin espacios ni acentos; si el área sube dos el mismo día, agrega `_2`. Ejemplo ilustrativo: `F-CAT-01_DGInmuebles_2027-01-11.xlsx`.
- El flujo no depende del nombre: toma el área de cada renglón, la fecha del archivo y la cuenta de quien lo subió. El nombre solo sirve para que las personas lo reconozcan.
- REG-02 mueve cada archivo a «Plantillas procesadas» y le antepone la fecha y hora de recepción y el ID del archivo: `20270111-1032_57_F-CAT-01_DGInmuebles_2027-01-11.xlsx`. Ese nombre es único y forma parte de `id_origen`.

::: {custom-style="Pendiente"}
**Decisión del equipo.** Cómo se evita que un área vea las plantillas de otras: (a) la función «Solicitar archivos» de SharePoint sobre la carpeta, que deja subir sin ver el contenido, si el inquilino la permite para cuentas internas; o (b) una biblioteca con permiso de colaboración para el personal del OAJ, de la que REG-02 saca cada archivo en cuanto llega. Las plantillas contienen nombres, puestos, correos y extensiones de enlaces y titulares.
:::

## 7.2 REG-02 paso a paso

| Paso | Acción (conector) | Configuración |
|:--------|:------------------------------|:------------------------------------------------------------------|
| 1 | Cuando se crea un archivo (solo propiedades) (SharePoint) | Biblioteca «Recepción de plantillas». Control de simultaneidad, grado 1. |
| 2 | Condición | Si la extensión no es `.xlsx`, mueve el archivo a «Plantillas procesadas» con el prefijo `NO-PROCESADO_`, avisa a quien lo subió y termina. |
| 3 | Retraso de 1 minuto | Da tiempo a que termine la carga y se libere el archivo. |
| 4 | Inicializar variables | `fechaRecepcion` = fecha de creación del archivo en hora de la Ciudad de México (PR-CAT-04, sección 6.6). `anio`. `nombreProcesado`. `renglon` = 2. `resultados` = arreglo vacío. |
| 5 | Enumerar filas presentes en una tabla (Excel Online (Business)) | Archivo: identificador del paso 1. Tabla: `tblMisListas` escrita como valor personalizado. Paginación activada, umbral 500. Formato de fecha y hora ISO 8601. |
| 6 | Seleccionar (Datos: Seleccionar) | Cambia cada encabezado de la tabla por su nombre técnico (sección 7.3). |
| 7 | Aplicar a cada uno, simultaneidad desactivada | Por cada renglón, en orden: incrementa `renglon`; si `A1`, `B2` y `B3` están vacíos, lo salta; si falta alguno de los tres, agrega a `resultados` «Renglón N: no registrado, falta A1, B2 o B3»; si están los tres, ejecuta los pasos 5 y 7 a 13 de REG-01 con `canal` = «Plantilla de Excel», `id_origen` = `concat('XLSX-', nombreProcesado, '#', renglon)`, `archivo_origen` y `persona_captura` = cuenta que subió el archivo, y agrega a `resultados` el renglón, el nombre de la lista, el folio y la clave. |
| 8 | Mover archivo (SharePoint) | A «Plantillas procesadas» con `nombreProcesado`. |
| 9 | Crear tabla HTML (Datos) | Con `resultados`: Renglón · Nombre de la lista · Folio · Clave. |
| 10 | Enviar un correo electrónico desde un buzón compartido (V2) | Un acuse por archivo. Para: quien subió el archivo y los correos `A2` distintos de los renglones. CC: los `titular_correo` de las áreas. Asunto y cuerpo en la sección 7.5. |
| 11 | Actualizar elementos de «Registros» del archivo | `acuse_enviado` = Sí y `fecha_acuse`. |

: Pasos de REG-02

El renglón que tiene la tabla en Excel empieza en el 3, porque los renglones 1 y 2 son los encabezados. La plantilla trae fórmula en la columna `C1` de los 200 renglones; por eso un renglón cuenta como vacío solo si `A1`, `B2` y `B3` lo están.

Una plantilla que el área vuelve a subir corregida registra otra vez todas sus listas. La validación de duplicados de la sección 6.4 las marca como «Posible duplicado» y la DGETD resuelve con el área. La guía y la hoja «Cómo llenar» deben pedir: «Para corregir una plantilla ya enviada, no la vuelva a subir; avise a su contacto».

## 7.3 Columnas de la plantilla

Con un archivo dinámico, Power Automate no conoce las columnas de la tabla y se usan expresiones con el texto exacto del encabezado: `item()?['¿Cómo se llama esta lista? Escriba el nombre completo, sin siglas.']`. El encabezado de la tabla `tblMisListas` es el renglón 2 de la hoja «Mis listas» (la pregunta completa). Si cambia `registro.yaml`, se regenera la plantilla con `build/plantilla_excel.py` y se actualiza la acción «Seleccionar».

| Col. | Encabezado (renglón 1 de la plantilla) | Nombre técnico |
|:----------|:----------------------------------------------------|:----------------------------------------|
| A | A1 · Área que registra | `area_registra` |
| B a E | A2 · Persona enlace: nombre completo, puesto, correo institucional, extensión | `enlace_nombre`, `enlace_puesto`, `enlace_correo`, `enlace_extension` |
| F y G | A3 · Persona titular que valida: nombre completo, puesto | `titular_nombre`, `titular_puesto` |
| H | B1 · Identificador del catálogo (lo llena la DGETD) | Se ignora |
| I | B1b · Clave interna actual | `clave_interna` |
| J | B2 · Nombre oficial | `nombre_oficial` |
| K | B3 · Descripción y propósito | `descripcion` |
| L | C1 · Propietario propuesto | `propietario` |
| M | C2 · Custodio propuesto | `custodio` |
| N | C2 · Custodio propuesto: persona de contacto | `custodio_contacto` |
| O | C2b · Preferencia de custodia | `preferencia_custodia` |
| P | C3 · Clasificación (tipo de lista) | `clasificacion_area` |
| Q | D1 · Sistemas consumidores | `sistemas_consumidores` |
| R | D1 · Casilla | `sistemas_por_dgetd` |
| S | D2 · Frecuencia de actualización | `frecuencia` |
| T | D2 · Frecuencia de actualización: qué lo dispara | `frecuencia_disparador` |
| U | D3 · Versión vigente | `maneja_versiones` |
| V | D3 · Versión vigente: versión actual | `version_area` |
| W | D4 · Fecha de última actualización | `fecha_actualizacion` |
| X | D4 · Casilla | `fecha_en_sistema` |
| Y | E1 · Nivel de acceso | `nivel_acceso` |
| Z | E2 · Datos personales | `datos_personales` |
| AA a AE | F1 a F5 | `ubicacion_lista`, `tamano_aproximado`, `clave_elementos`, `listas_parecidas`, `problema_actual` |

: Correspondencia entre las columnas de la plantilla y el inventario

En la plantilla, las opciones ya son los valores de `registro.yaml` (por ejemplo, «Entidades» en `C3`) y las casillas valen «Sí» o «No», así que no hay traducción. Las listas desplegables se pueden saltar pegando texto; el flujo aplica las validaciones de la sección 6.4. Si `D4` llega como fecha de Excel, el flujo toma los primeros 7 caracteres de la fecha ISO (`AAAA-MM`).

## 7.4 Consolidación con Power Query

El libro «Consolidado de plantillas» vive en una biblioteca privada de la DGETD. Sirve para validar y conciliar, no para registrar: las claves y los folios ya los asignó REG-02.

1. **Origen:** «Obtener datos» > «Desde carpeta de SharePoint», con la URL del sitio. Filtrar la carpeta «Plantillas procesadas» y la extensión `.xlsx`, sin los archivos `NO-PROCESADO_`.
2. **Combinar:** de cada archivo, la tabla `tblMisListas`; agregar el nombre del archivo y el número de renglón (índice que empieza en 3).
3. **Renombrar** por posición con los nombres técnicos de la sección 7.3 y quitar los renglones sin `A1`, `B2` ni `B3`.
4. **Clave de conciliación:** `"XLSX-" & [Name] & "#" & Text.From([renglon])`, igual a `id_origen`.
5. **Combinar con «Registros»** (conector «Lista de SharePoint Online») por `id_origen` y traer `Title` (folio) y la clave del catálogo.
6. **Hojas de validación:** renglones sin folio (el flujo no los registró), valores fuera de las listas de `registro.yaml`, `D4` con formato inválido, correos fuera del dominio, posibles duplicados por área y nombre normalizado, y conteo de «Por confirmar» por campo para el indicador de PR-CAT-04, capítulo 10.

```m
let
    Sitio = "[URL del sitio de SharePoint del registro]",
    Archivos = SharePoint.Files(Sitio, [ApiVersion = 15]),
    // Ajustar la ruta al nombre real de la biblioteca en el sitio
    Procesadas = Table.SelectRows(Archivos, each Text.Contains([Folder Path], "/Plantillas procesadas/")
        and [Extension] = ".xlsx" and not Text.StartsWith([Name], "NO-PROCESADO_")),
    ConDatos = Table.AddColumn(Procesadas, "Datos", each
        Table.AddIndexColumn(
            Excel.Workbook([Content], true){[Item = "tblMisListas", Kind = "Table"]}[Data],
            "renglon", 3, 1)),
    Expandido = Table.ExpandTableColumn(Table.SelectColumns(ConDatos, {"Name", "Datos"}), "Datos",
        Table.ColumnNames(ConDatos{0}[Datos]))
in
    Expandido
```

La conciliación semanal de REG-05 usa el mismo libro con un segundo origen: el libro de respuestas del formulario de grupo, comparado contra `id_origen` de «Registros». Una respuesta sin trámite indica que el desencadenador de Forms dejó de disparar.

**Plan B de la plantilla.** Si «Enumerar filas presentes en una tabla» falla con un archivo (por ejemplo, porque el área agregó o movió columnas), la DGETD toma los renglones del consolidado y los captura en el formulario como captura diferida de tipo «Plan B de plantilla» (sección 5.5), con la fecha de carga del archivo en `captura_diferida_fecha` y su liga en `captura_diferida_archivo`. Así cada renglón recibe clave y folio por la misma regla, con `canal` = «Plantilla de Excel», y la fecha de recepción y el año del folio son los de la carga del archivo. Un archivo subido el 31 de diciembre y capturado en enero conserva el año de recepción en el folio (ET-CAT-01, sección 6.2, regla 1), igual que en el ejemplo de la sección 4.2. El acuse de cada renglón sale por REG-01, uno por lista; la DGETD avisa a la persona enlace que el archivo se procesó por esta vía.

## 7.5 Acuse de la plantilla

Asunto: `Registro de catálogo recibido · Plantilla con N listas · Folios RC-AAAA-NNNN a RC-AAAA-NNNN`. Si los folios no son consecutivos (porque entraron formularios mientras se procesaba el archivo), el asunto dice `· N folios` y el cuerpo los lista.

El cuerpo usa la misma plantilla de la sección 6.7, con la tabla de `resultados` en lugar de la tabla de folio, clave y fecha, y con los renglones no registrados al final, con su motivo.

::: {custom-style="Pendiente"}
**Decisión del equipo.** El asunto de la plantilla se aparta del formato de un solo folio. Validar el texto.
:::

# 8. Ficha de confirmación

## 8.1 Cómo se genera

La ficha es la sección G de F-CAT-01 con lo que el área registró y lo que la DGETD prellenó (PR-CAT-04, sección 6.8). Se genera sin conectores premium, de dos formas complementarias:

1. **Vista de lista, para la DGETD.** La vista «Ficha» y el formulario del elemento agrupado por secciones (sección 2.3). Ahí la persona de contacto revisa y prellena: `G4` a `G7`, `G10`, y los campos «Por confirmar» que resuelva con el área.
2. **Plantilla de correo, para el área.** REG-03 arma la ficha en HTML y la envía. Las áreas no tienen acceso a la lista, así que la ficha les llega por correo.

## 8.2 REG-03 paso a paso

| Paso | Acción | Configuración |
|:--------|:------------------------------|:------------------------------------------------------------------|
| 1 | Para un elemento seleccionado (SharePoint) | Lista del inventario. La persona de contacto selecciona el catálogo y ejecuta «Enviar ficha» desde el menú «Automatizar». |
| 2 | Obtener elemento | Catálogo seleccionado. Si `estatus_registro` no es «En revisión», termina y avisa. |
| 3 | Redactar ficha HTML | Una tabla por sección de `registro.yaml` (A a G), con el `nombre` de cada campo como encabezado de renglón y el valor guardado. Los valores «Por confirmar» se muestran en negritas con el texto «Por confirmar», no solo con color. |
| 4 | Enviar un correo electrónico desde un buzón compartido (V2) | Para: `enlace_correo`. CC: `titular_correo`. Asunto: `Ficha de confirmación · CAT-NNNN · Folio RC-AAAA-NNNN`. El correo pide revisar y confirmar, o decir qué corregir. |
| 5 | Actualizar elemento | `estatus_registro` = Ficha enviada. REG-04 copia el estatus y la fecha al trámite. |
| 6 | Esperar la respuesta | Ver 8.3. |

: Pasos de REG-03

## 8.3 Confirmación

**Opción principal: Aprobaciones (conector estándar).** Después del paso 5, «Iniciar y esperar una aprobación» del tipo «Respuestas personalizadas: esperar una respuesta», asignada a `enlace_correo`, con dos respuestas: «Confirmo la ficha» y «Necesito corregir algo». Los detalles de la aprobación llevan el resumen de la ficha y la liga a la ficha completa en el correo.

- «Confirmo la ficha»: `estatus_registro` = Confirmado y `confirmacion_area` = `<nombre de quien respondió>, <AAAA-MM-DD>` (ET-CAT-01, tabla 5.4).
- «Necesito corregir algo»: `estatus_registro` = En revisión, el comentario se anexa a `observaciones` y se avisa a la persona de contacto.
- Si nadie responde en el tiempo máximo de espera del flujo, se avisa a la persona de contacto. Qué ocurre si el área no confirma está pendiente en ET-CAT-01 (sección 7.2, pendiente 6).

**Opción sin Aprobaciones.** El correo de la ficha pide responder «Confirmo» o indicar qué corregir. La persona de contacto anota `confirmacion_area` y cambia el estatus a mano. REG-04 copia el cambio al trámite.

::: {custom-style="Pendiente"}
**Por confirmar.** Aprobaciones necesita una base de datos de Dataverse en el entorno; en el entorno predeterminado suele crearse sola la primera vez. Hay que verificarlo (sección 10). Esa base solo guarda las aprobaciones, no los datos del registro.
:::

## 8.4 Ficha en PDF (opcional)

Si el equipo quiere una constancia imprimible, REG-03 guarda la ficha HTML como archivo en una carpeta de OneDrive para la Empresa o de SharePoint y usa «Convertir archivo» de OneDrive para la Empresa (conector estándar) para obtener un PDF y adjuntarlo. No se usa «Rellenar una plantilla de Microsoft Word», que es premium.

# 9. Permisos, datos personales, accesibilidad y registro acompañado

## 9.1 Permisos

| Recurso | Quién | Permiso |
|:------------------------------|:----------------------------------|:--------------------------------------------|
| Sitio y listas del registro | Personas propietarias (2 o 3 de la DGETD) | Control total. No eliminan elementos. |
| Sitio y listas del registro | Equipo de registro de la DGETD | «Colaborar sin eliminar» |
| Sitio y listas del registro | Resto del personal de la DGETD | Lectura, si la DGETD lo decide; si no, sin acceso |
| Sitio y listas del registro | Áreas, órganos jurisdiccionales y resto del OAJ | Sin acceso. Solo la DGETD lee las listas. |
| Formulario de registro | Personal del OAJ con cuenta institucional | Responder |
| Formulario de registro | Grupo de M365 de la DGETD | Propietario; edición por el equipo de registro |
| Recepción de plantillas | Personal del OAJ | Subir archivos, según la opción de la sección 7.1 |
| Plantillas procesadas y consolidado | Equipo de registro de la DGETD | «Colaborar sin eliminar» |
| Buzón compartido | Equipo de registro y cuenta de los flujos | Acceso completo y «Enviar como» |
| Flujos | Cuenta de servicio institucional, con al menos dos personas copropietarias | Propietarios. Las conexiones se crean con la cuenta de servicio, no con una cuenta personal. |

: Permisos del registro

::: {custom-style="Pendiente"}
**Por confirmar.** Si el inquilino permite una cuenta de servicio con licencia para los flujos. Si no, las conexiones quedan a nombre de una persona y otra persona debe ser copropietaria, con un procedimiento para recrearlas si la primera cambia de puesto.
:::

## 9.2 Datos personales y conservación

- El registro no pide el contenido de las listas ni datos personales de partes, peritos o víctimas. `E2` solo pregunta si la lista los contiene.
- Sí guarda datos personales de personas servidoras públicas: nombre, puesto, correo institucional y extensión de la persona enlace, de la persona titular y del contacto del custodio. Están en el inventario, en `respuesta_original`, en las respuestas de Forms, en las plantillas y en los correos.
- El formulario y la plantilla enlazan al aviso de privacidad simplificado: [liga al aviso de privacidad simplificado, por definir con la unidad de transparencia]{custom-style="Marcador"}. Fundamento: Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados y Acuerdo General del Pleno del Órgano de Administración Judicial que establece las disposiciones en materia de transparencia, acceso a la información pública y protección de datos personales. El artículo 23 de los Lineamientos no aplica aquí: regula el acceso a los catálogos que contienen datos personales, no los datos de las personas servidoras públicas que recaba el registro.
- Las listas no se publican ni se comparten fuera de la DGETD. Si el inquilino usa etiquetas de confidencialidad, el sitio lleva la de uso interno.
- Conservación: [plazo de conservación por definir con la unidad de transparencia y el área de archivo]{custom-style="Marcador"}. Propuesta: las respuestas de Forms y las plantillas se conservan hasta conciliar el corte del inventario (PR-CAT-04, actividad 22); después, la DGETD decide si se eliminan de Forms, porque los datos ya están en «Registros». Los elementos de las listas no se eliminan (sección 4.4).

## 9.3 Accesibilidad del formulario (WCAG 2.2 AA)

Forms resuelve buena parte de la accesibilidad, pero el contenido y el tema los pone la DGETD. Antes del piloto se revisa:

| Criterio | Qué revisar en Forms |
|:------------------------------|:----------------------------------------------------------------------|
| 1.1.1 Contenido no textual | Sin imágenes en preguntas ni en el encabezado; si se usa el logotipo, con texto alternativo. |
| 1.3.1 Información y relaciones | Cada pregunta tiene título propio; los subcampos de `A2` y `A3` se entienden solos («Puesto de la persona enlace.»). |
| 1.4.1 Uso del color | «Por confirmar» y «obligatorio» se dicen con texto; nada depende del color. |
| 1.4.3 y 1.4.11 Contraste | Tema de fondo liso; texto y controles con contraste suficiente. No usar la menta de acento (#49B6B2) como color del tema para texto. |
| 1.4.10 Reajuste del contenido | El formulario se usa en un teléfono y con zoom de 400 % sin desplazamiento horizontal. |
| 2.1.1 Teclado y 2.4.7 Foco visible | Todo el formulario, incluidas las listas desplegables de `A1`, `C1` y `C2`, se llena solo con teclado y el foco se ve. |
| 2.5.8 Tamaño del objetivo | Opciones y botones con área suficiente en el teléfono. |
| 3.1.1 Idioma | Textos en español; revisar que el lector de pantalla lea en español. |
| 3.2.6 Ayuda consistente | La línea de contacto en el mismo lugar en cada sección (sección 5.2). |
| 3.3.1 y 3.3.2 Errores y etiquetas | Las preguntas obligatorias se anuncian como obligatorias; el mensaje de error de Forms se entiende. |
| 3.3.7 Entrada redundante | Vínculo prellenado con `A1`, `A2`, `A3` y `C1` (sección 5.3). |
| 3.3.8 Autenticación accesible | Inicio de sesión institucional normal, sin pruebas adicionales. |
| Lector de pantalla | Prueba completa con NVDA o Narrador en Windows y con el lector del teléfono. |

: Revisión de accesibilidad del formulario

El acuse y la ficha se revisan igual: encabezados reales, tabla con encabezados de renglón, idioma `es-MX`, contraste AA y sentido completo sin colores. El informe de conformidad de accesibilidad que Microsoft publica para Forms se consulta en las verificaciones previas (sección 10) para saber qué excepciones conocidas tiene.

## 9.4 Registro acompañado

El procedimiento está en la sección 5.5. Para el equipo técnico, lo que importa:

- Las personas de la DGETD que hacen registro acompañado se agregan al grupo `grupo_captura_dgetd`. Solo así REG-01 marca el canal correcto y envía el acuse a la persona enlace.
- Si un órgano jurisdiccional no tiene cuenta de M365, el registro acompañado es su canal (PR-CAT-04, sección 6.5): la DGETD captura y el acuse va al correo que el órgano indique en `A2`.

# 10. Verificaciones previas y plan B

Se hacen antes de comprometer el formulario como camino principal, como pide la propuesta del kit («Antes de comprometerlo hay que verificar que Power Automate esté habilitado y que los órganos jurisdiccionales tengan cuenta de M365»).

| No. | Verificación | Cómo se verifica | Si falla |
|:-------|:------------------------------|:--------------------------------------------|:------------------------------|
| 1 | Power Automate habilitado para la DGETD y conectores permitidos por las directivas DLP | Crear un flujo de prueba con Forms, SharePoint, Outlook, Excel Online, Office 365 Groups, Teams y Aprobaciones en el entorno predeterminado. Pedir a la administración de M365 las directivas DLP vigentes. | Plan B 1 |
| 2 | Formularios de grupo | Crear un formulario desde el grupo de M365 de la DGETD y verificar que el grupo es el dueño. Probar «Mover» de una cuenta personal al grupo. | Plan B 2 |
| 3 | Cuentas de M365 de órganos jurisdiccionales | Pedir a la administración de M365 cuántos órganos tienen cuentas con correo y si las usan personas del órgano. Probar el formulario con una cuenta de un órgano en el piloto. | Plan B 3 |
| 4 | Vínculos prellenados | Generar uno, identificar los parámetros y armar uno por fórmula. Probar con opción y con texto. | Plan B 4 |
| 5 | Informe de accesibilidad de Forms | Consultar el informe de conformidad de accesibilidad de Microsoft para Forms y anotar las excepciones conocidas. Hacer la revisión de la sección 9.3. | Las excepciones se cubren con registro acompañado y con F-CAT-01 en Word como apoyo. |
| 6 | Límites de Forms | Contar las áreas y órganos activos de la lista oficial y probar una pregunta con todas las opciones. Probar textos de 1,000 y 2,000 caracteres. | Dividir `A1` por tipo (sección 5.4). |
| 7 | Buzón compartido y «Enviar como» | Enviar un correo de prueba desde el flujo con el buzón. | Usar el buzón del grupo de M365, si se puede enviar como el grupo. |
| 8 | Aprobaciones | Crear una aprobación de prueba en el entorno. | Opción sin Aprobaciones (sección 8.3). |
| 9 | «Solicitar archivos» en SharePoint para cuentas internas | Probarlo en la carpeta de recepción. | Opción (b) de la sección 7.1. |
| 10 | Cuenta de servicio con licencia | Pedirla a la administración de M365. | Conexiones de una persona con copropietaria (sección 9.1). |

: Verificaciones previas

**Plan B**, con lo que ya prevén la propuesta del kit, PR-CAT-04 (sección 6.5) y ET-CAT-01 (sección 6.1):

1. **Sin Power Automate.** El formulario sigue funcionando y las respuestas quedan en Forms. La DGETD crea el catálogo y el trámite en las listas a partir del libro de respuestas, con la clave y el folio calculados con la misma regla, y envía el acuse a mano desde el buzón con la plantilla de la sección 6.7. El acuse deja de ser automático, como prevén ET-CAT-01, sección 6.1, y PR-CAT-04, sección 6.6.
2. **Sin formularios de grupo.** El formulario se crea con la cuenta de servicio institucional, nunca con la cuenta de una persona, y se agregan personas coautoras de la DGETD.
3. **Órganos jurisdiccionales sin cuenta de M365.** El registro acompañado es el canal de respaldo (PR-CAT-04, sección 6.5). También puede la DGETD recibir la plantilla de Excel por el conducto institucional y subirla ella misma.
4. **Sin vínculos prellenados.** La persona enlace llena `A1` a `A3` en cada envío. Se recomienda la plantilla de Excel a partir de 3 listas, no de 5, y se mide en el piloto.
5. **Lo que no es plan B.** Word o PDF como medio de captura quedan descartados: obligan a imprimir, firmar, escanear y recapturar, y producen respuestas que no se pueden comparar. F-CAT-01 en Word sirve para preparar las respuestas y como constancia imprimible.

# 11. Piloto con 3 perfiles

Perfiles (PR-CAT-04, actividad 3): un área de alta madurez digital, una de baja madurez y un órgano jurisdiccional o su área competente. Fecha: [segunda quincena de noviembre de 2026, por confirmar]{custom-style="Marcador"}.

El piloto se hace en las listas de producción con registros reales, para no gastar claves en pruebas. Las pruebas técnicas previas (sección 12, tarea 11) se hacen en el sitio de pruebas.

| Qué medir | Cómo | Para qué decisión |
|:------------------------------|:----------------------------------------|:----------------------------------------|
| Tiempo real de llenado por lista | Hora de inicio y de finalización que Forms guarda en cada respuesta; en la plantilla, lo que reporte el área. | El dato que se comunique en la guía y la circular, en lugar de una cifra supuesta. |
| Preguntas que generan duda | Observación de la sesión y preguntas que la persona hace en voz alta o por chat. | Ajuste de subtítulos y de la guía. Si cambia un texto, se cambia en `registro.yaml`. |
| Uso de «Por confirmar» por campo | Vista «Por confirmar» y consolidado. | Carga de trabajo del prellenado; indicador de PR-CAT-04, capítulo 10. |
| Tiempo del envío al acuse | `fecha_acuse` menos la hora de envío. | El tiempo de acuse que se comunique en la guía y la circular (PR-CAT-04, sección 6.6). |
| Folio y clave correctos | Revisión de cada trámite; un envío simultáneo de dos personas a propósito. | Confirmación de la regla de la sección 4. |
| Errores y reintentos del flujo | Historial, `error_flujo` y canal de alertas. | Ajuste de reintentos y validaciones. |
| Uso de la liga prellenada | Si la persona cambió algún valor prellenado. | Si conviene prellenar más campos. |
| Accesibilidad | Por lo menos una prueba con lector de pantalla y una en teléfono. | Correcciones del tema y de los textos. |
| Plantilla de Excel | Un perfil registra al menos 6 listas con la plantilla. | Validaciones de REG-02 y umbral de 5 listas. |
| Registro acompañado | Duración de la sesión y problemas de captura. | Capacidad de la DGETD para atender órganos jurisdiccionales. |
| Esfuerzo de la DGETD por ficha | Tiempo de revisión, prellenado y envío de cada ficha. | Los plazos de los marcadores [plazo por definir según capacidad de la DGETD]{custom-style="Marcador"} de la ficha y de las dudas. |
| Confirmación | Si el área entiende la ficha y la aprobación, y cuánto tarda en responder. | Opción de confirmación (sección 8.3). |

: Qué se mide en el piloto

Las metas de los indicadores se fijan después del piloto (PR-CAT-04, capítulo 10).

# 12. Tareas para montarlo

Las duraciones son **estimaciones** en días hábiles de trabajo efectivo de una persona; no son compromisos. Con dos personas en paralelo, el montaje anterior al piloto cabe en unos 6 o 7 días hábiles (estimación), si las verificaciones de la sección 10 no encuentran bloqueos.

| No. | Tarea | Responsable | Días | Depende de |
|:-------|:--------------------------------------------|:--------------------------|:----------|:-----------------|
| 1 | Hacer las verificaciones previas 1 a 10 | Equipo técnico DGETD con administración de M365 | 1 | — |
| 2 | Crear sitio de pruebas y sitio de producción, grupos de SharePoint, nivel «Colaborar sin eliminar», bibliotecas y buzón | Equipo técnico DGETD | 0.5 | 1 |
| 3 | Crear en pruebas las listas «Áreas y órganos», «Parámetros», «Inventario de catálogos» y «Registros», con columnas, índices, valores únicos, vistas y formulario por secciones | Equipo técnico DGETD | 1.5 | 2 |
| 4 | Cargar la lista oficial de áreas y órganos, los bloques, las personas de contacto y los correos de titulares | Responsable del registro DGETD | 1 | 3; fuente de la lista oficial |
| 5 | Crear el formulario de grupo con secciones, preguntas, subtítulos, ramificación y tema; crear el formulario «Mi órgano no lleva listas propias» | Equipo técnico DGETD | 1 | 4 |
| 6 | Construir REG-01 con validaciones, idempotencia y manejo de errores | Equipo técnico DGETD | 1.5 | 3, 5 |
| 7 | Montar las plantillas del acuse (HTML y texto) y revisar su redacción | Responsable del registro DGETD | 0.5 | 6 |
| 8 | Construir REG-02 y el libro «Consolidado de plantillas» | Equipo técnico DGETD | 1.5 | 3 |
| 9 | Construir REG-03 con la opción de confirmación elegida | Equipo técnico DGETD | 1 | 3, 8.3 decidida |
| 10 | Construir REG-04, REG-05 y REG-06 | Equipo técnico DGETD | 1 | 6 |
| 11 | Probar en el sitio de pruebas: envíos simultáneos, cambio de año (simulando `anio`), clave de 5 dígitos (simulando el ID), reenvío de ejecuciones fallidas, plantilla con errores, área con apóstrofo | Equipo técnico DGETD | 1 | 6 a 10 |
| 12 | Revisar la accesibilidad del formulario, el acuse y la ficha (sección 9.3) | Equipo técnico DGETD | 0.5 | 5, 7 |
| 13 | Generar los vínculos prellenados de las áreas | Responsable del registro DGETD | 0.5 | 4, 5 |
| 14 | Crear las listas de producción a partir de las de prueba (estructura sin elementos) y copiar los flujos apuntando a producción | Equipo técnico DGETD | 0.5 | 11 |
| 15 | Obtener el aviso de privacidad simplificado y el plazo de conservación (duración por definir) | Unidad de transparencia, con la DGETD | — | — |
| 16 | Definir los valores de los marcadores de plazo y contacto en «Parámetros» (duración por definir) | Persona titular de la DGETD | — | Piloto |
| 17 | Hacer el piloto con 3 perfiles | Responsable del registro DGETD y equipo técnico | 3 a 5 | 12 a 14 |
| 18 | Ajustar formulario, flujos, plantilla y guía con lo aprendido | Equipo técnico DGETD | 1 | 17 |

: Tareas para montar el registro

Total de trabajo estimado: unos 15 días-persona, sin contar las tareas 15 y 16 (estimación). Las tareas 1, 4 y 15 dependen de otras áreas y son las que más pueden retrasar el montaje.

# 13. Decisiones que el equipo debe validar

Las dos primeras conviene resolverlas antes del piloto, porque el piloto se hace en las listas de producción.

1. **Antes del piloto.** Nombres técnicos nuevos y regla de pares de campos, y su incorporación a ET-CAT-01, sección 5.5, tabla 5.3.a y anexo A (sección 2.2, notas 1 y 2).
2. **Antes del piloto.** Valor «Anulado» para registros hechos por error en `registro.yaml` y en ET-CAT-01, sección 7.2; mientras tanto, el tratamiento provisional sin «Retirado» (sección 4.4).
3. Redacción de ET-CAT-01 sobre el orden de asignación de claves (sección 4.2).
4. Valores de `canal`, si se agregan a `registro.yaml` y cómo se distinguen las fichas de contingencia: con `es_contingencia`, como propone este documento, o con un cuarto valor «Contingencia» (sección 3.3).
5. Captura diferida con parámetros para la ficha de contingencia y el plan B de la plantilla (secciones 5.5 y 7.4).
6. Correo de la persona titular para la copia del acuse: desde la designación o como subcampo nuevo de `A3` (sección 3.4).
7. Cinco secciones obligatorias y una opcional, y pregunta de navegación para saltar F (sección 5.2).
8. Cómo se protege la carpeta de plantillas (sección 7.1).
9. Asunto del acuse de la plantilla (sección 7.5).
10. Confirmación de la ficha con Aprobaciones o por respuesta de correo (sección 8.3).
11. Cuenta de servicio para los flujos (sección 9.1).
12. Conservación de respuestas de Forms y plantillas (sección 9.2).
13. Umbral de la plantilla si no hay vínculos prellenados (sección 10, plan B 4).
14. Marcadores de este documento que no están en `registro.yaml` > `marcadores`: [liga al aviso de privacidad simplificado, por definir con la unidad de transparencia]{custom-style="Marcador"}, [liga para confirmar, por definir]{custom-style="Marcador"}, [plazo de conservación por definir con la unidad de transparencia y el área de archivo]{custom-style="Marcador"}, [dominio institucional]{custom-style="Marcador"} y [segunda quincena de noviembre de 2026, por confirmar]{custom-style="Marcador"}. Conviene darlos de alta para que la plantilla y los flujos los detecten.
