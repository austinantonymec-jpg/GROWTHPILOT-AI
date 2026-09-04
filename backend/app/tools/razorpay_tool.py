import os, uuid

class PaymentProvider:
    def create_order(self, amount_paise, receipt):
        key_id, secret = os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")
        if key_id and secret and key_id != "rzp_test_replace_me":
            import razorpay
            client = razorpay.Client(auth=(key_id, secret))
            order = client.order.create({"amount": amount_paise, "currency": "INR", "receipt": receipt})
            return {"id": order["id"], "provider": "razorpay", "key_id": key_id}
        return {"id": "order_demo_" + uuid.uuid4().hex[:12], "provider": "demo", "key_id": None}
