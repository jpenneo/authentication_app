# Importación de dependencias
from flask import Flask, jsonify
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
    CORS(app, resources={r"/*": {"origins": "*"}})

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
    """Manejador de error para rutas no encontradas."""
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Manejador de error para errores internos del servidor."""
    # Registrar el error en los logs para análisis
    app.logger.error(f"Internal Server Error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Verificar que la configuración se cargó correctamente
    app.logger.info("Configuración cargada:")
    app.logger.info(f"DEBUG: {app.config['DEBUG']}")
    app.logger.info(f"Entorno: {app.config['ENV']}")

    # Ejecutar la aplicación Flask
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=app.config['DEBUG'])