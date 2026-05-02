from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import date

app = Flask(__name__)
CORS(app)

def db():
    return sqlite3.connect("issue.db")

def init():
    con = db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS issued(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        book TEXT,
        issue_date TEXT,
        return_date TEXT
    )
    """)
    con.commit()
    con.close()

init()

# ISSUE BOOK
@app.route("/issue", methods=["POST"])
def issue():
    d = request.json
    today = str(date.today())

    con = db()
    cur = con.cursor()
    cur.execute("""
    INSERT INTO issued(user,book,issue_date,return_date)
    VALUES(?,?,?,?)
    """,(d["user"], d["book"], today, "NOT RETURNED"))
    con.commit()
    con.close()

    return jsonify({"msg":"Book issued"})

# VIEW ISSUED
@app.route("/issued", methods=["GET"])
def get():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM issued")
    rows = cur.fetchall()
    con.close()

    return jsonify([
        {
            "user":r[1],
            "book":r[2],
            "issue_date":r[3],
            "return_date":r[4]
        } for r in rows
    ])

# 🔴 RETURN BOOK
@app.route("/return", methods=["POST"])
def return_book():
    d = request.json
    today = str(date.today())

    con = db()
    cur = con.cursor()
    cur.execute("""
    UPDATE issued 
    SET return_date=? 
    WHERE user=? AND book=? AND return_date='NOT RETURNED'
    """,(today, d["user"], d["book"]))
    con.commit()
    con.close()

    return jsonify({"msg":"Book returned"})

app.run(host="0.0.0.0", port=5003)