DROP TABLE IF EXISTS games;

CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price REAL,
    release_date TEXT,
    description TEXT
);

INSERT INTO games (name, category, price, release_date, description) VALUES
('Cyberpunk 2077', 'RPG', 59.99, '2020-12-10', 'An open-world, action-adventure story set in Night City.'),
('The Witcher 3', 'RPG', 39.99, '2015-05-19', 'A story-driven, next-generation open world role-playing game.'),
('Red Dead Redemption 2', 'Action-Adventure', 49.99, '2018-10-26', 'A Western-themed action-adventure game set in an open world environment.');
