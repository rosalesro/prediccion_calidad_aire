import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELO_PATH = os.path.join(BASE_DIR, "entrenamiento", "modelos_guardados", "modelo_entrenado.pkl")

# Configuración de API
IQAIR_API_KEY = os.getenv("IQAIR_API_KEY")  # ✅ CORREGIDO
IQAIR_API_URL = "http://api.airvisual.com/v2/nearest_city"

# Columnas esperadas por el modelo
COLUMNAS_ESPERADAS = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3']






