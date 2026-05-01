@app.route("/recommend")
def recommend():
    query = request.args.get("cuisine")

    if not query:
        return jsonify([])

    df = pd.read_csv("restaurants.csv")

    filtered = df[
        df["Cuisine Type"].str.contains(query, case=False, na=False) |
        df["Area / Location"].str.contains(query, case=False, na=False)
    ]

    results = []

    for _, row in filtered.iterrows():
        results.append({
            "name": row["Restaurant Name"],
            "cuisine": row["Cuisine Type"],
            "location": row["Area / Location"],
            "rating": row["Rating"],
            "price": row["Price Range (for 2)"],
            "tags": row["Tags"]
        })

    return jsonify(results)
