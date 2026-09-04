from dataclasses import dataclass

@dataclass
class PolicyResult:
    approved: bool
    reason: str

class PolicyEngine:
    MAX_DISCOUNT = 10
    def validate_recommendation(self, products, catalogue):
        if not products:
            return PolicyResult(False, "A recommendation must include a catalogue product.")
        for product in products:
            item = catalogue.get(product["id"])
            if not item:
                return PolicyResult(False, f"Unknown catalogue product: {product['id']}")
            if item["stock"] <= 0:
                return PolicyResult(False, f"{item['name']} is out of stock.")
        return PolicyResult(True, "All recommended products are valid and available.")

    def validate_order(self, items, discount_percent, confirmed, catalogue):
        if not confirmed:
            return PolicyResult(False, "Explicit customer confirmation is required before creating an order.")
        if discount_percent > self.MAX_DISCOUNT:
            return PolicyResult(False, f"Discount {discount_percent}% exceeds the 10% business limit.")
        if not items:
            return PolicyResult(False, "An order needs at least one item.")
        return self.validate_recommendation(items, catalogue)
