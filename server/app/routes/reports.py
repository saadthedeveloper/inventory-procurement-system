from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.db import get_connection

reports_bp = Blueprint("reports", __name__)

# ------------------------------------------------------------------
# GET /reports/stock-valuation - Query the stock_valuation view
# ------------------------------------------------------------------
@reports_bp.route("/stock-valuation", methods=["GET"])
@jwt_required()
def stock_valuation():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock_valuation ORDER BY category_name, name")
    valuation = cursor.fetchall()
    conn.close()
    return jsonify(valuation), 200

# ------------------------------------------------------------------
# GET /reports/movement-history - Query stock_movements with optional filters
# Query params: product_id (int), start_date (YYYY-MM-DD), end_date (YYYY-MM-DD)
# ------------------------------------------------------------------
@reports_bp.route("/movement-history", methods=["GET"])
@jwt_required()
def movement_history():
    product_id = request.args.get("product_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    query = """
        SELECT sm.id, sm.product_id, p.name as product_name,
               sm.user_id, u.name as user_name,
               sm.quantity_before, sm.quantity_after,
               sm.reason, sm.changed_at
        FROM stock_movements sm
        LEFT JOIN products p ON sm.product_id = p.id
        LEFT JOIN users u ON sm.user_id = u.id
        WHERE 1=1
    """
    params = []
    if product_id:
        query += " AND sm.product_id = %s"
        params.append(product_id)
    if start_date:
        query += " AND sm.changed_at >= %s"
        params.append(start_date)
    if end_date:
        query += " AND sm.changed_at <= %s"
        params.append(end_date + " 23:59:59")
    query += " ORDER BY sm.changed_at DESC"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    movements = cursor.fetchall()
    conn.close()
    return jsonify(movements), 200
