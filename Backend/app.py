from flask import Flask, jsonify, request
from auth.routes import auth_bp
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf
from config import Config, db  # Importar configuración y Firestore
import os

# Crear la función de creación de la aplicación Flask
def create_app():
    app = Flask(__name__)

    # Aplicar configuración desde Config
    app.config.from_object(Config)

    # Configurar CORS con las URLs del frontend
    CORS(app, resources={r"/*":{"origins": os.getenv("FRONTEND_URL")}}, supports_credentials=True)

    # Configurar CSRF
    #csrf = CSRFProtect(app) ESto sólo es para pruebas.

    # Registrar el blueprint de autenticación
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Endpoint para obtener el token CSRF
    @app.route('/get-csrf-token', methods=['GET'])
    def get_csrf_token():
        csrf_token = generate_csrf()
        return jsonify({'csrf_token': csrf_token}), 200

    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify({'message': 'pong'}), 200

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
    app.logger.error(f"Internal Server Error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
   app.logger.info("Configuración cargada:")
   app.logger.info(f"DEBUG: {app.config['DEBUG']}")
   app.logger.info(f"Entorno: {app.config['ENV']}")
   app.logger.info(f"Frontend URL: {os.getenv('FRONTEND_URL')}") 

    # Ejecutar la aplicación Flask en producción usando el puerto proporcionado por Render
   port = int(os.getenv("PORT", 5000))
   app.run(host="0.0.0.0", port=port, debug=app.config['DEBUG'])