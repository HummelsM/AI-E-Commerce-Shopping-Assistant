import csv
import os
import re
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
CATALOGUE_PATH = Path(__file__).with_name("fictional_electronics_catalogue_usd.csv")


def load_products():
    with CATALOGUE_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


PRODUCTS = load_products()


def answer_question(question):
    """Starter catalogue search. Add an LLM call here for richer language understanding."""
    q = question.lower().strip()
    if not q:
        return {"message": "Please enter a question about our products.", "products": []}

    # Detect a maximum budget, e.g. "under $300", "less than 1000 dollars".
    budget = None
    patterns = [
        r"(?:under|below|less than|up to|max(?:imum)?(?: of)?)\s*\$?\s*([\d,]+)",
        r"\$\s*([\d,]+)\s*(?:or less|maximum|max)?"
    ]
    for pattern in patterns:
        match = re.search(pattern, q)
        if match:
            budget = float(match.group(1).replace(",", ""))
            break

    tokens = set(re.findall(r"[a-z0-9]+", q))
    stop_words = {
        "i", "im", "i'm", "looking", "for", "a", "an", "the", "do", "you",
        "have", "any", "can", "you", "find", "me", "show", "want", "need",
        "with", "under", "below", "less", "than", "up", "to", "my", "is",
        "are", "and", "or", "of", "please", "product", "products", "item",
        "items", "buy", "purchase", "what", "which", "would", "be", "good",
        "best", "dollars", "dollar", "price", "cost", "for"
    }
    keywords = tokens - stop_words

    scored = []
    for product in PRODUCTS:
        searchable = " ".join([
            product.get("Product_Name", ""),
            product.get("Category", ""),
            product.get("Brand", ""),
            product.get("Description", "")
        ]).lower()
        price = float(product.get("Price_USD", 0) or 0)

        if budget is not None and price > budget:
            continue

        score = sum(1 for word in keywords if len(word) > 1 and word in searchable)
        # Category synonyms to help simple natural-language queries.
        synonym_groups = {
            "headphones": ["audio", "headphones", "earbuds"],
            "earbuds": ["earbuds", "audio"],
            "laptop": ["laptops", "laptop", "notebook"],
            "computer": ["laptops", "accessories", "computer"],
            "tv": ["tvs", "displays", "television"],
            "television": ["tvs", "displays", "television"],
            "camera": ["cameras", "camera"],
            "gaming": ["gaming", "gameforge", "console"],
            "router": ["networking", "router", "wi-fi"],
            "speaker": ["audio", "speaker", "soundbar"],
            "phone": ["smartphones", "phone"],
            "smartphone": ["smartphones", "phone"],
            "tablet": ["tablets", "tablet"],
        }
        for token, terms in synonym_groups.items():
            if token in tokens and any(term in searchable for term in terms):
                score += 2

        if score > 0:
            scored.append((score, price, product))

    scored.sort(key=lambda item: (-item[0], item[1]))
    matches = [item[2] for item in scored[:5]]

    if not matches:
        if budget is not None:
            message = f"I couldn't find a clear match under ${budget:,.0f}. Try a product type such as laptop, headphones, TV, camera, or router."
        else:
            message = "I couldn't find a clear match. Try asking about a category, brand, product name, or budget—for example, 'wireless headphones under $300'."
        return {"message": message, "products": []}

    if budget is not None:
        intro = f"I found {len(matches)} matching product(s) priced at or below ${budget:,.0f}. Here are the closest catalogue matches:"
    else:
        intro = f"I found {len(matches)} possible catalogue match(es). You can refine your search by adding a budget or a feature:"
    return {"message": intro, "products": matches}


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("message", "")).strip()
    if len(question) > 500:
        return jsonify({"error": "Please keep your question under 500 characters."}), 400
    result = answer_question(question)
    return jsonify(result)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "products_loaded": len(PRODUCTS)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")), debug=False)
