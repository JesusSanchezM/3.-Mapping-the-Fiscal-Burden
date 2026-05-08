import requests
import zipfile
import sys
from tqdm import tqdm
from pathlib import Path

# Añadir la raíz al path para poder importar config
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from config.paths import RAW_DIR

# URL base del INEGI para microdatos ENIGH Nueva Serie
BASE_URL = "https://www.inegi.org.mx/contenidos/programas/enigh/nc/{year}/microdatos/enigh{year}_ns_{module}_csv.zip"

YEARS = [2018, 2024]
# Módulos clave para análisis de incidencia fiscal (Ingresos y Gastos)
MODULES = ["ingresos", "gastoshogar", "concentradohogar", "poblacion", "gastospersona", "trabajos"]

def download_and_extract(year, module):
    url = BASE_URL.format(year=year, module=module)
    zip_path = RAW_DIR / f"{module}_{year}.zip"
    final_csv_name = f"{module}_{year}.csv"

    if (RAW_DIR / final_csv_name).exists():
        print(f"⏭️  {final_csv_name} ya existe. Saltando...")
        return

    try:
        with requests.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            print(f"⬇️  Descargando {module} {year}...")

            with open(zip_path, "wb") as f, tqdm(
                total=total_size, unit='B', unit_scale=True
            ) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            csv_files = [f for f in zip_ref.namelist() if f.lower().endswith(".csv")]

            if not csv_files:
                raise ValueError("No CSV encontrado en el ZIP")

            file_name = csv_files[0]
            zip_ref.extract(file_name, RAW_DIR)
            (RAW_DIR / file_name).replace(RAW_DIR / final_csv_name)

            print(f"   ✅ Guardado como: {final_csv_name}")

        zip_path.unlink()

    except KeyboardInterrupt:
        print("\n⛔ Descarga interrumpida. Limpiando...")
        if zip_path.exists():
            zip_path.unlink()
        raise

    except Exception as e:
        print(f"❌ Error en {module} {year}: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando descarga para Análisis de Incidencia Fiscal...\n")
    for year in YEARS:
        for module in MODULES:
            download_and_extract(year, module)
    print("\n✨ Proceso de descarga finalizado.")   



# WRITE "python3 fiscal_incidence_project/src/download_enigh.py" TO RUN THIS BLOCK ON TERMINAL 