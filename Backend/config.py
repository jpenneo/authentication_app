import os
import json
from firebase_admin import credentials, initialize_app, firestore
import firebase_admin 

class Config:
    """Configuración para la aplicación Flask."""
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret")
    WTF_CSRF_SECRET_KEY = os.getenv("CSRF_SECRET_KEY", "csrf_default_secret")
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"
    ENV = os.getenv("FLASK_ENV", "development")

    # Determinar las credenciales de Firebase
    if os.getenv('FLASK_ENV') == 'production':
        # En producción, las credenciales de Firebase vienen desde la variable de entorno
        FIREBASE_CREDENTIALS = json.loads(os.getenv('FIREBASE_CREDENTIALS'))
    else:
        # En desarrollo, se usa el archivo local serviceAccountKey.json
        FIREBASE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'config', 'serviceAccountKey.json')
        try:
            with open(FIREBASE_CREDENTIALS_PATH) as f:
                FIREBASE_CREDENTIALS = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo de credenciales no se encuentra en la ruta: {FIREBASE_CREDENTIALS_PATH}")


# Inicialización de Firebase
def initialize_firebase():
    """Inicializa Firebase con las credenciales cargadas."""
    cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS_PATH)
    if not firebase_admin._apps:  # Verifica si Firebase ya está inicializado
        initialize_app(cred)
    return firestore.client()

# Instancia de Firestore
db = initialize_firebase()