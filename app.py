from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load dataset
data = pd.read_csv("restaurants.csv", encoding="latin1")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend")
def recommend():
    cuisine = request.args.get("cuisine")

    if not cuisine:
        return jsonify({"error": "Please provide a cuisine"}), 400

    # Filter based on your CSV column
    results = data[data["Cuisine Type"].str.contains(cuisine, case=False, na=False)]

    # Convert to list
    restaurants = results.head(5).to_dict(orient="records")

    return jsonify(restaurants)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
