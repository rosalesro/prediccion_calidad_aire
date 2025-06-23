from flask import Flask, render_template, request, jsonify
from core.predictor import PredictorCalidadAire
from services.iqair_api import obtener_datos_calidad_aire
import pandas as pd

app = Flask(__name__)
modelo = PredictorCalidadAire()  # Carga y prepara el modelo una sola vez

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resultado", methods=["POST"])
def resultado():
    try:
        archivo = request.files["archivo"]
        if archivo.filename == "":
            return "No se seleccionó ningún archivo"

        df = pd.read_csv(archivo)

        # Usar solo primera fila para mostrar contaminantes
        fila = df.iloc[0].to_dict()
        contaminantes = {
            k: round(float(v), 2)
            for k, v in fila.items()
            if k in modelo.modelo.feature_names_in_
        }

        resultado = modelo.predecir_promedio(df)
        return render_template("resultado.html", resultado=resultado, contaminantes=contaminantes)

    except Exception as e:
        return f"Error al procesar archivo: {e}"

@app.route("/predecir_desde_mapa", methods=["POST"])
def predecir_desde_mapa():
    try:
        datos = request.get_json()
        lat = datos.get("lat")
        lon = datos.get("lon")

        if lat is None or lon is None:
            return jsonify({"error": "Latitud o longitud no proporcionadas"}), 400

        (df, info_extra), error = obtener_datos_calidad_aire(lat, lon)
        if error:
            return jsonify({"error": error}), 500

        fila = df.iloc[0].to_dict()
        contaminantes = {k: round(float(v), 2) for k, v in fila.items()}

        resultado = modelo.predecir_promedio(df)
        return jsonify({
            "resultado": resultado,
            "contaminantes": contaminantes,
            "ciudad": info_extra["ciudad"],
            "pais": info_extra["pais"],
            "aqi_real": info_extra["aqi_real"]
        })

    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)





















