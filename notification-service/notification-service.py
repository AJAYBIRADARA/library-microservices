from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    msg = data.get("msg")

    print("Notification:", msg)

    return jsonify({"message":"Notification sent successfully"})

app.run(host="0.0.0.0", port=5005)