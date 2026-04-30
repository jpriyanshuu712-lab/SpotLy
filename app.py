import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

data = pd.read_csv("restaurants.csv")

@app.route("/")
def home():
    return "Spotly is running!"

@app.route("/recommend", methods=["GET"])
def recommend():
    cuisine = request.args.get("cuisine")

    results = data[data["Cuisine"].str.contains(cuisine, case=False, na=False)]

    return jsonify(results.head(5).to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
