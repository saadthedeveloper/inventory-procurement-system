-- Products without a valid category
SELECT 'products missing category' AS `check`, COUNT(*) AS orphan_count
FROM products p LEFT JOIN categories c ON p.category_id = c.id
WHERE c.id IS NULL

UNION ALL

-- Products without a valid unit
SELECT 'products missing unit', COUNT(*)
FROM products p LEFT JOIN units u ON p.unit_id = u.id
WHERE u.id IS NULL

UNION ALL

-- Users without a valid role
SELECT 'users missing role', COUNT(*)
FROM users u LEFT JOIN roles r ON u.role_id = r.id
WHERE r.id IS NULL

UNION ALL

-- Purchase orders without a valid supplier
SELECT 'purchase_orders missing supplier', COUNT(*)
FROM purchase_orders po LEFT JOIN suppliers s ON po.supplier_id = s.id
WHERE s.id IS NULL

UNION ALL

-- Purchase orders without a valid creator (user)
SELECT 'purchase_orders missing created_by user', COUNT(*)
FROM purchase_orders po LEFT JOIN users u ON po.created_by = u.id
WHERE u.id IS NULL

UNION ALL

-- Purchase order items without a valid purchase order
SELECT 'po_items missing purchase_order', COUNT(*)
FROM purchase_order_items poi LEFT JOIN purchase_orders po ON poi.purchase_order_id = po.id
WHERE po.id IS NULL

UNION ALL

-- Purchase order items without a valid product
SELECT 'po_items missing product', COUNT(*)
FROM purchase_order_items poi LEFT JOIN products p ON poi.product_id = p.id
WHERE p.id IS NULL

UNION ALL

-- Stock movements without a valid product
SELECT 'stock_movements missing product', COUNT(*)
FROM stock_movements sm LEFT JOIN products p ON sm.product_id = p.id
WHERE p.id IS NULL

UNION ALL

-- Stock movements with user_id that does not exist (allowed to be NULL)
SELECT 'stock_movements invalid user_id', COUNT(*)
FROM stock_movements sm LEFT JOIN users u ON sm.user_id = u.id
WHERE sm.user_id IS NOT NULL AND u.id IS NULL;