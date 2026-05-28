from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.db import get_connection

suppliers_bp = Blueprint("suppliers", __name__)

def is_admin():
    claims = get_jwt()
    return claims.get("role_id") == 1

@suppliers_bp.route("", methods=["GET"])
@jwt_required()
def get_suppliers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, contact_person, email, phone, payment_terms, is_active, created_at FROM suppliers ORDER BY name")
    suppliers = cursor.fetchall()
    conn.close()
    return jsonify(suppliers), 200

@suppliers_bp.route("/<int:supplier_id>", methods=["GET"])
@jwt_required()
def get_supplier(supplier_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, contact_person, email, phone, payment_terms, is_active, created_at FROM suppliers WHERE id = %s", (supplier_id,))
    supplier = cursor.fetchone()
    conn.close()
    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404
    return jsonify(supplier), 200

@suppliers_bp.route("", methods=["POST"])
@jwt_required()
def create_supplier():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403
    data = request.get_json()
    required = ["name", "contact_person", "email", "phone"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO suppliers (name, contact_person, email, phone, payment_terms, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, (data["name"], data["contact_person"], data["email"], data["phone"],
              data.get("payment_terms"), data.get("is_active", True)))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({"id": new_id, "message": "Supplier created"}), 201
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

@suppliers_bp.route("/<int:supplier_id>", methods=["PUT"])
@jwt_required()
def update_supplier(supplier_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403
    data = request.get_json()
    allowed = ["name", "contact_person", "email", "phone", "payment_terms", "is_active"]
    fields = []
    values = []
    for key in allowed:
        if key in data:
            fields.append(f"{key} = %s")
            values.append(data[key])
    if not fields:
        return jsonify({"error": "No fields to update"}), 400
    values.append(supplier_id)
    query = f"UPDATE suppliers SET {', '.join(fields)} WHERE id = %s"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({"error": "Supplier not found"}), 404
    return jsonify({"message": "Supplier updated"}), 200

@suppliers_bp.route("/<int:supplier_id>", methods=["DELETE"])
@jwt_required()
def delete_supplier(supplier_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE suppliers SET is_active = FALSE WHERE id = %s", (supplier_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        if affected == 0:
            return jsonify({"error": "Supplier not found"}), 404
        return jsonify({"message": "Supplier soft deleted"}), 200
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

