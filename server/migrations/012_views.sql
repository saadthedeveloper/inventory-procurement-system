CREATE OR REPLACE VIEW low_stock_alerts AS
SELECT 
    p.id,
    p.name,
    p.quantity,
    p.reorder_level,
    c.name AS category_name
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.quantity < p.reorder_level;

CREATE OR REPLACE VIEW stock_valuation AS
SELECT 
    p.id,
    p.name,
    p.quantity,
    p.unit_price,
    (p.quantity * p.unit_price) AS total_value,
    c.name AS category_name
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.is_active = TRUE;