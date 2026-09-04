import json
from pathlib import Path
DATA = Path(__file__).parents[3] / "data" / "customers.json"
def get_customer_context(customer_id):
    customers = json.loads(DATA.read_text(encoding="utf-8"))
    return next((c for c in customers if c["id"] == customer_id), {"id": customer_id, "preferences": [], "previous_purchases": [], "browsing_history": [], "average_order_value": 0})
