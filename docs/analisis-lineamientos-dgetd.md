# Análisis de los Lineamientos Generales de Catálogos Institucionales: qué le toca hacer a la DGETD

**Documento analizado:** *Lineamientos Generales de Catálogos Institucionales*, Comité de Gobernanza Digital del OAJ (v2). Son 9 páginas, 27 artículos y 7 transitorios, con firma electrónica del 16/10/2026.
**Fecha del análisis:** 09/11/2026.
**Método:** tres lecturas independientes del texto (obligaciones explícitas, entregables implícitos o por remisión, y plazos con vacíos). Después, una revisión de completitud y una verificación de citas contrastaron cada elemento con el artículo que lo sustenta.

---

## 1. En una frase

Los Lineamientos convierten a la DGETD en **la autoridad técnica del sistema de catálogos**. Tiene que emitir las reglas (estándares, formatos y procedimientos), operar la infraestructura (inventario y Plataforma), dictaminar cada catálogo antes de que lo vea el Comité, medir la calidad y conducir la regularización de los catálogos que ya existen. Todo esto con plazos encadenados de 60, 90 y 120 días.

## 2. Cómo leer las etiquetas

| Etiqueta | Significado |
|---|---|
| **Explícita** | El texto nombra a la DGETD como sujeto de la obligación. |
| **Derivada** | El texto no la nombra para esa tarea concreta, pero el entregable es indispensable para que otro actor cumpla, y cabe en la obligación general de emitir "formatos y procedimientos operativos" (art. 14 fr. IX; Transitorio TERCERO). |
| **De medios** | "Promoverá": hay que impulsarlo, pero no se fija un resultado verificable. |
| **Facultativa** | "Podrá": es opcional. |
| **Comité** | Requiere aprobación o decisión del Comité de Gobernanza Digital. |

## 3. Calendario

Todos los plazos corren desde la **entrada en vigor**, que es el día siguiente a la publicación (Transitorio PRIMERO). **El documento no trae la fecha de publicación**; solo consta la firma del 16/10/2026. Si la publicación fue ese mismo día, la entrada en vigor sería el 17/10/2026 y los plazos quedarían así (días naturales, sin excluir vacaciones):

| Transitorio | Obligación | Responsable | Vence (supuesto) |
|---|---|---|---|
| TERCERO | Publicar formatos, procedimientos y estándares técnicos | **DGETD** | **16/12/2026** (quedan unos 37 días) |
| CUARTO | Registrar ante la DGETD los catálogos que ya se administran, con los metadatos del art. 8 | Áreas y órganos jurisdiccionales (los recibe la DGETD) | 15/01/2027 |
| QUINTO | Plan de adecuación progresiva **aprobado por el Comité** | DGETD lo elabora, el Comité lo aprueba | 14/02/2027 |

> ⚠️ **Hay que confirmar la fecha real de publicación** en la Intranet y en el Sistema de Administración de Documentos Normativos Administrativos (Transitorio SEGUNDO). Si las dos fechas difieren, conviene tomar la más temprana.

**Por qué la secuencia es apretada:** el formato de registro tiene que estar publicado dentro de los 60 días para que las áreas registren a tiempo. El registro cierra el día 90. Del cierre del registro a la fecha en que el plan ya debe estar aprobado quedan **unos 30 días** para diagnosticar, priorizar, redactar y presentar el plan en sesión del Comité. Eso depende del calendario de sesiones.

---

## 4. Lo que la DGETD tiene que hacer

### 4.1 Paquete normativo del Transitorio TERCERO (60 días)

Es el entregable más urgente. Agrupa todo lo que el texto deja "conforme a lo que establezca la DGETD".

#### A. Estándares técnicos (art. 14 fr. II: *establecer y publicar*)

| # | Elemento | Fundamento | Etiqueta | Contenido mínimo que ya fija el texto |
|---|---|---|---|---|
| A1 | **Estándar de estructura de catálogos** | Art. 14 fr. II; art. 7 | Explícita | Atributos mínimos: identificador único, descripción, estatus (activo, inactivo u obsoleto), fechas de vigencia, metadatos de gestión (fecha de última actualización y responsable) y atributos específicos documentados en el diccionario. |
| A2 | **Especificación del identificador único de registro** | Art. 7 fr. I a)–d); art. 25 fr. I | Explícita (inciso d) | Alfanumérico, persistente o inmutable, con unicidad global en todo el OAJ y neutralidad semántica (sin fechas, lugares ni significado). La unicidad global exige además un **mecanismo central de asignación**, que el texto no prevé expresamente. |
| A3 | **Perfil de metadatos del catálogo (ficha)** | Art. 8 fr. I–XI | Derivada | Los 11 metadatos obligatorios: identificador del catálogo, nombre oficial, descripción y propósito, propietario, custodio, clasificación, sistemas consumidores, frecuencia de actualización, versión vigente, fecha de última actualización y nivel de acceso. |
| A4 | **Esquema de versionamiento** | Art. 13 fr. III; art. 4 fr. XIX | Explícita | Identificador único por versión. Distingue el **cambio estructural mayor**, que genera nueva versión, del **cambio menor de contenido**, que solo va a la bitácora. |
| A5 | **Estándar de formatos de publicación abiertos** | Art. 22; art. 25 fr. IV | Explícita | Formatos estructurados abiertos y legibles por máquina. El texto no los enumera: la DGETD los define, por ejemplo CSV, JSON o XML. También define cómo se publican junto con los metadatos y el diccionario (art. 21). |
| A6 | **Criterios de interoperabilidad y de catálogos de relación** | Art. 25 fr. I–IV; art. 5 fr. IV | Derivada (dentro de A1) | Identificadores estables, reutilizar antes de crear, relaciones explícitas entre catálogos y estándares abiertos. Conviene integrarlos como sección de A1, no como instrumento aparte. |

#### B. Formatos (art. 14 fr. IX)

| # | Formato | Lo usa | Fundamento | Campos mínimos que ya fija el texto |
|---|---|---|---|---|
| B1 | **Propuesta de nuevo catálogo** | Áreas y órganos jurisdiccionales | Art. 10 fr. I–VI | Justificación, contenido y alcance, sistemas consumidores, propietario y custodio propuestos, frecuencia estimada, análisis de catálogos existentes. Conviene agregar un campo para la opinión de los órganos jurisdiccionales en catálogos de origen jurisdiccional (art. 4 fr. XVII). |
| B2 | **Plantilla de diccionario de datos** | DGETD y propietario | Art. 11 | Por atributo: nombre técnico, descripción, tipo de dato, longitud, restricciones, obligatoriedad y valores permitidos. |
| B3 | **Dictamen técnico** | DGETD | Art. 12; art. 14 fr. III | No tiene contenido normado. Se sugiere que incluya el cumplimiento de los criterios del art. 6, la verificación de no redundancia (art. 25 fr. II), el tipo de catálogo (art. 5 fr. I–IV), la **propuesta estratégico/operativo** (art. 5), el propietario y custodio y el diccionario. |
| B4 | **Registro de catálogos existentes** | Áreas (Transitorio CUARTO) | Transitorio CUARTO; art. 8 | Los 11 metadatos del art. 8. Se recomienda añadir campos de diagnóstico (ver 4.2). |
| B5 | **Solicitud de cambio estructural mayor** | Propietario | Art. 13 fr. I–V | Descripción del cambio, evaluación de impacto en los sistemas consumidores, versión propuesta, documentación del cambio y plan de comunicación. |
| B6 | **Bitácora de cambios menores** | Custodio | Art. 13; art. 16 fr. IV | Tipo (alta, baja o modificación), elemento, fecha y responsable. |
| B7 | **Reporte periódico de indicadores de calidad** | Custodio | Art. 19 | Valores por indicador y periodo. |
| B8 | **Plan de mejora y seguimiento** | Custodio | Art. 20 | Indicador por debajo del umbral, acciones, fechas y avance. |

#### C. Procedimientos (art. 14 fr. IX)

Las fases las fija el art. 9: propuesta, diseño, aprobación, implementación, publicación, mantenimiento, evolución y retiro.

| # | Procedimiento | Fundamento | Nota |
|---|---|---|---|
| C1 | Recepción y evaluación de propuestas hasta el dictamen | Art. 10, 12, 14 fr. III | No hay plazo de respuesta; conviene fijarlo en el procedimiento. |
| C2 | Diseño conjunto del diccionario de datos con el propietario | Art. 11 | |
| C3 | Coordinación de la aprobación ante el Comité | Art. 14 fr. VI; art. 12 | Incluye cómo inscribir asuntos en las sesiones. |
| C4 | Implementación (carga inicial) y publicación en la Plataforma | Art. 9 fr. IV–V; art. 16 fr. VI; art. 21 | Debe incluir el **aviso al propietario** para que pueda "verificar la publicación" (art. 15 fr. VII). |
| C5 | Control de validación previo a publicar o versionar | Art. 6 fr. III | El art. 6 exige "controles formales de validación" que ningún otro artículo desarrolla. |
| C6 | Mantenimiento y **sincronización de cambios menores** con lo publicado | Art. 13; art. 8 fr. X | Sin esto, lo publicado se desfasa de la bitácora del custodio. |
| C7 | Control de cambios estructurales mayores | Art. 13 fr. I–V | Las fr. II, IV y V **no dicen quién** evalúa el impacto, documenta y comunica. El procedimiento debe asignarlo, y no conviene asumir por defecto que todo recae en la DGETD. Conviene fijar la "anticipación suficiente" en días. |
| C8 | Retiro controlado | Art. 9 fr. VIII | Ningún artículo lo regula. Hay que definir quién lo solicita, quién lo aprueba, el aviso a los consumidores y la conservación de identificadores e histórico. |
| C9 | Medición y reporte de indicadores | Art. 19 | Periodicidad, canal y destino de los reportes (Grupo de Trabajo de Calidad de Datos). |
| C10 | Seguimiento de acciones correctivas | Art. 20 | |
| C11 | Registro de catálogos existentes (Transitorio CUARTO) | Transitorio CUARTO | Debe estar operando antes del día 90. |

#### D. Indicadores de calidad (art. 14 fr. VII; art. 19)

| # | Elemento | Etiqueta | Nota |
|---|---|---|---|
| D1 | **Indicadores cuantitativos** para las 6 dimensiones del art. 18: completitud, exactitud, consistencia, actualidad, unicidad y validez | Explícita | El TERCERO no los nombra expresamente, pero conviene publicarlos con el paquete porque los procedimientos C9 y C10 dependen de ellos. |
| D2 | **Umbrales** | **No asignados** | El art. 20 habla de "umbrales establecidos" sin decir quién los fija. Lo lógico es que la DGETD los proponga junto con los indicadores, y conviene formalizarlo ante el Comité. |
| D3 | Medición automatizada | Facultativa | Art. 19: "preferentemente". |

> Hay una inconsistencia a considerar al diseñar D1. El art. 7 fr. I b) exige unicidad **global** del identificador en todo el OAJ, pero el art. 18 fr. V mide la unicidad solo **dentro del catálogo**. Conviene que el indicador de unicidad cubra ambos niveles.

#### E. Facultativos que conviene decidir ahora

| # | Elemento | Fundamento | Nota |
|---|---|---|---|
| E1 | Procedimientos simplificados para catálogos operativos o de alcance acotado | Art. 5, último párrafo | "Podrá", **previa aprobación del Comité**. No le corre el plazo de 60 días. Puede ir en una sesión posterior. |

---

### 4.2 Transición de los catálogos existentes (Transitorios CUARTO, QUINTO y SEXTO)

| # | Elemento | Fundamento | Etiqueta | Nota |
|---|---|---|---|---|
| T1 | **Recibir y administrar el registro** de catálogos existentes | Transitorio CUARTO | Explícita (registran "ante la DGETD") | |
| T2 | **Asignar el identificador de catálogo** (art. 8 fr. I) al registrarse | Art. 8 fr. I; Transitorio CUARTO | Derivada | Las áreas no pueden darse a sí mismas un código único para todo el OAJ. |
| T3 | **Depurar el registro**: decidir qué "catálogos de información" registrados son "catálogos institucionales" según el art. 6 | Transitorio CUARTO frente al QUINTO; art. 6 | Derivada | El CUARTO usa un término más amplio y sin definir. El QUINTO solo adecúa "catálogos institucionales". |
| T4 | **Diagnóstico de brechas** por catálogo frente a los arts. 7, 8, 11, 21 y 22 | Transitorio QUINTO | Derivada | Es el insumo del plan. Los metadatos del CUARTO no bastan para medir las brechas. |
| T5 | **Plan de adecuación progresiva** | Transitorio QUINTO | **Explícita · Comité** | Debe quedar aprobado dentro de los 120 días. Hay que considerar identificadores heredados con significado (claves de circuito, materia o año), que chocan con la neutralidad y la inmutabilidad del art. 7: se necesitan tablas de equivalencia y un régimen de transición. |
| T6 | **Tratamiento de los catálogos consolidados con la norma del extinto CJF** | Transitorio SEXTO | Derivada | El SEXTO abroga la norma anterior pero no dice si esos catálogos conservan su autorización. |

### 4.3 Infraestructura permanente

| # | Elemento | Fundamento | Etiqueta | Nota |
|---|---|---|---|---|
| P1 | **Inventario institucional de catálogos autorizados** | Art. 14 fr. I | Explícita | Su contenido no está normado. Se sugiere usar la ficha del art. 8 y estatus como *registrado*, *en dictamen*, *autorizado*, *en adecuación* y *retirado*, para resolver el desfase entre el registro del CUARTO y los catálogos "autorizados". |
| P2 | **Administrar la Plataforma de Acceso a la Información Institucional** | Art. 14 fr. IV | Explícita | El texto da por hecho que **la Plataforma ya existe**. Si no está operando, ningún catálogo puede ser "autorizado" (art. 4 fr. IV). Es un riesgo crítico que hay que verificar. |
| P3 | Autenticación y autorización según el nivel de sensibilidad | Art. 23 | Derivada (por P2) | La escala de sensibilidad viene de la "normativa aplicable" y de las políticas del propietario (art. 15 fr. III). A la DGETD le toca implementarla, no definirla. |
| P4 | **Registro de accesos y estadísticas de uso** | Art. 24 | Derivada (por P2) | Requiere aviso de privacidad y política de conservación, porque registra datos personales de los usuarios. |
| P5 | Impulsar API y servicios de datos | Art. 26 | **De medios** | "Promoverá": no hay meta ni plazo. |

### 4.4 Funciones continuas

| # | Función | Fundamento | Etiqueta |
|---|---|---|---|
| F1 | Evaluar propuestas y emitir dictámenes técnicos | Art. 14 fr. III; art. 12 | Explícita |
| F2 | Elaborar el diccionario de datos de cada catálogo junto con el propietario | Art. 11 | Explícita |
| F3 | Proponer al Comité la clasificación estratégico/operativo de cada catálogo | Art. 5, último párrafo | Explícita · Comité |
| F4 | Coordinar el proceso de aprobación ante el Comité | Art. 14 fr. VI | Explícita · Comité |
| F5 | Recibir solicitudes de cambio estructural y asignar versión | Art. 13 fr. I y III; art. 15 fr. VI | Explícita |
| F6 | Fungir como **custodio** cuando el Comité la designe (preferentemente en catálogos transversales o en la Plataforma) y cumplir entonces las obligaciones del art. 16 | Art. 17; art. 12 | Preferente · Comité |
| F7 | Supervisión, estandarización técnica, calidad e interoperabilidad cuando el custodio sea otra área | Art. 17, último párrafo | Explícita |
| F8 | Asesoría técnica a propietarios y custodios | Art. 14 fr. V | Explícita |
| F9 | Monitorear el cumplimiento de los Lineamientos | Art. 14 fr. VIII | Explícita (sin destinatario ni periodicidad) |
| F10 | Recibir planes de mejora y su seguimiento | Art. 20 | Explícita (como receptora) |

---

## 5. Vacíos y ambigüedades que conviene resolver

Están ordenados por impacto. La columna "Cómo resolverlo" distingue lo que la DGETD puede definir en su propio paquete normativo de lo que requiere al Comité.

| # | Vacío | Artículos | Cómo resolverlo |
|---|---|---|---|
| V1 | No consta la fecha de publicación, así que no hay fecha cierta para los plazos | Transitorios PRIMERO y SEGUNDO | Confirmarla de inmediato. |
| V2 | La Plataforma se da por existente | Arts. 4 fr. XVI, 14 fr. IV, 21–24 | Diagnóstico interno de la DGETD; si no existe, informar al Comité. |
| V3 | Nadie fija los **umbrales de calidad** | Art. 20 | La DGETD los propone; el Comité los formaliza. |
| V4 | Registro frente a inventario: los catálogos registrados no son "autorizados". Además, el CUARTO pide metadatos que el art. 12 reserva al Comité (propietario, custodio, clasificación) | Transitorio CUARTO; arts. 4 fr. IV, 5, 12, 14 fr. I | Estatus en el inventario (P1) y datos "propuestos" en el registro. Definir si los catálogos adecuados se vuelven "autorizados" con o sin acuerdo del Comité. |
| V5 | Las fr. II, IV y V del art. 13 no tienen sujeto; tampoco se dice si el Comité interviene en cambios mayores | Art. 13; art. 15 fr. II | Asignarlo en el procedimiento C7. |
| V6 | El "catálogo autorizado" se define como "publicado", pero los catálogos reservados o confidenciales no se publican | Art. 4 fr. IV frente a art. 21 y art. 23 | Publicación con acceso restringido en la Plataforma (art. 23). Conviene una aclaración del Comité. |
| V7 | Faltan criterios objetivos para distinguir estratégico de operativo | Art. 5 | Metodología de la DGETD dentro del dictamen (B3). |
| V8 | Nadie fija la frecuencia de actualización | Arts. 8 fr. VIII, 10 fr. V, 16 fr. I | Fijarla en el dictamen y formalizarla con la aprobación. |
| V9 | No se define la relación con la Política de Gobierno de Datos ni con el Grupo de Trabajo de Calidad de Datos | Art. 19 | Precisar en C9 a quién y por qué canal llegan los reportes. |
| V10 | Retiro sin regulación y sin diferencia entre "inactivo" y "obsoleto" | Art. 9 fr. VIII; art. 7 fr. III | Procedimiento C8 y definiciones en el estándar A1. |
| V11 | La DGETD como custodio se supervisa a sí misma, sin segregación de funciones | Arts. 17, 19, 20 | Separar internamente la operación de la supervisión. |
| V12 | No hay consecuencias por incumplimiento (registro, adecuación, reportes) | Transitorios CUARTO y QUINTO; art. 19 | Prever en el procedimiento un escalamiento al Comité. |
| V13 | No se aclara si los estándares del TERCERO requieren aprobación del Comité ni cómo se versionan | Transitorio TERCERO; art. 14 fr. II | El texto solo exige publicarlos. Conviene presentarlos al Comité para su conocimiento y versionar los propios estándares. |
| V14 | El art. 27 se titula "Periodicidad de revisión" pero no fija ninguna | Art. 27 | Sin acción inmediata. |

---

## 6. Ruta crítica sugerida

1. **Esta semana:** confirmar la fecha de publicación (V1) y el estado de la Plataforma (V2). Con eso se fija el calendario real.
2. **Antes del día 60 (16/12/2026, si se confirma el supuesto):** publicar el paquete del TERCERO.
   - Prioridad 1, porque las áreas los necesitan para el registro: A3 ficha de metadatos, B4 formato de registro, C11 procedimiento de registro y T2 regla de asignación de identificador de catálogo.
   - Prioridad 2: A1, A2, A4, A5; B1, B2, B3, B5, B6; C1–C8.
   - Prioridad 3, que también puede ir en el paquete: D1 indicadores y propuesta de umbrales, B7, B8, C9, C10.
3. **Días 60–90:** operar el registro (T1), dar asesoría (F8) e ir depurando y diagnosticando sobre la marcha (T3, T4), para no esperar al cierre.
4. **Días 90–120:** cerrar el diagnóstico, redactar el plan de adecuación (T5, T6) y agendarlo en sesión del Comité **antes** del día 120.
5. **En paralelo, sin plazo:** procedimientos simplificados (E1, requiere Comité), API (P5) y trazabilidad de uso (P4).

---

*Este análisis interpreta el texto normativo con fines de planeación. No sustituye la interpretación que corresponde al Comité (Transitorio SÉPTIMO).*
