from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/fine", methods=["GET"])
def get_fine():
    return jsonify({"fine": 50})

app.run(host="0.0.0.0", port=5004)