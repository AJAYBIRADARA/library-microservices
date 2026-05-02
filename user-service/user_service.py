from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

def get_db():
    return sqlite3.connect("users.db")

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 🔹 REGISTER
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    hashed_password = generate_password_hash(data["password"])

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users(first_name,last_name,phone,email,address,username,password)
            VALUES(?,?,?,?,?,?,?)
        """, (
            data["first_name"],
            data["last_name"],
            data["phone"],
            data["email"],
            data["address"],
            data["username"],
            hashed_password
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Account created successfully"})

    except:
        return jsonify({"message": "Username already exists"}), 400


# 🔹 LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (data["username"],))
    user = cur.fetchone()
    conn.close()

    if user and check_password_hash(user[0], data["password"]):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid username or password"}), 401


# 🔹 GET USERS (optional)
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username, email FROM users")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"username": r[0], "email": r[1]} for r in rows])


app.run(host="0.0.0.0", port=5001)