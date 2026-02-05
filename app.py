from flask import Flask, render_template, request
import json

app = Flask(__name__)


# -----------------------------
# Load schemes
# -----------------------------
def load_schemes():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# Recommendation logic
# -----------------------------
def recommend_scheme(occupation, caste, gender, income):
    schemes = load_schemes()
    results = []

    for scheme in schemes:
        score = 0

        if scheme["category"].lower() == occupation.lower():
            score += 2
        if scheme["social_category"].lower() == caste.lower():
            score += 1
        if scheme["gender"].lower() in [gender.lower(), "any"]:
            score += 1
        if income <= scheme["max_income"]:
            score += 2

        if score >= 3:
            results.append(scheme)  # FULL scheme

    return results


# -----------------------------
# First page
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    results = None

    if request.method == "POST":
        occupation = request.form["occupation"]
        caste = request.form["caste"]
        gender = request.form["gender"]
        income = int(request.form["income"])

        results = recommend_scheme(occupation, caste, gender, income)

    return render_template("index.html", results=results)


# -----------------------------
# Second page
# -----------------------------
@app.route("/scheme/<int:scheme_id>")
def scheme_details(scheme_id):
    schemes = load_schemes()
    scheme = next((s for s in schemes if s["id"] == scheme_id), None)

    if scheme is None:
        return "Scheme not found", 404

    return render_template("scheme.html", scheme=scheme)


# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
