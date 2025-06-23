import joblib
import numpy as np
import pandas as pd
from config import MODELO_PATH, COLUMNAS_ESPERADAS

class PredictorCalidadAire:
    def __init__(self):
        self.modelo = joblib.load(MODELO_PATH)

    def predecir(self, datos_df: pd.DataFrame):
        # Validación: columnas necesarias
        for col in COLUMNAS_ESPERADAS:
            if col not in datos_df.columns:
                raise ValueError(f"Falta la columna: {col}")

        # Filtrar solo las columnas requeridas
        X = datos_df[COLUMNAS_ESPERADAS]

        # Realiza predicción
        predicciones = self.modelo.predict(X)
        return predicciones

    def predecir_promedio(self, datos_df: pd.DataFrame):
        predicciones = self.predecir(datos_df)
        return round(float(np.mean(predicciones)), 2)

