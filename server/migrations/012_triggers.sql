DELIMITER $$

-- Trigger 1: When a purchase order status changes to 'received', update product stock
CREATE TRIGGER update_stock_on_receive
AFTER UPDATE ON purchase_orders
FOR EACH ROW
BEGIN
    IF NEW.status = 'received' AND OLD.status != 'received' THEN
        UPDATE products p
        JOIN purchase_order_items poi ON p.id = poi.product_id
        SET p.quantity = p.quantity + poi.quantity_received
        WHERE poi.purchase_order_id = NEW.id;
    END IF;
END$$

-- Trigger 2: After any product quantity change, log the movement
CREATE TRIGGER log_stock_movement
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    IF OLD.quantity != NEW.quantity THEN
        INSERT INTO stock_movements (product_id, user_id, quantity_before, quantity_after, reason, changed_at)
        VALUES (NEW.id, NULL, OLD.quantity, NEW.quantity, 'Auto logged from trigger', NOW());
    END IF;
END$$

DELIMITER ;
