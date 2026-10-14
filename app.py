from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


def init_db():
  conn = sqlite3.connect('parking.db')
  cursor = conn.cursor()
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
  conn.commit()
  conn.close()


@app.route('/api/register', methods=['POST'])
def register():
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')

  if not username or not password:
    return jsonify({'error': 'Username aur password dena zaroori hai'}), 400

  try:
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, password),
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'User successfully register ho gaya hai!'}), 201
  except sqlite3.IntegrityError:
    return jsonify({'error': 'Yeh username pehle se exist karta hai'}), 400


@app.route('/api/login', methods=['POST'])
def login():
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')

  conn = sqlite3.connect('parking.db')
  cursor = conn.cursor()
  cursor.execute(
      'SELECT * FROM users WHERE username = ? AND password = ?',
      (username, password),
  )
  user = cursor.fetchone()
  conn.close()

  if user:
    return jsonify({'message': 'Login successful!', 'username': username}), 200
  else:
    return jsonify({'error': 'Invalid username ya password'}), 401


if __name__ == '__main__':
  init_db()
  app.run(debug=True, port=5000)