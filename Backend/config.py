import os
import json
from firebase_admin import credentials, initialize_app, firestore
import firebase_admin
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración para la aplicación Flask."""
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret")
    WTF_CSRF_SECRET_KEY = False #os.getenv("CSRF_SECRET_KEY", "csrf_default_secret")
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"
    ENV = os.getenv("FLASK_ENV", "production")
    
    # URLs del frontend configurables
    FRONTEND_URL= os.getenv("FRONTEND_URL")

    # Determinar las credenciales de Firebase
    if ENV == 'production':
        # En producción, las credenciales de Firebase vienen desde las variables de entorno
        FIREBASE_CREDENTIALS = {
            "type": "service_account",
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
            "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
        }
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
    # Usamos las credenciales de Firebase dependiendo del entorno
    cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
    if not firebase_admin._apps:  # Verifica si Firebase ya está inicializado
        initialize_app(cred)
    return firestore.client()

# Instancia de Firestore
db = initialize_firebase()