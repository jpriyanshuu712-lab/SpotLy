from flask import Flask, request, jsonify, send_file
import pandas as pd

app = Flask(__name__)

# Load dataset
data = pd.read_csv("restaurants.csv", encoding="latin1")

# Homepage
@app.route("/")
def home():
    return send_file("index.html")

# Recommendation API
@app.route("/recommend")
def recommend():
    cuisine = request.args.get("cuisine")

    if not cuisine:
        return jsonify({"error": "Please provide a cuisine"}), 400

    results = data[data["cuisine"].str.contains(cuisine, case=False, na=False)]

    return jsonify(results.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
