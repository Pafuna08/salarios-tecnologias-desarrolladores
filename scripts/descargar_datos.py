"""Descarga los datasets del proyecto en data/raw/.

Los archivos de la encuesta de Stack Overflow pesan más de 100 MB cada uno
(límite de GitHub), por eso no se versionan: este script los obtiene desde
las fuentes oficiales. Solo usa la biblioteca estándar de Python.

Uso (desde la raíz del proyecto, con el entorno activo):
    python scripts/descargar_datos.py            # descarga lo que falte
    python scripts/descargar_datos.py --forzar   # vuelve a descargar todo
"""

import argparse
import io
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "data" / "raw"

SO_BASE = "https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive"
ANIOS = [2022, 2023, 2024, 2025]

# nombre local -> URL de origen
ARCHIVOS = {}
for anio in ANIOS:
    ARCHIVOS[f"so_survey_{anio}.csv"] = f"{SO_BASE}/{anio}/results.csv"
    ARCHIVOS[f"so_schema_{anio}.csv"] = f"{SO_BASE}/{anio}/schema.csv"
ARCHIVOS["pib_per_capita_owid.csv"] = (
    "https://ourworldindata.org/grapher/gdp-per-capita-worldbank.csv"
    "?v=1&csvType=full&useColumnShortNames=true"
)

# El Banco Mundial entrega un .zip; de él se extrae el CSV principal.
BANCO_MUNDIAL_URL = (
    "https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.PP.CD?downloadformat=csv"
)
BANCO_MUNDIAL_ARCHIVO = "pib_per_capita_ppa_bm.csv"


def descargar(url, destino):
    """Descarga url en destino mostrando el avance en MB."""
    temporal = destino.with_suffix(destino.suffix + ".part")
    with urllib.request.urlopen(url, timeout=120) as resp, open(temporal, "wb") as f:
        total = int(resp.headers.get("Content-Length") or 0)
        leido = 0
        while bloque := resp.read(1024 * 1024):
            f.write(bloque)
            leido += len(bloque)
            if total:
                print(f"\r  {leido / 1e6:7.1f} / {total / 1e6:.1f} MB", end="", flush=True)
    print()
    temporal.replace(destino)


def descargar_banco_mundial(destino):
    with urllib.request.urlopen(BANCO_MUNDIAL_URL, timeout=120) as resp:
        contenido = resp.read()
    with zipfile.ZipFile(io.BytesIO(contenido)) as z:
        principal = [n for n in z.namelist() if n.startswith("API_") and n.endswith(".csv")]
        if not principal:
            raise RuntimeError(f"No se encontró el CSV principal en el zip: {z.namelist()}")
        with z.open(principal[0]) as origen, open(destino, "wb") as f:
            shutil.copyfileobj(origen, f)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--forzar", action="store_true", help="vuelve a descargar aunque exista")
    args = parser.parse_args()

    DESTINO.mkdir(parents=True, exist_ok=True)
    errores = []

    tareas = list(ARCHIVOS.items()) + [(BANCO_MUNDIAL_ARCHIVO, None)]
    for nombre, url in tareas:
        ruta = DESTINO / nombre
        if ruta.exists() and not args.forzar:
            print(f"[ya existe] {nombre}")
            continue
        print(f"[descargando] {nombre}")
        try:
            if url is None:
                descargar_banco_mundial(ruta)
            else:
                descargar(url, ruta)
        except Exception as e:  # se informa y se sigue con los demás
            errores.append((nombre, e))
            print(f"  ERROR: {e}")

    if errores:
        print(f"\n{len(errores)} archivo(s) con error. Vuelve a ejecutar el script.")
        sys.exit(1)
    print(f"\nListo. Archivos en {DESTINO}")


if __name__ == "__main__":
    main()
