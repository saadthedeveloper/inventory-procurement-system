from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
import bcrypt
from app.db import get_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password, role_id FROM users WHERE email = %s AND is_active = TRUE", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Check password (bcrypt)
    stored_password = user["password"]
    if isinstance(stored_password, str):
        stored_password = stored_password.encode("utf-8")

    if not bcrypt.checkpw(password.encode("utf-8"), stored_password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token with string identity (user id) and additional claims
    additional_claims = {
        "name": user["name"],
        "role_id": user["role_id"]
    }
    access_token = create_access_token(identity=str(user["id"]), additional_claims=additional_claims)

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role_id": user["role_id"]
        }
    }), 200
