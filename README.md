# Tecnologías y salarios de desarrolladores de software

Proyecto individual de ciencia de datos con Python y pandas.

**Aprendiz:** Pablo Enrique Fuenmayor Osuna · Servicio Nacional de Aprendizaje (SENA)

**Actividad actual:** GA1-220501094-01-AA1-EV06 – Diagnosticar la calidad de datos: preparación, exploración y documentación.

## Descripción y propósito

El proyecto estudia qué tecnologías se asocian con mejores salarios en el desarrollo de software. La idea es orientar a quienes estudian o trabajan en el sector sobre qué habilidades aprender. Usa las encuestas anuales de Stack Overflow de 2022 a 2025 y el PIB per cápita de cada país como contexto económico.

En esta etapa se hace el **diagnóstico inicial de calidad** de todos los datasets: estructura, tipos de datos, valores faltantes, inconsistencias y acciones de limpieza propuestas. Todavía no se limpia ni se modela.

## Pregunta analítica

> ¿Qué lenguajes de programación y frameworks se asocian con un salario anual mayor entre desarrolladores profesionales de tiempo completo, y cuánto cambia esa diferencia según los años de experiencia y la región, entre 2022 y 2025?

## Datasets

| # | Archivo (`data/raw/`) | Fuente | Tamaño | Contenido |
|---|---|---|---:|---|
| 1 | `so_survey_2022.csv` | [Stack Overflow Developer Survey 2022](https://survey.stackoverflow.co/2022) | 109 MB | 73.268 respuestas × 79 columnas |
| 2 | `so_survey_2023.csv` | [Stack Overflow Developer Survey 2023](https://survey.stackoverflow.co/2023) | 159 MB | 89.184 × 84 |
| 3 | `so_survey_2024.csv` | [Stack Overflow Developer Survey 2024](https://survey.stackoverflow.co/2024) | 160 MB | 65.437 × 114 |
| 4 | `so_survey_2025.csv` | [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025) | 141 MB | 49.191 × 172 |
| 5 | `pib_per_capita_owid.csv` | [Our World in Data – PIB per cápita PPA](https://ourworldindata.org/grapher/gdp-per-capita-worldbank) | 0,3 MB | 7.445 filas país-año (1990–2025) |
| 6 | `pib_per_capita_ppa_bm.csv` | [Banco Mundial – NY.GDP.PCAP.PP.CD](https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD) | 0,2 MB | 266 entidades × años 1960–2025 |

También se descargan los diccionarios de preguntas de cada encuesta (`so_schema_<año>.csv`).

**Los datos no están en el repositorio.** Cada encuesta pesa más de 100 MB, el límite de GitHub. El script [`scripts/descargar_datos.py`](scripts/descargar_datos.py) los descarga desde las fuentes oficiales: las encuestas vienen del repositorio [StackExchange/Survey](https://github.com/StackExchange/Survey), con licencia [ODbL](https://opendatacommons.org/licenses/odbl/1-0/).

## Estructura del repositorio

```text
salarios-tecnologias-desarrolladores/
├── .venv/                          (ignorada: entorno virtual)
├── data/
│   └── raw/                        (ignorada: datasets descargados)
│       └── .gitkeep
├── notebooks/
│   ├── 00_entorno.ipynb            comprobación del entorno
│   └── diagnostico_calidad.ipynb   carga, inspección y diagnóstico
├── reports/
│   ├── informe_diagnostico.md      informe técnico
│   ├── tabla_diagnostico_estructural.csv
│   └── tabla_hallazgos.csv
├── scripts/
│   └── descargar_datos.py          descarga de los datasets
├── .gitignore
├── requirements.txt
└── README.md
```

## Cómo reproducir el diagnóstico

Requisitos: **Python 3.12 o superior** y **Git**. Se necesitan unos 600 MB libres en disco para los datos y unos 2 GB de RAM para cargar las cuatro encuestas a la vez.

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

3. Instalar las dependencias (pandas, JupyterLab y las suyas):

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Descargar los datos (unos 570 MB; el script omite los archivos que ya existan):

   ```bash
   python scripts/descargar_datos.py
   ```

5. Abrir JupyterLab y ejecutar el cuaderno `notebooks/diagnostico_calidad.ipynb` (*Run → Run All Cells*):

   ```bash
   jupyter lab
   ```

   O ejecutarlo completo desde la terminal:

   ```bash
   jupyter nbconvert --to notebook --execute --inplace notebooks/diagnostico_calidad.ipynb
   ```

   El cuaderno vuelve a generar `reports/tabla_diagnostico_estructural.csv` y `reports/tabla_hallazgos.csv`.

## Principales resultados

El detalle está en el [informe técnico](reports/informe_diagnostico.md). En resumen:

- **Salario:** entre 46 % y 64 % de nulos en el total (26 %–53 % dentro de la población de interés), con valores desde 1 USD hasta 74 millones de USD. Hay que excluir los nulos, recortar los atípicos y usar la mediana.
- **Experiencia:** `YearsCodePro` se lee como texto por las etiquetas `Less than 1 year` y `More than 50 years`, y desaparece en 2025. Hay casos imposibles, como `WorkExp` de 100 años.
- **Comparabilidad entre años:** en 2025 `Employment` no distingue el tiempo completo, y cambian los nombres de tecnologías (`React.js`/`React`, `ASP.NET Core`), `RemoteWork` y `Currency`.
- **Selección múltiple:** lenguajes y frameworks vienen en una sola celda separados por `;`.
- **Unión con el PIB:** cerca del 30 % de las respuestas tienen un nombre de país que no coincide con OWID. Las dos fuentes de PIB usan unidades distintas e incluyen agregados regionales.
- **Conclusión:** los datos sirven para responder la pregunta después de aplicar las acciones de limpieza propuestas. Quedan 105.748 profesionales a tiempo completo con salario y lenguajes informados en los cuatro años.

## Historial de versiones

El repositorio sigue la guía *Proyecto práctica: entorno y cuaderno*: `main` guarda las versiones estables, `develop` integra el trabajo y cada fase se desarrolla en una rama `feat/*`.

| Tag | Contenido |
|---|---|
| `v0.1` | Estructura, `.gitignore` y entorno virtual |
| `v0.2` | pandas instalado y `requirements.txt` |
| `v0.3` | JupyterLab en el mismo entorno |
| `v0.4` | Cuaderno `00_entorno.ipynb` |
| `v0.5` | Diagnóstico de calidad: script de descarga, cuaderno, informe y README |

## Herramientas

Python 3.14 · pandas 3.1 · NumPy 2.5 · JupyterLab 4.6 · Git y GitHub
