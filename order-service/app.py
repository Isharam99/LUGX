import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)
DATABASE = 'orders.db'

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

@app.route('/orders', methods=['GET'])
def get_orders():
    """Retrieves a list of orders from the database."""
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return jsonify([dict(row) for row in orders])

# Initialize the database when the app starts
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)