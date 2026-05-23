from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.db import get_connection

units_bp = Blueprint("units", __name__)

def is_admin():
    claims = get_jwt()
    return claims.get("role_id") == 1

@units_bp.route("/", methods=["GET"])
@jwt_required()
def get_units():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM units ORDER BY name")
    units = cursor.fetchall()
    conn.close()
    return jsonify(units), 200

@units_bp.route("/<int:unit_id>", methods=["GET"])
@jwt_required()
def get_unit(unit_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM units WHERE id = %s", (unit_id,))
    unit = cursor.fetchone()
    conn.close()
    if not unit:
        return jsonify({"error": "Unit not found"}), 404
    return jsonify(unit), 200

@units_bp.route("/", methods=["POST"])
@jwt_required()
def create_unit():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO units (name) VALUES (%s)", (name,))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({"id": new_id, "name": name, "message": "Unit created"}), 201
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

@units_bp.route("/<int:unit_id>", methods=["PUT"])
@jwt_required()
def update_unit(unit_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE units SET name = %s WHERE id = %s", (name, unit_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({"error": "Unit not found"}), 404
    return jsonify({"message": "Unit updated"}), 200

@units_bp.route("/<int:unit_id>", methods=["DELETE"])
@jwt_required()
def delete_unit(unit_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM units WHERE id = %s", (unit_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        if affected == 0:
            return jsonify({"error": "Unit not found"}), 404
        return jsonify({"message": "Unit deleted"}), 200
    except Exception as e:
        conn.close()
        return jsonify({"error": f"Cannot delete unit: {str(e)}"}), 409
