from flask import Blueprint, request, jsonify
from config import db  # Importamos la referencia de Firestore desde config.py
from firebase_admin.auth import create_user as firebase_create_user, get_user_by_email as firebase_get_user_by_email, verify_id_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# Ruta para registro de usuarios (Alineada con el frontend)
@auth_bp.route("/registro", methods=["POST"])
def register():
    try:
        data = request.json

        # Validar que los campos obligatorios estén presentes
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        # Verificar si el usuario ya está registrado
        try:
            firebase_get_user_by_email(data["email"])
            return jsonify({"error": "El usuario ya está registrado"}), 409
        except Exception:
            # Si el usuario no existe, Firebase lanzará un error (esto es esperado)
            pass

        # Crear usuario en Firebase Authentication
        hashed_password = generate_password_hash(data["password"])
        firebase_user = firebase_create_user(
            email=data["email"],
            password=data["password"],
        )

        # Guardar información adicional del usuario en Firestore
        user_data = {
            "user":data["user"],
            "email": data["email"],
              "password": hashed_password
              }
        db.collection("users").document(firebase_user.uid).set(user_data)

        return jsonify({"message": "Usuario registrado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": "Error al registrar usuario", "details": str(e)}), 500


# Ruta para inicio de sesión (Alineada con el frontend)
@auth_bp.route("/inicio-sesion", methods=["POST"])
def login():
    try:
        data = request.json

        # Validar que los campos obligatorios estén presentes
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        # Buscar el usuario en Firebase Authentication
        user_ref = db.collection("users").where("email", "==", data["email"]).get()
        if not user_ref:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        # Obtener los datos del usuario
        user_data = user_ref[0].to_dict()
        if not check_password_hash(user_data["password"], data["password"]):
            return jsonify({"error": "Credenciales incorrectas"}), 401

        # Generar un token de autenticación usando Firebase (opcional)
        return jsonify({"message": "Inicio de sesión exitoso"}), 200

    except Exception as e:
        return jsonify({"error": "Error durante el inicio de sesión", "details": str(e)}), 500


# Ruta protegida para el dashboard
@auth_bp.route("/dashboard", methods=["GET"])
def dashboard():
    try:
        auth_header = request.headers.get("Authorization")

        # Validar que el token esté presente y en el formato correcto
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "No se proporcionó un token válido"}), 401

        token = auth_header.split(" ")[1]

        # Verificar el token de Firebase
        decoded_token = verify_id_token(token)
        user_email = decoded_token.get("email")

        if user_email:
            return jsonify({"email": user_email, "info": "Bienvenido al dashboard"}), 200

        return jsonify({"error": "Token inválido"}), 401

    except Exception as e:
        return jsonify({"error": "Token inválido o expirado", "details": str(e)}), 401
