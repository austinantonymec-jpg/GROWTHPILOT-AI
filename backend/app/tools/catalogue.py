import json
from pathlib import Path

DATA = Path(__file__).parents[3] / "data" / "products.json"

def load_catalogue():
    return json.loads(DATA.read_text(encoding="utf-8"))

def as_map(products): return {p["id"]: p for p in products}

def search_catalogue(query, products, device=None):
    words = set(query.lower().replace("-", " ").split())
    matches = []
    for p in products:
        corpus = " ".join([p["name"], p["category"], p["description"], *p["tags"], *p["compatible_devices"]]).lower()
        score = sum(word in corpus for word in words)
        if device and device.lower() in " ".join(p["compatible_devices"]).lower(): score += 8
        if score and p["stock"] > 0: matches.append((score, p))
    return [p for _, p in sorted(matches, key=lambda x: (-x[0], -x[1]["popularity"]))[:8]]
