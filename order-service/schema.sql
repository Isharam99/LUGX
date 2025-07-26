DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    total_price REAL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO orders (customer_name, total_price) VALUES
('John Doe', 99.98),
('Jane Smith', 59.99);