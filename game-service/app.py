import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE = 'games.db'

def get_db_connection():
    """Connects to the specific database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the table if it doesn't exist."""
    conn = get_db_connection()
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# --- SEARCH for Games (New Endpoint) ---
@app.route('/games/search', methods=['GET'])
def search_games():
    """Searches for games based on query parameters."""
    category = request.args.get('category')
    max_price = request.args.get('max_price')
    query = "SELECT * FROM games WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if max_price:
        query += " AND price <= ?"
        params.append(float(max_price))
    conn = get_db_connection()
    games = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(row) for row in games])

# --- GET All Games ---
@app.route('/games', methods=['GET'])
def get_games():
    """Retrieves a list of all games from the database."""
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM games').fetchall()
    conn.close()
    return jsonify([dict(row) for row in games])

# --- GET a Single Game by ID ---
@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    """Retrieves a single game by its ID."""
    conn = get_db_connection()
    game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()
    conn.close()
    if game is None:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(dict(game))

# --- CREATE a New Game ---
@app.route('/games', methods=['POST'])
def create_game():
    """Creates a new game in the database."""
    new_game = request.get_json()
    if not new_game or 'name' not in new_game or 'price' not in new_game:
        return jsonify({'error': 'Missing required fields'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO games (name, category, price, release_date, description) VALUES (?, ?, ?, ?, ?)',
                 (new_game['name'], new_game.get('category'), new_game['price'], new_game.get('release_date'), new_game.get('description')))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': new_id, **new_game}), 201

# --- UPDATE an Existing Game ---
@app.route('/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    """Updates an existing game's details."""
    game_updates = request.get_json()
    conn = get_db_connection()
    conn.execute('UPDATE games SET name = ?, category = ?, price = ?, release_date = ?, description = ? WHERE id = ?',
                 (game_updates['name'], game_updates.get('category'), game_updates['price'], game_updates.get('release_date'), game_updates.get('description'), game_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 200

# --- DELETE a Game ---
@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    """Deletes a game from the database."""
    conn = get_db_connection()
    conn.execute('DELETE FROM games WHERE id = ?', (game_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 200

# This part will run only once when the app starts to set up the database
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
