from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# 🔹 GET RECORD BY USERNAME
@app.route("/record/<username>", methods=["GET"])
def get_record(username):
    try:
        # Call issue-service (Docker service name)
        res = requests.get("http://issue-service:5003/issued")
        data = res.json()

        # Filter user records
        user_records = [
            {
                "book": r["book"],
                "issue_date": r["issue_date"],
                "return_date": r["return_date"]
            }
            for r in data if r["user"] == username
        ]

        return jsonify(user_records)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.run(host="0.0.0.0", port=5006)