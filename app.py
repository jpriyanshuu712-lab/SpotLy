from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the CSV once at startup instead of on every request -- with 10,000+
# rows, re-reading from disk on every /recommend call adds real latency.
DF = pd.read_csv("restaurants.csv")
DF = DF.fillna("")

# Columns that get searched when someone types/picks a "what" query --
# a cuisine name, a dish like "momos" or "sushi", a food type like
# "snacks" or "sweets", or an occasion like "party" or "fine dine".
SEARCHABLE_TEXT_COLUMNS = ["Cuisine Type", "Popular Dishes", "Food Type", "Tags"]


def _row_matches_query(df, query: str):
    """Return a boolean mask: True for rows where `query` appears in ANY
    of the searchable text columns (cuisine, dish, food type, or tag)."""
    mask = pd.Series(False, index=df.index)
    for col in SEARCHABLE_TEXT_COLUMNS:
        if col in df.columns:
            mask = mask | df[col].astype(str).str.contains(query, case=False, na=False)
    return mask


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/meta")
def meta():
    """Optional: powers dropdowns/suggestions if your frontend wants them.
    Safe to ignore/not call -- it doesn't affect /recommend."""
    locations = sorted(DF["Area / Location"].unique().tolist())
    price_bands = sorted(DF["Price Range (for 2)"].unique().tolist())
    cuisines = sorted(set(
        c.strip() for cell in DF["Cuisine Type"] for c in str(cell).split(",") if c.strip()
    ))
    dishes = sorted(set(
        d.strip() for cell in DF["Popular Dishes"] for d in str(cell).split(",") if d.strip()
    )) if "Popular Dishes" in DF.columns else []
    food_types = sorted(set(
        f.strip() for cell in DF["Food Type"] for f in str(cell).split(",") if f.strip()
    )) if "Food Type" in DF.columns else []
    occasions = ["Party", "Fine Dine", "Evening Snack", "Date Night",
                 "Business Meeting", "Celebration", "Casual Hangout",
                 "Solo Dining", "Family Gathering"]

    return jsonify({
        "locations": locations,
        "price_bands": price_bands,
        "cuisines": cuisines,
        "dishes": dishes,
        "food_types": food_types,
        "occasions": occasions,
    })


@app.route("/recommend")
def recommend():
    # New unified field: matches cuisine, dish, food type, or occasion/tag
    # all at once (e.g. "momos", "sushi", "party", "sweets").
    query = request.args.get("q", "").strip()

    # Original params, still supported exactly as before.
    cuisine = request.args.get("cuisine", "").strip()
    location = request.args.get("location", "").strip()
    price = request.args.get("price", "").strip()

    # Optional pagination -- OFF by default (limit=0 means "no limit"),
    # so behavior matches the original app exactly unless you opt in.
    limit = request.args.get("limit", default=0, type=int)
    offset = request.args.get("offset", default=0, type=int)

    df = DF

    if query:
        df = df[_row_matches_query(df, query)]
    if cuisine:
        df = df[df["Cuisine Type"].str.contains(cuisine, case=False, na=False)]
    if location:
        df = df[df["Area / Location"].str.contains(location, case=False, na=False)]
    if price:
        # Falls back to substring match so it still works if your frontend
        # sends a partial price string instead of an exact band.
        exact = df["Price Range (for 2)"] == price
        df = df[exact] if exact.any() else df[df["Price Range (for 2)"].astype(str).str.contains(price, na=False)]

    if limit and limit > 0:
        df = df.iloc[offset: offset + limit]

    results = []
    for _, row in df.iterrows():
        rating = row["Rating"]
        if rating == "" or rating != rating:
            rating = 0
        results.append({
            "name": row["Restaurant Name"],
            "cuisine": row["Cuisine Type"],
            "dishes": row.get("Popular Dishes", ""),
            "food_type": row.get("Food Type", ""),
            "location": row["Area / Location"],
            "rating": float(rating),
            "price": row["Price Range (for 2)"],
            "tags": row["Tags"],
        })

    # IMPORTANT: plain array response, same shape as the original app.py,
    # so any existing frontend that does `data.forEach(...)` keeps working.
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
