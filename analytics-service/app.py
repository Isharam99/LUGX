import os
from flask import Flask, request, jsonify
from clickhouse_driver import Client
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CLICKHOUSE_HOST = os.environ.get('CLICKHOUSE_HOST', 'clickhouse-service')
CLICKHOUSE_PASSWORD = os.environ.get('CLICKHOUSE_PASSWORD', 'password123')

def get_client():
    """Creates a new client connection."""
    return Client(host=CLICKHOUSE_HOST, password=CLICKHOUSE_PASSWORD)

def initialize_schema(client):
    """Ensures the database and table exist."""
    client.execute('CREATE DATABASE IF NOT EXISTS analytics_db')
    client.execute('''
        CREATE TABLE IF NOT EXISTS analytics_db.events (
            event_time DateTime DEFAULT now(),
            event_type String,
            page_url String
        ) ENGINE = MergeTree()
        ORDER BY event_time
    ''')

@app.route('/track', methods=['POST'])
def track_event():
    """Receives, ensures schema exists, and stores a tracking event."""
    data = request.get_json()
    if not data or 'event_type' not in data or 'page_url' not in data:
        return jsonify({"error": "Invalid data"}), 400

    try:
        client = get_client()
        # Ensure DB and table exist before trying to insert
        initialize_schema(client)
        
        # Let ClickHouse handle the timestamp automatically
        client.execute(
            'INSERT INTO analytics_db.events (event_type, page_url) VALUES',
            [(data['event_type'], data['page_url'])]
        )
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
