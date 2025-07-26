DROP TABLE IF EXISTS games;

CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price REAL
);

INSERT INTO games (name, category, price) VALUES
('Cyberpunk 2077', 'RPG', 59.99),
('The Witcher 3', 'RPG', 39.99),
('Red Dead Redemption 2', 'Action-Adventure', 49.99);