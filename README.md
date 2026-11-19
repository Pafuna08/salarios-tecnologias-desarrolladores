# Tecnologías y salarios de desarrolladores de software

Proyecto individual de ciencia de datos con Python y pandas.

**Aprendiz:** Pablo Enrique Fuenmayor Osuna · Servicio Nacional de Aprendizaje (SENA)

**Actividad actual:** GA1-220501094-01-AA1-EV07 – Preparación, limpieza y estructuración de datos del proyecto individual con Pandas.

## Descripción y propósito

El proyecto estudia qué tecnologías se asocian con mejores salarios en el desarrollo de software. La idea es orientar a quienes estudian o trabajan en el sector sobre qué habilidades aprender. Usa las encuestas anuales de Stack Overflow de 2022 a 2025 y el PIB per cápita de cada país como contexto económico.

El trabajo va por etapas:

1. **Diagnóstico de calidad** (EV06): estructura, tipos, valores faltantes e inconsistencias de cada dataset. Ver [`notebooks/data_quality.ipynb`](notebooks/data_quality.ipynb) y el informe [`reports/data_quality.md`](reports/data_quality.md).
2. **Preparación de los datos** (EV07, esta entrega): limpieza, filtrado, indicadores y combinación de los datasets. Ver [`notebooks/data_preparation.ipynb`](notebooks/data_preparation.ipynb). El resultado queda en `data/processed/`.

## Pregunta analítica

> ¿Qué lenguajes de programación y frameworks se asocian con un salario anual mayor entre desarrolladores profesionales de tiempo completo, y cuánto cambia esa diferencia según los años de experiencia y la región, entre 2022 y 2025?

## Fuentes de datos

| # | Archivo (`data/raw/`) | Fuente | Tamaño | Contenido |
|---|---|---|---:|---|
| 1 | `so_survey_2022.csv` | [Stack Overflow Developer Survey 2022](https://survey.stackoverflow.co/2022) | 109 MB | 73.268 respuestas × 79 columnas |
| 2 | `so_survey_2023.csv` | [Stack Overflow Developer Survey 2023](https://survey.stackoverflow.co/2023) | 159 MB | 89.184 × 84 |
| 3 | `so_survey_2024.csv` | [Stack Overflow Developer Survey 2024](https://survey.stackoverflow.co/2024) | 160 MB | 65.437 × 114 |
| 4 | `so_survey_2025.csv` | [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025) | 141 MB | 49.191 × 172 |
| 5 | `gdp_per_capita_owid.csv` | [Our World in Data – PIB per cápita PPA](https://ourworldindata.org/grapher/gdp-per-capita-worldbank) | 0,3 MB | 7.445 filas país-año (1990–2025), USD PPA constantes de 2021 |
| 6 | `gdp_per_capita_ppp_wb.csv` | [Banco Mundial – NY.GDP.PCAP.PP.CD](https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD) | 0,2 MB | 266 entidades × años 1960–2025, USD PPA corrientes |

También se descargan los diccionarios de preguntas de cada encuesta (`so_schema_<año>.csv`).

**Los datos originales no están en el repositorio.** Cada encuesta pesa más de 100 MB, el límite de GitHub. El script [`scripts/download_data.py`](scripts/download_data.py) los descarga desde las fuentes oficiales: las encuestas vienen del repositorio [StackExchange/Survey](https://github.com/StackExchange/Survey), con licencia [ODbL](https://opendatacommons.org/licenses/odbl/1-0/). Los archivos de `data/raw/` no se modifican: todo lo que se produce va a `data/processed/`, que sí está en el repositorio porque pesa menos de 6 MB.

## Estructura del repositorio

```text
salarios-tecnologias-desarrolladores/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   ├── raw/                         datasets originales (no se versionan; ver download_data.py)
│   └── processed/                   datasets limpios y estructurados
│       ├── developers.parquet
│       ├── developer_languages.parquet
│       ├── developer_frameworks.parquet
│       ├── gdp_per_capita.csv
│       ├── technology_salary.csv
│       └── salary_by_year_region_experience.csv
├── notebooks/
│   ├── 00_environment.ipynb         comprobación del entorno
│   ├── data_quality.ipynb           diagnóstico de calidad (EV06)
│   └── data_preparation.ipynb       limpieza, análisis y estructuración (EV07)
├── reports/
│   ├── data_quality.md              informe del diagnóstico
│   ├── data_quality_structure.csv
│   └── data_quality_findings.csv
└── scripts/
    └── download_data.py             descarga de los datasets originales
```

## Cómo ejecutar el proyecto

Requisitos: **Python 3.12 o superior** y **Git**. Se necesitan unos 600 MB libres en disco para los datos y unos 2 GB de RAM.

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/Pafuna08/salarios-tecnologias-desarrolladores.git
   cd salarios-tecnologias-desarrolladores
   ```

2. Crear y activar el entorno virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows PowerShell: .\.venv\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea la activación, ejecutar una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

3. Instalar las dependencias (pandas, PyArrow, JupyterLab y las suyas):

   ```bash
   python -m pip install -r requirements.txt
   ```

   `requirements.txt` se generó con `pip freeze` en Windows. La única dependencia exclusiva de ese sistema, `pywinpty`, tiene el marcador `; sys_platform == "win32"`, así que el mismo archivo funciona también en macOS y Linux.

4. Descargar los datos originales (unos 570 MB; el script omite los archivos que ya existan):

   ```bash
   python scripts/download_data.py
   ```

5. Abrir JupyterLab y ejecutar los cuadernos en orden (*Run → Run All Cells*): primero `data_quality.ipynb` y después `data_preparation.ipynb`.

   ```bash
   jupyter lab
   ```

   O ejecutarlos completos desde la terminal:

   ```bash
   cd notebooks
   jupyter nbconvert --to notebook --execute --inplace data_quality.ipynb
   jupyter nbconvert --to notebook --execute --inplace data_preparation.ipynb
   ```

   `data_preparation.ipynb` tarda menos de un minuto y vuelve a generar todos los archivos de `data/processed/`.

## Transformaciones realizadas (EV07)

El cuaderno [`data_preparation.ipynb`](notebooks/data_preparation.ipynb) aplica las acciones propuestas en el diagnóstico, en el orden de las lecciones 2, 3 y 4 del material *Preparar y estructurar datos con Python*.

### Limpieza y estandarización

Cada paso es una función. Las funciones se encadenan con `pipe()` y una función de registro anota filas, nulos y memoria después de cada paso. Al final, `assert` comprueba las reglas de los datos limpios.

| Problema | Tratamiento |
|---|---|
| Columnas sin uso (hasta 172 por año, 2 vacías en 2022) | Solo se cargan las 11 columnas necesarias, renombradas en inglés (`snake_case`) |
| Duplicados | 0 exactos. Las 15 respuestas iguales en las 10 columnas no lo son en la encuesta completa, así que se conservan |
| Experiencia como texto (`Less than 1 year`, `More than 50 years`) | Se reemplaza por 0,5 y 51 y se convierte a `Float64` sin perder valores |
| `YearsCodePro` no existe en 2025 | `work_exp` es la variable común. En 2022–2024 se completa con `years_code_pro` (correlación 0,92–0,94) y la fuente queda en `work_exp_source` |
| Experiencia imposible | Se anula si supera 50 años, si es mayor que la edad máxima declarada menos 14, o si `years_code_pro` es mayor que `years_code` |
| `Employment` y `MainBranch` distintos entre años | Dos columnas booleanas: `is_professional` y `full_time`. En 2025 `Employed` se usa como aproximación de tiempo completo |
| Edad | Categoría ordenada; `Prefer not to say` → nulo |
| Países con nombre distinto al de OWID (36,5 % de las respuestas sin PIB) | Tabla de 25 equivalencias; `Nomadic` → nulo |
| Variantes de tecnologías (`React.js`/`React`, `ASP.NET CORE`, `Bash/Shell (all shells)`…) | `strip` y equivalencias: de 58 a 55 lenguajes y de 42 a 39 frameworks |
| Agregados en las fuentes de PIB | Se filtran por `owid_region` (OWID) y por código ISO3 (Banco Mundial) |

Los nulos se trataron según su causa: el salario no se imputa porque es la variable que se quiere explicar; los nulos de lenguajes y frameworks se conservan.

### Filtrado, agrupación e indicadores

- **Población de interés:** desarrolladores profesionales de tiempo completo con salario plausible. Se usan los percentiles 1–99 de cada año, con un piso de 1.000 USD y un tope de 1.000.000 USD. Quedan **104.096 de 277.080 respuestas** (30.686 en 2022, 38.734 en 2023, 18.286 en 2024 y 16.390 en 2025).
- **Categorías:** región continental (de OWID) y cinco niveles de experiencia con `pd.cut`.
- **Salario relativo** con `groupby().transform('median')`. Se divide cada salario entre la mediana de su año, de su año y región, o de su año, región y nivel de experiencia. Así la tecnología no se confunde con el país.
- **Indicadores:**
  1. Prima salarial por lenguaje.
  2. Prima salarial por framework.
  3. Salario por nivel de experiencia.
  4. Salario por región y relación salario / PIB per cápita.
  5. Prima de cada lenguaje según experiencia y región.

### Combinación y estructuración

- `concat` de los cuatro años, validado con la clave `year` + `response_id`, porque `ResponseId` se reinicia cada año.
- `melt` del PIB del Banco Mundial (formato ancho) y `merge(validate='1:1')` con OWID para contrastar las fuentes. OWID queda como fuente principal.
- `pivot` + `ffill` + `melt` para completar el PIB de los años sin dato con el último valor del país.
- `merge(how='left', validate='m:1', indicator=True)` de las respuestas con el PIB: el **99,5 %** encuentra su país.
- `explode` de las tecnologías a tablas puente validadas contra `developers`.
- Exportación a Parquet y CSV. Los Parquet se vuelven a leer para comprobar que quedaron idénticos.

## Datasets procesados (`data/processed/`)

| Archivo | Filas | Una fila por | Uso |
|---|---:|---|---|
| `developers.parquet` | 104.096 | persona de la población de interés | Tabla principal del análisis |
| `developer_languages.parquet` | 540.902 | persona y lenguaje | Agrupar el salario por lenguaje |
| `developer_frameworks.parquet` | 282.657 | persona y framework | Agrupar el salario por framework |
| `gdp_per_capita.csv` | 796 | país y año (2022–2025) | PIB per cápita de las dos fuentes |
| `technology_salary.csv` | 57 | tecnología | Indicadores 1 y 2 |
| `salary_by_year_region_experience.csv` | 120 | año, región y nivel de experiencia | Salario mediano por grupo |

Las tablas puente se unen con `developers` por `year` + `response_id`.

**Columnas de `developers.parquet`:**

| Columna | Tipo | Descripción |
|---|---|---|
| `year`, `response_id` | entero | Clave de la respuesta (año de la encuesta e identificador dentro del año) |
| `country`, `iso3`, `region` | texto / categoría | País con el nombre de OWID, código ISO3 y región continental |
| `age` | categoría ordenada | Rango de edad |
| `work_exp`, `work_exp_source`, `exp_level` | decimal / categoría | Años de experiencia laboral, variable de origen y nivel (0-2, 3-5, 6-10, 11-20, 21+) |
| `salary_usd` | decimal | Salario anual en USD (`ConvertedCompYearly`) |
| `salary_rel_year`, `salary_rel_region` | decimal | Salario dividido entre la mediana del año, o del año y la región |
| `gdp_pc_ppp`, `gdp_year` | decimal / entero | PIB per cápita PPA (OWID, USD de 2021) y año del dato |
| `salary_gdp_ratio` | decimal | Salario dividido entre el PIB per cápita |
| `languages`, `frameworks` | texto | Tecnologías estandarizadas, separadas por `;` |

## Principales resultados

- **Calidad antes y después:**
  - El salario pasa de tener 51,8 % de nulos y un rango de 1 USD a 74 millones de USD a no tener nulos, con un rango de 1.000 USD a 1 millón de USD.
  - La experiencia pasa de texto con 38,8 % de nulos a número con 0,6 %.
  - Las respuestas sin PIB del país bajan de 36,5 % a 0,5 %.
- **Lenguajes:** Scala (+28,6 %), Erlang (+28,3 %), Elixir (+25,0 %), Ruby (+17,9 %), Go (+16,9 %) y Rust (+12,2 %) se asocian con salarios mayores que la mediana de su región. PHP (−16,7 %), VBA, Dart y MATLAB, con salarios menores.
- **Frameworks:** Phoenix (+26,9 %) y Ruby on Rails (+16,5 %) encabezan la lista. Laravel (−23,3 %) y Symfony (−13,4 %) la cierran. Los más usados, React y Node.js, quedan cerca de 0 %.
- **Experiencia y región pesan más que la tecnología:**
  - El salario mediano se multiplica por 2,8–3,6 entre 0–2 y más de 20 años.
  - La mediana de América del Norte (135.000 USD) es 6,6 veces la de África.
  - Las primas de las tecnologías son mucho mayores en Asia y África que en Europa y Oceanía.
- **Limitaciones:** en 2025 no se distingue el tiempo completo; la muestra es voluntaria y se concentra en cinco países (48 %); los resultados son asociaciones, no causas.

## Historial de versiones

El repositorio sigue la guía *Proyecto práctica: entorno y cuaderno*: `main` guarda las versiones estables, `develop` integra el trabajo y cada fase se desarrolla en su propia rama.

| Versión | Contenido |
|---|---|
| `v0.1` | Estructura, `.gitignore` y entorno virtual |
| `v0.2` | pandas instalado y `requirements.txt` |
| `v0.3` | JupyterLab en el mismo entorno |
| `v0.4` | Cuaderno de comprobación del entorno |
| `v0.5` | Diagnóstico de calidad (EV06): script de descarga, cuaderno, informe y README |
| `feature/project-data-preparation` | Preparación de los datos (EV07): estructura con nombres en inglés, limpieza, indicadores, datasets procesados y README |

## Herramientas

Python 3.14 · pandas 3.1 · NumPy 2.5 · PyArrow 26 · JupyterLab 4.6 · Git y GitHub
