from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def db():
    return sqlite3.connect("books.db")

def init():
    con = db()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT
    )
    """)
    con.commit()
    con.close()

init()

@app.route("/books", methods=["GET"])
def get_books():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT id,title,author FROM books")
    data = cur.fetchall()
    con.close()
    return jsonify([{"id":r[0],"title":r[1],"author":r[2]} for r in data])

@app.route("/add-book", methods=["POST"])
def add():
    d = request.json
    con = db()
    cur = con.cursor()
    cur.execute("INSERT INTO books(title,author) VALUES(?,?)",
                (d["title"], d["author"]))
    con.commit()
    con.close()
    return jsonify({"msg":"Book added"})

# 🔴 DELETE BOOK
@app.route("/delete-book/<int:id>", methods=["DELETE"])
def delete(id):
    con = db()
    cur = con.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (id,))
    con.commit()
    con.close()
    return jsonify({"msg":"Book deleted"})

app.run(host="0.0.0.0", port=5002)