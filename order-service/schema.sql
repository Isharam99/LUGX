DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'Pending'
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    game_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (id)
);

-- Insert some sample data
INSERT INTO orders (id, customer_name, status) VALUES (1, 'John Doe', 'Shipped');
INSERT INTO order_items (order_id, game_name, quantity, price) VALUES
(1, 'Cyberpunk 2077', 1, 59.99),
(1, 'The Witcher 3', 1, 39.99);
