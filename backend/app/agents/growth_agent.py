import re
from app.tools.catalogue import search_catalogue
from app.services.recommendation import score_product, complementary

DEVICES = ["Samsung Galaxy S24 Ultra", "iPhone 15 Pro", "MacBook Air M3", "Samsung Galaxy S24", "Pixel 8"]
class GrowthAgent:
    def respond(self, message, customer, products):
        device = next((d for d in DEVICES if d.lower() in message.lower()), None)
        intent_words = re.findall(r"[a-z0-9]+", message.lower())
        found = search_catalogue(message, products, device)
        if not found:
            return {"reply": "I couldn't find an in-stock matching item. Try a device name or product category.", "recommendations": [], "timeline": ["Intent understood", "Catalogue searched: no safe match"]}
        ranked = sorted(found, key=lambda p: score_product(p, intent_words, device, customer), reverse=True)
        primary = ranked[0]
        score = score_product(primary, intent_words, device, customer)
        add_on = complementary(primary, products, device)
        recommendations=[{"id": primary["id"], "name": primary["name"], "price": primary["price"], "score": score, "reason": f"Matches your request{(' and is compatible with ' + device) if device else ''}."}]
        if add_on:
            recommendations.append({"id": add_on["id"], "name": add_on["name"], "price": add_on["price"], "score": score_product(add_on, intent_words, device, customer), "reason": f"A relevant companion to protect or power your {device or 'purchase'}—not a random add-on."})
        bundle = primary["price"] + (add_on["price"] if add_on else 0)
        reply = f"I found {primary['name']} for ₹{primary['price']:,}. " + (f"I also suggest {add_on['name']} because it complements the primary purchase. Together: ₹{bundle:,}." if add_on else "It's the strongest in-stock match for your request.")
        return {"reply": reply, "recommendations": recommendations, "timeline": ["Intent and device entities extracted", f"Catalogue searched: {len(found)} relevant in-stock items", "Recommendation ranked by compatibility, intent, history, popularity and margin", "Policy checked: recommendation proposed — no payment action taken"], "device": device}
