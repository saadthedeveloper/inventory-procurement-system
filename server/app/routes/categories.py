from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.db import get_connection

categories_bp = Blueprint("categories", __name__)

def is_admin():
    claims = get_jwt()
    return claims.get("role_id") == 1

# ------------------------------------------------------------------
# GET /categories - List all categories (any authenticated user)
# ------------------------------------------------------------------
@categories_bp.route("", methods=["GET"])
@jwt_required()
def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories ORDER BY name")
    categories = cursor.fetchall()
    conn.close()
    return jsonify(categories), 200

# ------------------------------------------------------------------
# GET /categories/<id> - Get a single category
# ------------------------------------------------------------------
@categories_bp.route("/<int:category_id>", methods=["GET"])
@jwt_required()
def get_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories WHERE id = %s", (category_id,))
    category = cursor.fetchone()
    conn.close()
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category), 200

# ------------------------------------------------------------------
# POST /categories - Create a new category (Admin only)
# ------------------------------------------------------------------
@categories_bp.route("", methods=["POST"])
@jwt_required()
def create_category():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({"id": new_id, "name": name, "message": "Category created"}), 201
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------------
# PUT /categories/<id> - Update a category (Admin only)
# ------------------------------------------------------------------
@categories_bp.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category(category_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE categories SET name = %s WHERE id = %s", (name, category_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({"message": "Category updated"}), 200

# ------------------------------------------------------------------
# DELETE /categories/<id> - Delete a category (Admin only)
# ------------------------------------------------------------------
@categories_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        if affected == 0:
            return jsonify({"error": "Category not found"}), 404
        return jsonify({"message": "Category deleted"}), 200
    except Exception as e:
        conn.close()
        # This will catch foreign key constraint errors (e.g., category used in products)
        return jsonify({"error": f"Cannot delete category: {str(e)}"}), 409

