from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = "parking.db"

# Initialize Database and Tables
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # 2. Parking Slots Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_number TEXT UNIQUE NOT NULL,
            is_available BOOLEAN NOT NULL,
            slot_type TEXT NOT NULL
        )
    ''')

    # 3. Bookings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            slot_id INTEGER,
            booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (slot_id) REFERENCES parking_slots (id)
        )
    ''')
    
    # Add initial parking slots if empty
    cursor.execute('SELECT COUNT(*) FROM parking_slots')
    if cursor.fetchone()[0] == 0:
        initial_slots = [
            ("A1", 1, "Car"),
            ("A2", 0, "Car"),
            ("B1", 1, "Bike")
        ]
        cursor.executemany('''
            INSERT INTO parking_slots (slot_number, is_available, slot_type)
            VALUES (?, ?, ?)
        ''', initial_slots)
        conn.commit()
    
    conn.close()

init_db()

@app.route("/")
def home():
    return jsonify({"message": "Parking Management System API is running!"})

# Route: Register User
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        ''', (username, email, password))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "User registered successfully!"})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"success": False, "message": "Username or Email already exists!"}), 400

# Route: Login User
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "success": True,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"]
            }
        })
    else:
        return jsonify({"success": False, "message": "Invalid email or password!"}), 401

# Route: Get all parking slots
@app.route("/api/slots", methods=["GET"])
def get_slots():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parking_slots')
    rows = cursor.fetchall()
    conn.close()

    slots = [{"id": r["id"], "slot_number": r["slot_number"], "is_available": bool(r["is_available"]), "type": r["slot_type"]} for r in rows]
    return jsonify(slots)

# Route: Book a slot
@app.route("/api/book", methods=["POST"])
def book_slot():
    data = request.json
    user_id = data.get("user_id")
    slot_id = data.get("slot_id")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT is_available FROM parking_slots WHERE id = ?', (slot_id,))
    slot = cursor.fetchone()
    
    if not slot:
        conn.close()
        return jsonify({"success": False, "message": "Slot not found!"}), 404
    
    if slot[0] == 1:
        cursor.execute('UPDATE parking_slots SET is_available = 0 WHERE id = ?', (slot_id,))
        cursor.execute('INSERT INTO bookings (user_id, slot_id) VALUES (?, ?)', (user_id, slot_id))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Slot booked successfully!"})
    else:
        conn.close()
        return jsonify({"success": False, "message": "Slot is already occupied!"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)