import requests
import zipfile
import sys
from pathlib import Path

# Añadir la raíz al path para poder importar config
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from config.paths import RAW_DIR

# URL base del INEGI para microdatos ENIGH Nueva Serie
BASE_URL = "https://www.inegi.org.mx/contenidos/programas/enigh/nc/{year}/microdatos/enigh{year}_ns_{module}_csv.zip"

YEARS = [2018, 2024]
# Módulos clave para análisis de incidencia fiscal (Ingresos y Gastos)
MODULES = ["ingresos", "gastoshogar", "concentradohogar", "poblacion"]

def download_and_extract(year, module):
    url = BASE_URL.format(year=year, module=module)
    zip_path = RAW_DIR / f"{module}_{year}.zip"
    final_csv_name = f"{module}_{year}.csv"

    if (RAW_DIR / final_csv_name).exists():
        print(f"⏭️  {final_csv_name} ya existe. Saltando...")
        return

    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"⚠️  No disponible: {module} {year}")
            return

        print(f"⬇️  Descargando {module} {year}...")
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.lower().endswith(".csv"):
                    # Extraer temporalmente
                    zip_ref.extract(file_name, RAW_DIR)
                    # Renombrar y mover a la raíz de raw/
                    (RAW_DIR / file_name).replace(RAW_DIR / final_csv_name)
                    print(f"   ✅ Guardado como: {final_csv_name}")

        zip_path.unlink() # Limpiar el zip
        
    except Exception as e:
        print(f"❌ Error en {module} {year}: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando descarga para Análisis de Incidencia Fiscal...\n")
    for year in YEARS:
        for module in MODULES:
            download_and_extract(year, module)
    print("\n✨ Proceso de descarga finalizado.")   



# WRITE "python3 fiscal_incidence_project/src/download_enigh.py" TO RUN THIS BLOCK ON TERMINAL 