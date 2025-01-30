from flask import Blueprint, request, jsonify, redirect, url_for
# Importar Firestore desde config.py
from config import db,Config  
from firebase_admin.auth import (
    create_user as firebase_create_user,
    get_user_by_email as firebase_get_user_by_email,
    verify_id_token,
)
from werkzeug.security import generate_password_hash, check_password_hash
import traceback
import jwt

auth_bp = Blueprint("auth", __name__)


# Ruta raíz "/" que redirige a "/inicio-sesion"
@auth_bp.route("/", methods=["GET"])
def root():
    """
    Redirige la ruta raíz (/) a /inicio-sesion.
    """
    return redirect(url_for("auth.login_page"))


# Ruta para la página de inicio de sesión (GET)
@auth_bp.route("/inicio-sesion", methods=["GET"])
def login_page():
    """
    Página de inicio de sesión: apunta al documento UserLogin.vue en el frontend.
    """
    return jsonify({"message": "Esta ruta apunta al documento UserLogin.vue en el frontend"})


# Ruta para procesar el inicio de sesión
@auth_bp.route("/inicio-sesion", methods=["POST"])
def login():
    """
    Procesa el inicio de sesión con validación.
    """
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Correo y contraseña son obligatorios"}), 400

        # Buscar el usuario en Firestore
        users_ref = db.collection("users")
        query = users_ref.where("email", "==", email).limit(1)
        user_docs = query.stream()
        user_doc = next(user_docs, None)  # Obtener el primer documento encontrado

        if not user_doc:
            return jsonify({"error": "Usuario no encontrado"}), 404

        user_data = user_doc.to_dict()

        # Verificar la contraseña
        if not check_password_hash(user_data["password"], password):
            return jsonify({"error": "Contraseña incorrecta"}), 401

        # Simular un token de sesión para fines de prueba (deberías usar JWT o sesiones reales)
        token = "fake-session-token"

        return jsonify(
            {"message": "Inicio de sesión exitoso", "token": token, "user": user_data["user"], "email": user_data["email"]}
        ), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Error al iniciar sesión"}), 500


# Ruta para la página de registro
@auth_bp.route("/registro", methods=["GET"])
def register_page():
    """
    Página de registro: apunta al documento UserRegister.vue en el frontend.
    """
    return jsonify({"message": "Esta ruta apunta al documento UserRegister.vue en el frontend"})


# Ruta para procesar el registro
@auth_bp.route("/registro", methods=["POST"])
def register():
    """
    Procesa el registro de usuarios con validación de contraseña.
    """
    try:
        data = request.json
        user = data.get("user")
        email = data.get("email")
        password = data.get("password")

        # Validar que los campos obligatorios estén presentes
        if not user or not email or not password:
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # Validar la contraseña
        if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password) or not any(char in "@$!%*?&" for char in password):
            return jsonify(
                {
                    "error": "La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial (@$!%*?&)"
                }
            ), 400

        # Verificar si el usuario ya está registrado
        try:
            firebase_get_user_by_email(data["email"])
            return jsonify({"error": "El usuario ya está registrado"}), 409
        except Exception:
            pass  # Si no existe el usuario, Firebase lanza un error

        # Crear usuario en Firebase Authentication
        hashed_password = generate_password_hash(data["password"])

        firebase_user = firebase_create_user(email=data["email"], password=data["password"])

        # Guardar información adicional del usuario en Firestore
        user_data = {
            "user": user,
            "email": email,
            "password": hashed_password,
        }
        db.collection("users").document(firebase_user.uid).set(user_data)

        return jsonify({"message": "Usuario registrado exitosamente"}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Error al registrar usuario"}), 500


# Ruta para la página del dashboard
@auth_bp.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Muestra el dashboard con los datos de Firestore (contraseña con asteriscos).
    Solo accesible para usuarios autenticados.
    """
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "No se proporcionó un token válido"}), 401

        token = auth_header.split(" ")[1]

        # Verificar el token de Firebase
        try:
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "El token ha expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        user_email = decoded_token.get("email")

        # Obtener los datos del usuario desde Firestore
        users_ref = db.collection('users')
        user_docs = users_ref.where('email', '==', user_email).stream()
        users = []
        for user_doc in user_docs:
            user_data = user_doc.to_dict()
            users.append({
                'user': user_data.get('user'),
                'email': user_data.get('email'),
                'password': '*' * len(user_data.get('password', '')),  # Contraseña enmascarada
            })

        return jsonify({"users": users}), 200

    except Exception as e:
        return jsonify({"error": "Token inválido o expirado", "details": str(e)}), 401
    
