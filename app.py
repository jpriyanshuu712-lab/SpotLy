from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load restaurant data
df = pd.read_csv("restaurants.csv")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend")
def recommend():

    cuisine = request.args.get("cuisine", "").lower()

    filtered = df[df["Cuisine Type"].str.lower().str.contains(cuisine)]

    results = []

    for _, row in filtered.head(10).iterrows():
       results.append({
    "name": row["Restaurant Name"],
    "cuisine": row["Cuisine Type"],
    "location": row["Area / Location"],
    "rating": row["Rating"],
    "price": row["Price Range (for 2)"],
    "tags": row["Tags"]
})

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
