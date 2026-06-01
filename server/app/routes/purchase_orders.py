from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.db import get_connection

purchase_orders_bp = Blueprint("purchase_orders", __name__)

def is_admin():
    claims = get_jwt()
    return claims.get("role_id") == 1

def is_manager():
    claims = get_jwt()
    return claims.get("role_id") == 2  # role_id 2 = Manager

def is_staff():
    claims = get_jwt()
    return claims.get("role_id") in [1,2,3]  # any logged in user

# ------------------------------------------------------------------
# GET /purchase-orders - List all purchase orders
# ------------------------------------------------------------------
@purchase_orders_bp.route("", methods=["GET"])
@jwt_required()
def get_purchase_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT po.id, po.supplier_id, s.name as supplier_name,
               po.created_by, u1.name as created_by_name,
               po.approved_by, u2.name as approved_by_name,
               po.approved_at, po.status, po.notes,
               po.created_at, po.updated_at
        FROM purchase_orders po
        LEFT JOIN suppliers s ON po.supplier_id = s.id
        LEFT JOIN users u1 ON po.created_by = u1.id
        LEFT JOIN users u2 ON po.approved_by = u2.id
        ORDER BY po.created_at DESC
    """)
    orders = cursor.fetchall()
    conn.close()
    return jsonify(orders), 200

# ------------------------------------------------------------------
# Cancel PO (Admin or creator)
# ------------------------------------------------------------------
@purchase_orders_bp.route("/<int:po_id>/cancel", methods=["PUT"])
@jwt_required()
def cancel_order(po_id):
    claims = get_jwt()
    role_id = claims.get("role_id")
    user_id = int(get_jwt_identity())
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, created_by FROM purchase_orders WHERE id = %s", (po_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Order not found"}), 404
    if row["status"] not in ["pending", "approved"]:
        conn.close()
        return jsonify({"error": "Only pending orders can be cancelled"}), 400
    if not (role_id == 1 or row["created_by"] == user_id):
        conn.close()
        return jsonify({"error": "Not authorized to cancel this order"}), 403
    cursor.execute("UPDATE purchase_orders SET status = 'cancelled', updated_at = NOW() WHERE id = %s", (po_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order cancelled"}), 200

# ------------------------------------------------------------------
# GET /purchase-orders/<id> - Get one purchase order with its items
# ------------------------------------------------------------------
@purchase_orders_bp.route("/<int:po_id>", methods=["GET"])
@jwt_required()
def get_purchase_order(po_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT po.id, po.supplier_id, s.name as supplier_name,
               po.created_by, u1.name as created_by_name,
               po.approved_by, u2.name as approved_by_name,
               po.approved_at, po.status, po.notes,
               po.created_at, po.updated_at
        FROM purchase_orders po
        LEFT JOIN suppliers s ON po.supplier_id = s.id
        LEFT JOIN users u1 ON po.created_by = u1.id
        LEFT JOIN users u2 ON po.approved_by = u2.id
        WHERE po.id = %s
    """, (po_id,))
    order = cursor.fetchone()
    if not order:
        conn.close()
        return jsonify({"error": "Purchase order not found"}), 404

    # get items
    cursor.execute("""
        SELECT poi.id, poi.product_id, p.name as product_name,
               poi.quantity_ordered, poi.quantity_received, poi.unit_cost
        FROM purchase_order_items poi
        JOIN products p ON poi.product_id = p.id
        WHERE poi.purchase_order_id = %s
    """, (po_id,))
    items = cursor.fetchall()
    conn.close()
    order["items"] = items
    return jsonify(order), 200

# ------------------------------------------------------------------
# POST /purchase-orders - Create a new purchase order (Manager or Admin)
# ------------------------------------------------------------------
@purchase_orders_bp.route("", methods=["POST"])
@jwt_required()
def create_purchase_order():
    # Only Manager or Admin can create
    claims = get_jwt()
    role_id = claims.get("role_id")
    if role_id not in [1,2]:
        return jsonify({"error": "Manager or Admin access required"}), 403

    data = request.get_json()
    supplier_id = data.get("supplier_id")
    notes = data.get("notes")
    items = data.get("items", [])  # list of {product_id, quantity_ordered, unit_cost}

    if not supplier_id or not items:
        return jsonify({"error": "supplier_id and items are required"}), 400

    user_id = int(get_jwt_identity())  # string id from token

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Insert purchase order
        cursor.execute("""
            INSERT INTO purchase_orders (supplier_id, created_by, status, notes, created_at, updated_at)
            VALUES (%s, %s, 'pending', %s, NOW(), NOW())
        """, (supplier_id, user_id, notes))
        po_id = cursor.lastrowid

        # Insert items
        for item in items:
            product_id = item.get("product_id")
            qty_ordered = item.get("quantity_ordered")
            unit_cost = item.get("unit_cost")
            if not product_id or not qty_ordered or not unit_cost:
                conn.rollback()
                conn.close()
                return jsonify({"error": "Each item must have product_id, quantity_ordered, unit_cost"}), 400
            cursor.execute("""
                INSERT INTO purchase_order_items (purchase_order_id, product_id, quantity_ordered, quantity_received, unit_cost)
                VALUES (%s, %s, %s, 0, %s)
            """, (po_id, product_id, qty_ordered, unit_cost))

        conn.commit()
        conn.close()
        return jsonify({"id": po_id, "message": "Purchase order created"}), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------------
# PUT /purchase-orders/<id>/approve - Approve order (Admin only)
# ------------------------------------------------------------------
@purchase_orders_bp.route("/<int:po_id>/approve", methods=["PUT"])
@jwt_required()
def approve_order(po_id):
    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403

    user_id = int(get_jwt_identity())
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE purchase_orders
        SET status = 'approved', approved_by = %s, approved_at = NOW(), updated_at = NOW()
        WHERE id = %s AND status = 'pending'
    """, (user_id, po_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({"error": "Order not found or not in pending status"}), 404
    return jsonify({"message": "Order approved"}), 200

# ------------------------------------------------------------------
# PUT /purchase-orders/<id>/receive - Mark order as received (Staff/Manager/Admin)
# Optionally can specify received quantities per item
# ------------------------------------------------------------------
@purchase_orders_bp.route("/<int:po_id>/receive", methods=["PUT"])
@jwt_required()
def receive_order(po_id):
    # Any authenticated user can mark received (staff, manager, admin)
    data = request.get_json()
    items_received = data.get("items", [])  # list of {product_id, quantity_received}

    conn = get_connection()
    cursor = conn.cursor()

    # First, update the received quantities in purchase_order_items
    try:
        for item in items_received:
            product_id = item.get("product_id")
            qty_received = item.get("quantity_received")
            cursor.execute("""
                UPDATE purchase_order_items
                SET quantity_received = %s
                WHERE purchase_order_id = %s AND product_id = %s
            """, (qty_received, po_id, product_id))

        # Then update the order status to 'received'
        cursor.execute("""
            UPDATE purchase_orders
            SET status = 'received', updated_at = NOW()
            WHERE id = %s AND status = 'approved'
        """, (po_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        if affected == 0:
            return jsonify({"error": "Order not found or not in approved status"}), 404
        # The database trigger will automatically update product quantities
        return jsonify({"message": "Order marked as received. Stock updated by trigger."}), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": str(e)}), 500
