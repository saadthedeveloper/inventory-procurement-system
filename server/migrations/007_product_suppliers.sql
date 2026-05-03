CREATE TABLE product_suppliers(
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    supplier_id INT NOT NULL,
    unit_cost DECIMAL(10,2) NOT NULL,
    is_preferred BOOLEAN DEFAULT FALSE,
    UNIQUE KEY (product_id, supplier_id),
    FOREIGN KEY (product_id) REFERENCES products(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);