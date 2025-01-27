# Importación de dependencias
from flask import Flask
from auth.routes import auth_bp
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from config import Config, db  # Importar configuración y Firestore
import os

# Crear la función de creación de la aplicación Flask
def create_app():
    app = Flask(__name__)

    # Aplicar configuración desde Config
    app.config.from_object(Config)

    # Configurar CORS
    CORS(app)

    # Configurar CSRF
    csrf = CSRFProtect(app)

    # Registrar el blueprint de autenticación
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Inicializa cualquier otra extensión aquí, si es necesario

    return app

# Crear la instancia de la aplicación
app = create_app()

# Manejadores de errores
@app.errorhandler(404)
def page_not_found(e):
    return {'error': 'Page not found'}, 404

@app.errorhandler(500)
def internal_server_error(e):
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])