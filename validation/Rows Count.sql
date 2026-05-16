SELECT 'roles' as table_name, COUNT(*) AS row_count FROM roles
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'units', COUNT(*) FROM units
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'suppliers', COUNT(*) FROM suppliers
UNION ALL
SELECT 'product_suppliers', COUNT(*) FROM product_suppliers
UNION ALL
SELECT 'purchase_orders', COUNT(*) FROM purchase_orders
UNION ALL
SELECT 'purchase_order_items', COUNT(*) FROM purchase_order_items
UNION ALL
SELECT 'stock_movements', COUNT(*) FROM stock_movements;