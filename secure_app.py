from flask import Flask, request, jsonify
import sqlite3
import re

app = Flask(__name__)


def is_valid_username(username):
    
    return re.match("^[a-zA-Z0-9_]{3,20}$", username)


def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL
        )
    ''')

    cursor.execute("INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)", ("admin", "admin@example.com"))
    conn.commit()
    conn.close()

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username parameter is missing."}), 400

    if not is_valid_username(username):
        return jsonify({"error": "Invalid username format."}), 400

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

       
        cursor.execute("SELECT id, username, email FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({
                "id": user[0],
                "username": user[1],
                "email": user[2]
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    init_db()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
