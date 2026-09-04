def score_product(product, intent_words, device, customer):
    compatibility = 1 if device and any(device.lower() in d.lower() for d in product["compatible_devices"]) else 0.15
    intent = min(1, sum(w in (product["name"]+" "+product["category"]+" "+" ".join(product["tags"])).lower() for w in intent_words) / max(1,len(intent_words)))
    history = 1 if product["category"] in customer.get("preferences", []) else .2
    popularity = product.get("popularity", 50) / 100
    margin = product.get("margin_percent", 20) / 100
    return round(100 * (.4*compatibility + .3*intent + .15*history + .1*popularity + .05*margin))

def complementary(primary, products, device):
    pairs = {"Phone Case": ["Screen Protector", "Charger", "USB Cable", "Power Bank"], "Laptop": ["Laptop Sleeve", "Keyboard", "Mouse", "USB Hub"], "Smartphone": ["Phone Case", "Screen Protector", "Charger"]}
    wanted = pairs.get(primary["category"], [])
    return next((p for p in products if p["category"] in wanted and p["stock"] > 0 and (not device or not p["compatible_devices"] or any(device.lower() in d.lower() for d in p["compatible_devices"]))), None)
