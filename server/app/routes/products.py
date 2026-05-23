from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.db import get_connection

products_bp = Blueprint("products", __name__)

# Helper to check if current user is admin using claims
def is_admin():
    claims = get_jwt()
    return claims.get("role_id") == 1

# ------------------------------------------------------------------
# GET /products - List all active products (Staff, Manager, Admin)
# ------------------------------------------------------------------
@products_bp.route("/", methods=["GET"])
@jwt_required()
def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.sku, p.quantity, p.reorder_level, p.unit_price,
               p.is_active, p.created_at,
               c.name AS category_name, u.name AS unit_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN units u ON p.unit_id = u.id
        WHERE p.is_active = TRUE
        ORDER BY p.id
    """)
    products = cursor.fetchall()
    conn.close()
    return jsonify(products), 200

# ------------------------------------------------------------------
# GET /products/<id> - Get a single product
# ------------------------------------------------------------------
@products_bp.route("/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.sku, p.category_id, p.unit_id,
               p.quantity, p.reorder_level, p.unit_price, p.is_active, p.created_at,
               c.name AS category_name, u.name AS unit_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN units u ON p.unit_id = u.id
        WHERE p.id = %s
    """, (product_id,))
    product = cursor.fetchone()
    conn.close()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

# ------------------------------------------------------------------
# POST /products - Create a new product (Admin only)
# ------------------------------------------------------------------
@products_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    required = ["name", "category_id", "unit_id", "reorder_level", "unit_price"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    name = data["name"]
    sku = data.get("sku")
    category_id = data["category_id"]
    unit_id = data["unit_id"]
    quantity = data.get("quantity", 0)
    reorder_level = data["reorder_level"]
    unit_price = data["unit_price"]
    is_active = data.get("is_active", True)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO products (name, sku, category_id, unit_id, quantity,
                                  reorder_level, unit_price, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (name, sku, category_id, unit_id, quantity, reorder_level, unit_price, is_active))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({"id": new_id, "message": "Product created"}), 201
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------------
# PUT /products/<id> - Update a product (Admin only)
# ------------------------------------------------------------------
@products_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    fields = []
    values = []
    allowed = ["name", "sku", "category_id", "unit_id", "quantity",
               "reorder_level", "unit_price", "is_active"]
    for key in allowed:
        if key in data:
            fields.append(f"{key} = %s")
            values.append(data[key])
    if not fields:
        return jsonify({"error": "No fields to update"}), 400

    values.append(product_id)
    query = f"UPDATE products SET {', '.join(fields)} WHERE id = %s"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"message": "Product updated"}), 200

# ------------------------------------------------------------------
# DELETE /products/<id> - Soft delete (Admin only)
# ------------------------------------------------------------------
@products_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET is_active = FALSE WHERE id = %s", (product_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"message": "Product soft deleted"}), 200

# ------------------------------------------------------------------
# GET /products/low-stock - Query low_stock_alerts view
# ------------------------------------------------------------------
@products_bp.route("/low-stock", methods=["GET"])
@jwt_required()
def low_stock():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM low_stock_alerts ORDER BY quantity ASC")
    alerts = cursor.fetchall()
    conn.close()
    return jsonify(alerts), 200
