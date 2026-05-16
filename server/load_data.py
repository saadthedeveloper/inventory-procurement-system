import csv
import pymysql
from app.config import Config

def clear_tables(cursor, tables):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table, _, _ in tables:
        cursor.execute(f"TRUNCATE TABLE {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    print("All tables cleared.")

def load_csv(table_name, csv_path, columns, cursor):
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            converted_row = [None if val == '' else val for val in row]
            placeholders = ','.join(['%s'] * len(converted_row))
            sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
            cursor.execute(sql, converted_row)
    print(f"Loaded {table_name}")

def main():
    conn = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )
    cursor = conn.cursor()

    tables = [
        ('roles', 'csv_data/roles.csv', ['id', 'name']),
        ('users', 'csv_data/users.csv', ['id', 'name', 'email', 'password', 'role_id', 'is_active', 'created_at']),
        ('categories', 'csv_data/categories.csv', ['id', 'name']),
        ('units', 'csv_data/units.csv', ['id', 'name']),
        ('products', 'csv_data/products.csv', ['id', 'name', 'sku', 'category_id', 'unit_id', 'quantity', 'reorder_level', 'unit_price', 'is_active', 'created_at']),
        ('suppliers', 'csv_data/suppliers.csv', ['id', 'name', 'contact_person', 'email', 'phone', 'payment_terms', 'is_active', 'created_at']),
        ('product_suppliers', 'csv_data/product_suppliers.csv', ['id', 'product_id', 'supplier_id', 'unit_cost', 'is_preferred']),
        ('purchase_orders', 'csv_data/purchase_orders.csv', ['id', 'supplier_id', 'created_by', 'approved_by', 'approved_at', 'status', 'notes', 'created_at', 'updated_at']),
        ('purchase_order_items', 'csv_data/purchase_order_items.csv', ['id', 'purchase_order_id', 'product_id', 'quantity_ordered', 'quantity_received', 'unit_cost']),
        ('stock_movements', 'csv_data/stock_movements.csv', ['id', 'product_id', 'user_id', 'quantity_before', 'quantity_after', 'reason', 'changed_at'])
    ]

    clear_tables(cursor, tables)
    for table, path, cols in tables:
        load_csv(table, path, cols, cursor)

    conn.commit()
    conn.close()
    print("All data loaded successfully.")

if __name__ == "__main__":
    main()
