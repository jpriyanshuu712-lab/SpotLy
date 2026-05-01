import pandas as pd
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Load restaurant dataset
data = pd.read_csv("restaurants.csv")

# Home page
@app.route("/")
def home():
    return send_file("index.html")

# Recommendation API
@app.route("/recommend")
def recommend():
    cuisine = request.args.get("cuisine")

    if cuisine:
        results = data[data["cuisine"].str.contains(cuisine, case=False, na=False)]
    else:
        results = data

    return jsonify(results.to_dict(orient="records"))

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
