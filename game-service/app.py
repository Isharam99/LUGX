import sqlite3
from flask import Flask, jsonify

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

@app.route('/games', methods=['GET'])
def get_games():
    """Retrieves a list of games from the database."""
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM games').fetchall()
    conn.close()
    # Convert rows to a list of dictionaries
    return jsonify([dict(row) for row in games])

# This part will run only once when the app starts
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)