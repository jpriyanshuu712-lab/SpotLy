from flask import Flask, request, jsonify, send_file
import pandas as pd

app = Flask(__name__)

# Load dataset safely
try:
    data = pd.read_csv("restaurants.csv", encoding="latin1")
    print("CSV loaded successfully")
except Exception as e:
    print("CSV loading error:", e)
    data = pd.DataFrame()

# Home route
@app.route("/")
def home():
    return send_file("index.html")

# Recommendation API
@app.route("/recommend")
def recommend():
    try:
        cuisine = request.args.get("cuisine")

        if not cuisine:
            return jsonify({"error": "Cuisine not provided"}), 400

        results = data[data["cuisine"].str.contains(cuisine, case=False, na=False)]

        return jsonify(results.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
