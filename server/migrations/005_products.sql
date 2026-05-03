CREATE TABLE products(
    id INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE,
    category_id INT NOT NULL,
    unit_id INT NOT NULL,
    quantity INT DEFAULT 0,
    reorder_level INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (unit_id) REFERENCES units(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);