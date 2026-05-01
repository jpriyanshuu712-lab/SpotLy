import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

try:
    data = pd.read_csv("restaurants.csv", encoding="latin1")
except Exception as e:
    print("CSV error:", e)
    data = pd.DataFrame()

@app.route("/")
def home():
    return "Spotly is running!"

@app.route("/recommend")
def recommend():
    cuisine = request.args.get("cuisine", "")

    results = data[data["Cuisine"].str.contains(cuisine, case=False, na=False)]

    return jsonify(results.head(5).to_dict(orient="records"))
