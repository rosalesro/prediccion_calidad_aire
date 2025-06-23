import os
from dotenv import load_dotenv
from app import app  # tu aplicación Flask en app.py

# Cargar variables de entorno desde .env antes de iniciar la app
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Aplicación para Gunicorn
application = app

if __name__ == '__main__':
    # Usa host/puerto definidos en el entorno o valores por defecto
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=(os.getenv('FLASK_ENV', 'production') == 'development')
    )
