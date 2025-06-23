import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import r2_score, mean_squared_error
from math import sqrt

# Ruta del archivo CSV
csv_path = os.path.join("entrenamiento", "data", "city_day_dos.csv")

# Cargamos el dataset
df = pd.read_csv(csv_path)

# Eliminamos columnas no deseadas
columnas_a_eliminar = ['City', 'Date', 'Benzene', 'Toluene', 'Xylene', 'AQI_Bucket']
df = df.drop(columns=columnas_a_eliminar, errors='ignore')

# Eliminamos filas con valores nulos
df = df.dropna()

# Separación de variables predictoras y objetivo
X = df.drop(columns=["AQI"])
y = df["AQI"]

# División en datos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Pipeline de preprocesamiento y modelo
pipeline = Pipeline(steps=[
    ('preprocesamiento', ColumnTransformer(transformers=[
        ('escala', Pipeline([
            ('imputacion', SimpleImputer(strategy='mean')),
            ('escalado', StandardScaler())
        ]), X.columns)
    ])),
    ('modelo', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Entrenamos el modelo
pipeline.fit(X_train, y_train)

# Evaluación
y_pred = pipeline.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = sqrt(mean_squared_error(y_test, y_pred))

# Guardamos el modelo entrenado
ruta_guardado = os.path.join("entrenamiento", "modelos_guardados", "modelo_entrenado.pkl")
joblib.dump(pipeline, ruta_guardado)

# Resultados
print(f"\n✅ Entrenamiento completado y modelo guardado en: {ruta_guardado}")
print(f"📊 R² Score (precisión del modelo): {r2:.4f}")
print(f"📉 RMSE (raíz del error cuadrático medio): {rmse:.2f}")





