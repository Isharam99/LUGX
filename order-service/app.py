import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE = 'orders.db'

def get_db_connection():
    """Connects to the specific database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the tables if it doesn't exist."""
    conn = get_db_connection()
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


# --- GET All Orders (New Endpoint) ---
@app.route('/orders', methods=['GET'])
def get_all_orders():
    """Retrieves a list of all orders."""
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return jsonify([dict(row) for row in orders])


# --- GET a Single Order with its Items (New Endpoint) ---
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Retrieves a single order and its line items."""
    conn = get_db_connection()
    # Get the main order details
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    if order is None:
        conn.close()
        return jsonify({'error': 'Order not found'}), 404
    
    # Get the line items for that order
    items = conn.execute('SELECT * FROM order_items WHERE order_id = ?', (order_id,)).fetchall()
    conn.close()
    
    # Combine the results
    order_details = dict(order)
    order_details['items'] = [dict(item) for item in items]
    
    return jsonify(order_details)

# --- CREATE a New Order (New Endpoint) ---
@app.route('/orders', methods=['POST'])
def create_order():
    """Creates a new order with items."""
    data = request.get_json()
    if not data or 'customer_name' not in data or 'items' not in data:
        return jsonify({'error': 'Missing required fields: customer_name and items'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Create the main order record
    cursor.execute('INSERT INTO orders (customer_name) VALUES (?)', (data['customer_name'],))
    order_id = cursor.lastrowid
    
    # 2. Add each item from the cart to the order_items table
    total_price = 0
    for item in data['items']:
        cursor.execute('INSERT INTO order_items (order_id, game_name, quantity, price) VALUES (?, ?, ?, ?)',
                     (order_id, item['game_name'], item['quantity'], item['price']))
        total_price += item['quantity'] * item['price']

    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'order_id': order_id, 'total_price': total_price}), 201

# This part will run only once when the app starts to set up the database
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)