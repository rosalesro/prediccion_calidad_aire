import requests
import pandas as pd
from config import IQAIR_API_KEY, IQAIR_API_URL, COLUMNAS_ESPERADAS

def obtener_datos_calidad_aire(lat, lon):
    try:
        response = requests.get(IQAIR_API_URL, params={
            "lat": lat,
            "lon": lon,
            "key": IQAIR_API_KEY
        })
        data = response.json()

        if data["status"] != "success":
            return None, "Error: " + data["data"].get("message", "Desconocido")

        pollution = data["data"]["current"]["pollution"]

        fila = {
            "PM2.5": pollution.get("pm2_5", None),
            "PM10": pollution.get("pm10", None),
            "NO": 0.0,
            "NO2": pollution.get("no2", None),
            "NOx": 0.0,
            "NH3": 0.0,
            "CO": pollution.get("co", None),
            "SO2": pollution.get("so2", None),
            "O3": pollution.get("o3", None)
        }

        df = pd.DataFrame([fila]).fillna(0.0)

        # Extras: ciudad, país y AQI real de IQAir
        info_extra = {
            "ciudad": data["data"].get("city", "Desconocida"),
            "pais": data["data"].get("country", "Desconocido"),
            "aqi_real": pollution.get("aqius", None)
        }

        return (df, info_extra), None

    except Exception as e:
        return None, f"Excepción al conectarse con la API: {e}"

