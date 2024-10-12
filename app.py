from flask import Flask, jsonify
import pyodbc
import config  # Configuration file for database settings

app = Flask(__name__)

# Database connection function
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={config.DRIVER};'
            f'SERVER={config.SERVER};'
            f'DATABASE={config.DATABASE};'
            f'UID={config.USERNAME};'
            f'PWD={config.PASSWORD};'
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM SampleTable")  # Modify this query based on your table
    row = cursor.fetchone()

    if row:
        result = {"id": row[0], "name": row[1]}
        conn.close()
        return jsonify(result)
    else:
        conn.close()
        return jsonify({"error": "No data found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
