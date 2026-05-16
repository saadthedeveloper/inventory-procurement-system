-- Check for NULLs in critical foreign key columns
SELECT 'products.category_id' AS column_name, COUNT(*) AS null_count FROM products WHERE category_id IS NULL
UNION ALL
SELECT 'products.unit_id', COUNT(*) FROM products WHERE unit_id IS NULL
UNION ALL
SELECT 'users.role_id', COUNT(*) FROM users WHERE role_id IS NULL
UNION ALL
SELECT 'purchase_orders.supplier_id', COUNT(*) FROM purchase_orders WHERE supplier_id IS NULL
UNION ALL
SELECT 'purchase_orders.created_by', COUNT(*) FROM purchase_orders WHERE created_by IS NULL
UNION ALL
SELECT 'purchase_order_items.purchase_order_id', COUNT(*) FROM purchase_order_items WHERE purchase_order_id IS NULL
UNION ALL
SELECT 'purchase_order_items.product_id', COUNT(*) FROM purchase_order_items WHERE product_id IS NULL
UNION ALL
SELECT 'stock_movements.product_id', COUNT(*) FROM stock_movements WHERE product_id IS NULL;