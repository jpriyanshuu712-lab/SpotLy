import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

data = pd.read_csv("restaurants.csv", encoding="latin1")

@app.route("/")
def home():
    return "Spotly is running!"

@app.route("/recommend")
def recommend():
    cuisine = request.args.get("cuisine")

    if not cuisine:
        return jsonify({"error": "Please provide a cuisine"}), 400

    results = data[data["Cuisine Type"].str.contains(cuisine, case=False, na=False)]

    return jsonify(results.head(5).to_dict(orient="records"))

if __name__ == "__main__":
    app.run()
