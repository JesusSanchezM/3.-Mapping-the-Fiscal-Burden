# config/paths.py
from pathlib import Path

# __file__ es la ubicación de este script (config/paths.py)
# .parent.parent nos sube a la raíz (fiscal_incidence_project)
ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Crear carpetas si no existen
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)