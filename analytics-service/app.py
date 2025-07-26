import os
from flask import Flask, request, jsonify
from clickhouse_driver import Client
from flask_cors import CORS 

app = Flask(__name__)

# The service name 'clickhouse-service' is used as the host
CLICKHOUSE_HOST = os.environ.get('CLICKHOUSE_HOST', 'clickhouse-service')
client = Client(host=CLICKHOUSE_HOST)

def init_db():
    """Creates the analytics table in ClickHouse if it doesn't exist."""
    client.execute('''
        CREATE TABLE IF NOT EXISTS analytics_db.events (
            event_time DateTime,
            event_type String,
            page_url String
        ) ENGINE = MergeTree()
        ORDER BY event_time
    ''')

@app.route('/track', methods=['POST'])
def track_event():
    """Receives and stores a tracking event."""
    data = request.get_json()
    if not data or 'event_type' not in data or 'page_url' not in data:
        return jsonify({"error": "Invalid data"}), 400

    try:
        client.execute(
            'INSERT INTO analytics_db.events (event_type, page_url, event_time) VALUES',
            [(data['event_type'], data['page_url'], 'now()')]
        )
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Initialize the database and table on startup
try:
    client.execute('CREATE DATABASE IF NOT EXISTS analytics_db')
    init_db()
except Exception as e:
    print(f"Could not initialize database: {e}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)