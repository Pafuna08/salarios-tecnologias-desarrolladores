# Informe técnico: diagnóstico inicial de calidad de datos

**Actividad:** GA1-220501094-01-AA1-EV06 – Diagnosticar la calidad de datos: preparación, exploración y documentación
**Aprendiz:** Pablo Enrique Fuenmayor Osuna
**Institución:** Servicio Nacional de Aprendizaje (SENA)
**Fecha:** 3 de noviembre de 2026
**Herramientas:** Python 3.14, pandas 3.1, JupyterLab 4.6
**Cuaderno de respaldo:** [`notebooks/diagnostico_calidad.ipynb`](../notebooks/diagnostico_calidad.ipynb)

Todas las cifras de este informe salen de la ejecución de ese cuaderno. Las tablas completas también están en [`tabla_diagnostico_estructural.csv`](tabla_diagnostico_estructural.csv) y [`tabla_hallazgos.csv`](tabla_hallazgos.csv).

---

## 1. Proyecto y pregunta analítica

**Proyecto:** Tecnologías y salarios de desarrolladores de software.

**Propósito:** identificar qué tecnologías se asocian con mejores salarios en el desarrollo de software, para orientar a quienes estudian o trabajan en el sector sobre qué habilidades aprender.

**Pregunta analítica:**

> ¿Qué lenguajes de programación y frameworks se asocian con un salario anual mayor entre desarrolladores profesionales de tiempo completo, y cuánto cambia esa diferencia según los años de experiencia y la región, entre 2022 y 2025?

**Población de interés:** personas que responden *"I am a developer by profession"* en `MainBranch` y que trabajan a tiempo completo según `Employment`.

## 2. Datasets utilizados

| # | DataFrame | Fuente | Contenido | Uso en el proyecto |
|---|---|---|---|---|
| 1 | `so_2022` | [Stack Overflow Developer Survey](https://survey.stackoverflow.co/) 2022 | Una fila por persona encuestada: perfil, empleo, experiencia, tecnologías y salario | Salario (`ConvertedCompYearly`), lenguajes (`LanguageHaveWorkedWith`), frameworks (`WebframeHaveWorkedWith`), experiencia (`YearsCodePro`, `WorkExp`) y país (`Country`) |
| 2 | `so_2023` | Stack Overflow Developer Survey 2023 | Ídem | Ídem |
| 3 | `so_2024` | Stack Overflow Developer Survey 2024 | Ídem | Ídem |
| 4 | `so_2025` | Stack Overflow Developer Survey 2025 | Ídem | Ídem |
| 5 | `pib_owid` | [Our World in Data](https://ourworldindata.org/grapher/gdp-per-capita-worldbank), con datos del Banco Mundial | PIB per cápita PPA en USD internacionales constantes de 2021, una fila por país y año | Contexto económico para comparar salarios entre regiones |
| 6 | `pib_bm` | [Banco Mundial](https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD), `NY.GDP.PCAP.PP.CD` | PIB per cápita PPA en USD internacionales corrientes, una columna por año | Segunda fuente para contrastar |

Las encuestas se descargan del repositorio oficial [StackExchange/Survey](https://github.com/StackExchange/Survey), junto con su diccionario de preguntas (`so_schema_<año>.csv`). Cada encuesta pesa entre 109 y 160 MB, más que el límite de GitHub, así que no se versionan: se obtienen con `scripts/descargar_datos.py`.

## 3. Resultados de la inspección estructural

En cada DataFrame se ejecutaron `head()`, `tail()`, `shape`, `columns`, `dtypes`, `info()`, `describe()` y `describe(include='object')`.

| Dataset | Filas | Columnas | Tipos de datos | % celdas nulas | Observaciones |
|---|---:|---:|---|---:|---|
| `so_2022` | 73.268 | 79 | str: 73, float64: 5, int64: 1 | 28,4 | `YearsCode` y `YearsCodePro` como texto; tecnologías y `DevType` en selección múltiple con `;`; salario de 1 a 50 M USD; 2 columnas `VCHosting*` 100 % vacías |
| `so_2023` | 89.184 | 84 | str: 80, float64: 3, int64: 1 | 33,6 | Misma estructura que 2022; `YearsCodePro` sigue como texto; salario máximo de ~74 M USD |
| `so_2024` | 65.437 | 114 | str: 100, float64: 13, int64: 1 | 38,8 | Salario con la mayor proporción de nulos; `Currency` con dos formatos; cambios de nombre en frameworks |
| `so_2025` | 49.191 | 172 | str: 119, float64: 52, int64: 1 | 52,4 | Sin `YearsCodePro` (solo `WorkExp`); `Employment` no distingue tiempo completo; más nulos en tecnologías y país |
| `pib_owid` | 7.445 | 5 | str: 3, int64: 1, float64: 1 | 1,3 | Formato largo país-año sin nulos en el PIB; incluye agregados (`owid_region` nula); USD PPA constantes de 2021 |
| `pib_bm` | 266 | 71 | float64: 67, str: 4 | 48,0 | Formato ancho (un año por columna); columna vacía `Unnamed: 70`; incluye agregados; USD PPA corrientes |

**Características principales:**

- **Encuestas:** casi todas las columnas son texto (`str`, el tipo de texto de pandas 3). Muchas son preguntas de selección múltiple guardadas en una sola celda y separadas por `;`. Por ejemplo, más del 93 % de las respuestas de `LanguageHaveWorkedWith` tienen más de un lenguaje. `ResponseId` es único en los cuatro años y no hay filas duplicadas. El número de columnas crece cada año (de 79 a 172), sobre todo por las preguntas nuevas sobre IA. Por eso el porcentaje global de celdas nulas sube, aunque esas preguntas no se usan en el proyecto.
- **PIB OWID:** tabla larga y limpia, con `year` como entero y el PIB como decimal, sin nulos en el PIB ni pares país-año repetidos. Cubre de 1990 a 2025.
- **PIB Banco Mundial:** tabla ancha, de 1960 a 2025, con 4 líneas de metadatos antes del encabezado; por eso se cargó con `skiprows=4`. El 48 % de celdas nulas se debe sobre todo a años antiguos sin dato y a la columna vacía.

## 4. Valores faltantes, tipos de datos e inconsistencias

### 4.1 Valores faltantes

Porcentaje de nulos en las variables clave, sobre el total de respuestas:

| Variable | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|
| `MainBranch` | 0,0 | 0,0 | 0,0 | 0,0 |
| `Employment` | 2,1 | 1,4 | 0,0 | 1,7 |
| `Country` | 2,0 | 1,4 | 9,9 | **28,0** |
| `YearsCodePro` | 29,3 | 25,8 | 21,1 | *no existe* |
| `WorkExp` | 49,8 | 51,1 | 54,7 | 12,8 |
| `LanguageHaveWorkedWith` | 3,1 | 2,3 | 8,7 | **35,6** |
| `WebframeHaveWorkedWith` | 26,9 | 24,9 | 31,0 | **53,3** |
| `ConvertedCompYearly` (salario) | **48,0** | **46,2** | **64,2** | **51,3** |

Muchos de esos nulos se deben al diseño de la encuesta: el salario no se pregunta a estudiantes ni a desempleados. Por eso se midió también dentro de la población de interés:

| Año | Profesionales a tiempo completo | % salario nulo | % lenguajes nulo | % frameworks nulo | % país nulo | Con salario y lenguajes |
|---|---:|---:|---:|---:|---:|---:|
| 2022 | 43.199 | 26,6 | 0,4 | 20,9 | 0,0 | 31.647 |
| 2023 | 53.663 | 26,2 | 0,4 | 20,2 | 0,0 | 39.529 |
| 2024 | 39.937 | **52,8** | 8,0 | 27,2 | 9,7 | 18.785 |
| 2025 | 28.774 | **41,3** | **32,3** | **48,1** | **25,8** | 15.787 |

*En 2025 "tiempo completo" se aproxima con `Employment == "Employed"` (ver 4.4).*

**Cómo afecta al análisis:**

- El salario es la variable que se quiere explicar. Imputarlo inventaría el resultado, así que **las filas sin salario se excluyen**. Esto deja de 15.787 a 39.529 casos útiles por año: suficientes para las tecnologías populares, pero pocos para las tecnologías y países poco frecuentes.
- En 2024 el salario falta en más de la mitad de la población. Una causa identificable es que **10.305 personas escribieron un monto en `CompTotal` que no se convirtió a USD**, incluso cuando la moneda era el dólar. Además, `CompTotal` llega a 1×10¹⁵⁰, lo que sugiere que Stack Overflow descartó montos poco creíbles al convertir.
- En 2025 faltan muchos más lenguajes, frameworks y países que en los años anteriores. Eso reduce los casos del último año y hace menos precisa la comparación temporal.
- En `pib_bm` faltan datos de 2025 para 33 entidades (19 en 2022). En `pib_owid` hay 198 entidades con dato en 2025 (212 en 2022).

### 4.2 Tipos de datos

| Variable | Tipo leído | Tipo correcto | Causa |
|---|---|---|---|
| `YearsCodePro`, `YearsCode` (2022–2024) | `str` | numérico | Etiquetas de texto `Less than 1 year` (hasta 2.856 casos) y `More than 50 years` (hasta 353 casos) |
| `YearsCode`, `WorkExp` (2025) | `float64` | numérico | Ya vienen numéricos: **la misma variable cambia de tipo entre años** |
| `LanguageHaveWorkedWith`, `WebframeHaveWorkedWith` | `str` | lista de categorías | Selección múltiple en una celda (`JavaScript;TypeScript`) |
| `DevType` | `str` | categoría | Selección múltiple en 2022 (60,8 % con varias opciones), única desde 2023 |
| `Employment` | `str` | categoría | Selección múltiple en 2022–2024 (~15 % con varias opciones) |
| `VCHostingPersonal use`, `VCHostingProfessional use` (2022) | `float64` | — | Columnas 100 % vacías: pandas les asigna `float64` porque solo hay `NaN` |
| Años de `pib_bm` (`1960` … `2025`) | nombres de columna `str` | filas con año `int` | Formato ancho |
| `Unnamed: 70` (`pib_bm`) | `float64` | — | Columna vacía creada por la coma final de cada línea del CSV |

Los tipos de `ResponseId` (`int64`), `ConvertedCompYearly` y `CompTotal` (`float64`), y de `year` y el PIB en `pib_owid`, son coherentes con lo que representan.

### 4.3 Posibles inconsistencias

**Salarios atípicos o imposibles** (`ConvertedCompYearly`, USD/año):

| Año | n | Mínimo | Mediana | Media | Percentil 99 | Máximo | < 1.000 USD | > 1 M USD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | 38.071 | 1 | 67.845 | 170.761 | 2.161.310 | 50.000.000 | 337 | 865 |
| 2023 | 48.019 | 1 | 74.963 | 103.110 | 400.000 | 74.351.432 | 684 | 60 |
| 2024 | 23.435 | 1 | 65.000 | 86.155 | 393.751 | 16.256.603 | 545 | 41 |
| 2025 | 23.947 | 1 | 75.320 | 101.762 | 440.856 | 50.000.000 | 724 | 46 |

La media queda muy por encima de la mediana, y en 2022 el percentil 99 supera los 2 millones de USD. Hay salarios de 1 USD y de decenas de millones: probablemente errores de digitación, de moneda o de frecuencia (un salario mensual escrito como anual).

**Experiencia incoherente:**

| Año | `WorkExp` máximo | `WorkExp` > 50 | Experiencia mayor que la edad permite* | `YearsCodePro` > `YearsCode` |
|---|---:|---:|---:|---:|
| 2022 | 50 | 0 | 111 | 544 |
| 2023 | 50 | 0 | 141 | 691 |
| 2024 | 50 | 0 | 107 | 504 |
| 2025 | **100** | **147** | 119 | — |

\* `WorkExp` mayor que la edad máxima del rango declarado menos 14 años.

**Categorías y nombres que cambian entre años:**

- `Employment`: hasta 2024 distingue `Employed, full-time` y `Employed, part-time`; en 2025 solo existe `Employed`.
- `RemoteWork`: `Fully remote` / `Full in-person` en 2022, `Remote` / `In-person` en 2023–2024, y cinco opciones nuevas en 2025.
- `Age`: 2025 elimina la opción `Under 18 years old`.
- `Currency`: mezcla `USD\tUnited States dollar` (con tabulador) y `EUR European Euro` (con espacio); en 2025 predomina el segundo formato.
- Tecnologías: `ASP.NET Core ` (con espacio final, 2022), `ASP.NET CORE` (2023–2024) y `ASP.NET Core` (2025); `React.js` y `React`; `Angular.js` y `AngularJS`; `Bash/Shell` y `Bash/Shell (all shells)`; `COBOL` y `Cobol`; `LISP` y `Lisp`. Solo 31 lenguajes y 20 frameworks aparecen con el mismo nombre en los cuatro años.

**Países que no coinciden con las fuentes de PIB:**

Entre 28 y 30 países por año no coinciden con los nombres de OWID, y esos países reúnen **del 29,7 % al 32,2 % de las respuestas**. Los de más respuestas son `United States of America` (13.543 en 2022), `United Kingdom of Great Britain and Northern Ireland`, `Russian Federation`, `Iran, Islamic Republic of...`, `Czech Republic`, `Viet Nam`, `Taiwan` y `Hong Kong (S.A.R.)`. También aparece `Nomadic`, que no es un país.

**Fuentes de PIB:**

- `pib_bm` incluye 68 entidades que no son países en OWID: agregados como `Arab World`, `Euro area` y `High income`, más algunos territorios. `pib_owid` incluye 13 agregados (`World`, `High-income countries`, regiones del BM).
- Las dos fuentes usan **unidades distintas**. Para 2023, el valor del Banco Mundial (USD corrientes) es entre 11 % y 16 % mayor que el de OWID (USD constantes de 2021) en Colombia, EE. UU., India, Alemania y Brasil. No se deben mezclar.
- No hay duplicados de país-año en ninguna de las dos.

### 4.4 Limitaciones para responder la pregunta

1. **2025 no distingue tiempo completo.** La población de 2025 incluye medio tiempo y no es exactamente comparable con 2022–2024.
2. **La experiencia no es homogénea.** 2025 no tiene `YearsCodePro`. La única variable común a los cuatro años es `WorkExp`, que en 2022–2024 tiene alrededor de 50 % de nulos en el total.
3. **Muestra no aleatoria.** Responden usuarios de Stack Overflow que quieren participar. EE. UU. aporta entre 18,8 % y 21,2 % de las respuestas, y los 5 países principales reúnen entre 44 % y 46 %. Entre 73 y 99 países tienen menos de 30 respuestas, así que no se pueden sacar conclusiones por país; hay que agrupar por región.
4. **Salario autodeclarado** y convertido a USD con la tasa de cambio de cada año. No está ajustado por costo de vida, por eso se necesita el contexto del PIB PPA o comparar dentro de cada región.
5. **Asociación, no causalidad.** Un salario mayor asociado a una tecnología puede reflejar el país, el tipo de empresa o el cargo, no la tecnología en sí.
6. **Opciones que cambian.** Las tecnologías que no se ofrecían todos los años (p. ej. `Spring Boot` no era una opción en 2022; aparece desde 2023) no se pueden comparar en el tiempo.

## 5. Principales hallazgos de calidad por dataset

| Dataset | Problema identificado | Evidencia encontrada | Posible impacto | Acción propuesta |
|---|---|---|---|---|
| Encuestas 2022–2025 | Valores faltantes en el salario (variable objetivo) | `ConvertedCompYearly` nulo: 48,0 % (2022), 46,2 %, 64,2 %, 51,3 % (2025); 52,8 % en la población de interés de 2024 | Menos casos por tecnología; 2024 queda con menos representación | Filtrar la población de interés y excluir filas sin salario; no imputar la variable objetivo |
| Encuestas 2022–2025 | Salarios atípicos o imposibles | Mínimo 1 USD en los 4 años; máximo 74.351.432 USD; 1.012 respuestas > 1 M USD y 2.290 < 1.000 USD | La media se distorsiona y las diferencias entre tecnologías pueden ser falsas | Usar la mediana; recortar por percentiles 1–99 por año (o por país) y documentar el criterio |
| Encuestas 2022–2024 | Años de experiencia como texto | `YearsCodePro` y `YearsCode` de tipo `str` por `Less than 1 year` y `More than 50 years` | No se pueden calcular rangos ni estadísticas de experiencia | Reemplazar esas etiquetas (0,5 y 51) y convertir con `pd.to_numeric` |
| Encuesta 2025 | Variable de experiencia profesional eliminada | `YearsCodePro` no existe en 2025; solo `WorkExp` | La experiencia no es comparable entre los 4 años con la misma variable | Usar `WorkExp` como variable común y documentarlo |
| Encuestas 2022–2025 | Experiencia incoherente | `WorkExp` máximo en 2025 = 100; 478 casos con más experiencia que la que permite la edad; 1.739 con más años profesionales que años programando (2022–2024) | Sesga el análisis por nivel de experiencia | Marcar y excluir respuestas incoherentes con reglas explícitas |
| Encuesta 2025 | `Employment` no distingue tiempo completo | Categorías de 2025: `Employed`, `Student`, … en lugar de `Employed, full-time` | La población de 2025 no es la misma que pide la pregunta | Usar `Employed` como aproximación y declararlo como limitación, o limitar ese corte a 2022–2024 |
| Encuestas 2022–2025 | Selección múltiple en una sola celda | `LanguageHaveWorkedWith` y `WebframeHaveWorkedWith` con varias opciones separadas por `;` | No se puede agrupar el salario por tecnología directamente | Separar con `str.split(';')` + `explode()` o crear columnas indicadoras por tecnología |
| Encuestas 2022–2025 | Etiquetas que cambian entre años | `RemoteWork`, `Employment` y `Age` con etiquetas distintas; `Currency` con 2 formatos; `ASP.NET Core ` / `ASP.NET CORE` / `ASP.NET Core`; `React.js` / `React` | Al unir los años se crean categorías falsas o duplicadas | Armonizar con un diccionario de equivalencias y `str.strip()` |
| Encuesta 2025 | Más nulos en tecnologías y país | `LanguageHaveWorkedWith` nulo 35,6 % y `Country` 28,0 % en 2025 | Menos casos por tecnología y región en el último año | Excluir esas filas del análisis por tecnología o región y reportar el tamaño de muestra por año |
| Encuestas vs. PIB | Nombres de país no coinciden | ~30 países sin coincidencia con OWID (p. ej. `United States of America`, `United Kingdom of Great Britain and Northern Ireland`, `Russian Federation`) | Al unir se perdería cerca del 30 % de las respuestas | Crear una tabla de equivalencias de países o unir por código ISO3; excluir `Nomadic` |
| `so_2022` | Columnas completamente vacías | `VCHostingPersonal use` y `VCHostingProfessional use`: 73.268 nulos de 73.268 filas (100 %) | No aportan información y ocupan memoria | Eliminarlas con `drop(columns=...)` |
| `pib_bm` | Formato ancho y columnas sin información | Un año por columna (texto); `Unnamed: 70` vacía; `Indicator Name` e `Indicator Code` constantes | No se puede unir por año directamente | Eliminar columnas vacías y constantes; pasar a formato largo con `melt` y convertir el año a `int` |
| `pib_bm` / `pib_owid` | Agregados mezclados con países y unidades distintas | `pib_bm`: 68 entidades que no son países de OWID; OWID usa USD PPA constantes de 2021 y BM USD PPA corrientes | Se podrían unir regiones como si fueran países, o mezclar unidades | Filtrar solo países; usar una sola fuente (OWID) como principal y BM como contraste |
| `pib_bm` | PIB 2025 incompleto | 33 entidades sin dato en 2025 (vs. 19 en 2022) | Algunos países no tendrían contexto económico en 2025 | Usar el último año disponible por país y documentarlo |

## 6. Acciones de limpieza y preparación propuestas

En orden de aplicación, para un siguiente cuaderno de limpieza (`notebooks/01_limpieza.ipynb`):

1. **Seleccionar columnas** relevantes de cada encuesta (`ResponseId`, `MainBranch`, `Employment`, `Country`, `Age`, `YearsCodePro`, `WorkExp`, `LanguageHaveWorkedWith`, `WebframeHaveWorkedWith`, `ConvertedCompYearly`) y agregar una columna `anio`.
2. **Filtrar la población de interés:** desarrolladores profesionales a tiempo completo; en 2025, `Employed`, documentado como aproximación.
3. **Excluir filas sin salario** (sin imputar) y **tratar los atípicos**: recortar fuera de los percentiles 1–99 de cada año y comparar resultados con y sin recorte.
4. **Convertir la experiencia a número:** `Less than 1 year` → 0,5 y `More than 50 years` → 51, luego `pd.to_numeric`. Usar `WorkExp` como variable común y marcar los casos incoherentes (experiencia mayor que la edad permite, `WorkExp` > 50, `YearsCodePro` > `YearsCode`).
5. **Armonizar etiquetas** entre años con un diccionario de equivalencias y `str.strip()` (tecnologías, `RemoteWork`, `Currency`).
6. **Separar la selección múltiple** de lenguajes y frameworks con `str.split(';')` y `explode()`, conservando `ResponseId`.
7. **Unir los cuatro años** en un único DataFrame con `pd.concat`.
8. **Preparar el PIB:** usar OWID como fuente principal; filtrar solo países (`owid_region` no nula); en BM, eliminar `Unnamed: 70`, `Indicator Name` e `Indicator Code`, pasar a formato largo con `melt`, convertir el año a `int` y quitar agregados.
9. **Tabla de equivalencias de países** entre la encuesta y OWID (p. ej. `United States of America` → `United States`). Excluir `Nomadic` y agregar una columna de región.
10. **Guardar el resultado** en `data/processed/` y documentar cada decisión en el README.

## 7. Conclusiones

1. **Los datos permiten responder la pregunta, pero no en bruto.** Las cuatro encuestas tienen salario, tecnologías, experiencia y país para un total de 105.748 desarrolladores profesionales a tiempo completo con salario y lenguajes informados (31.647 + 39.529 + 18.785 + 15.787). Las dos fuentes de PIB cubren 2022–2025 para casi todos los países.
2. **El salario es el punto más delicado.** Entre 26 % y 53 % de la población de interés no lo informa, y hay valores desde 1 USD hasta 74 millones. Con la mediana y un recorte de atípicos documentado es utilizable.
3. **Los cuatro años no son directamente comparables.** Cambian las categorías de empleo, la variable de experiencia profesional, los nombres de las tecnologías y el formato de la moneda. Hay que armonizarlos antes de unirlos, y declarar como limitación que en 2025 no se puede separar el tiempo completo.
4. **Para analizar por región** hay que construir una tabla de equivalencias de países, que hoy dejaría fuera cerca del 30 % de las respuestas, filtrar los agregados y usar una sola unidad de PIB. Por la concentración de respuestas en pocos países, conviene agrupar por región y no por país.
5. **Estado para continuar:** el diagnóstico no encontró problemas que impidan el proyecto. Con las acciones de la sección 6, los datos quedan en condiciones de iniciar el análisis de salarios por tecnología, experiencia y región.
