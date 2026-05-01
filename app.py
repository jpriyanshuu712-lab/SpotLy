
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend")
def recommend():

    cuisine = request.args.get("cuisine", "")
    location = request.args.get("location", "")
    price = request.args.get("price", "")

    df = pd.read_csv("restaurants.csv")

    # remove NaN
    df = df.fillna("")

    if cuisine:
        df = df[df["Cuisine Type"].str.contains(cuisine, case=False)]

    if location:
        df = df[df["Area / Location"].str.contains(location, case=False)]

    if price:
        df = df[df["Price Range (for 2)"].astype(str).str.contains(price)]

    results = []

    for _, row in df.iterrows():

        rating = row["Rating"]
        if rating == "" or rating != rating:
            rating = 0

        results.append({
            "name": row["Restaurant Name"],
            "cuisine": row["Cuisine Type"],
            "location": row["Area / Location"],
            "rating": float(rating),
            "price": row["Price Range (for 2)"],
            "tags": row["Tags"]
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
