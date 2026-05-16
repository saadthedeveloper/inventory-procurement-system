-- Indexes on foreign key columns (already auto-indexed by InnoDB, but explicit is fine)
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_unit_id ON products(unit_id);
CREATE INDEX idx_product_suppliers_product_id ON product_suppliers(product_id);
CREATE INDEX idx_product_suppliers_supplier_id ON product_suppliers(supplier_id);
CREATE INDEX idx_purchase_orders_supplier_id ON purchase_orders(supplier_id);
CREATE INDEX idx_purchase_orders_created_by ON purchase_orders(created_by);
CREATE INDEX idx_purchase_orders_approved_by ON purchase_orders(approved_by);
CREATE INDEX idx_purchase_order_items_purchase_order_id ON purchase_order_items(purchase_order_id);
CREATE INDEX idx_purchase_order_items_product_id ON purchase_order_items(product_id);
CREATE INDEX idx_stock_movements_product_id ON stock_movements(product_id);
CREATE INDEX idx_stock_movements_user_id ON stock_movements(user_id);

-- Additional indexes on columns frequently used in WHERE, ORDER BY, or JOIN
CREATE INDEX idx_purchase_orders_status ON purchase_orders(status);
CREATE INDEX idx_stock_movements_changed_at ON stock_movements(changed_at);
CREATE INDEX idx_products_sku ON products(sku);  -- if you search by SKU often
