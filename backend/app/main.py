from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.models.schemas import ChatRequest, CheckoutRequest, FailureRequest
from app.tools.catalogue import load_catalogue, as_map
from app.tools.customer import get_customer_context
from app.tools.razorpay_tool import PaymentProvider
from app.agents.growth_agent import GrowthAgent
from app.policies.policy_engine import PolicyEngine
from app.services import audit

app = FastAPI(title="GROWTHPILOT AI", version="1.0.0")
agent, policy, payments = GrowthAgent(), PolicyEngine(), PaymentProvider()
ROOT = Path(__file__).parents[2]

@app.on_event("startup")
def startup(): audit.init_db()

@app.get("/")
def home(): return FileResponse(ROOT / "frontend" / "public" / "index.html")

@app.get("/api/catalogue")
def catalogue(): return load_catalogue()

@app.post("/api/chat")
def chat(request: ChatRequest):
    products = load_catalogue(); customer = get_customer_context(request.customer_id)
    result = agent.respond(request.message, customer, products)
    audit.log("AGENT", "recommendation", "PROPOSED", "Explainable recommendation generated; payment authority not granted.", {"request": request.message, "recommendations": result["recommendations"]})
    return result

@app.post("/api/checkout")
def checkout(request: CheckoutRequest):
    catalogue_map = as_map(load_catalogue())
    raw_items = [{"id": i.product_id, "quantity": i.quantity} for i in request.items]
    result = policy.validate_order(raw_items, request.discount_percent, request.customer_confirmed, catalogue_map)
    if not result.approved:
        audit.log("POLICY", "create_order", "REJECTED", result.reason, request.model_dump())
        raise HTTPException(400, result.reason)
    total = sum(catalogue_map[i.product_id]["price"] * i.quantity for i in request.items)
    final = round(total * (1 - request.discount_percent / 100))
    try:
        order = payments.create_order(final * 100, "growthpilot")
    except Exception as exc:
        audit.log("PAYMENT", "create_order", "FAILED", "Payment provider error; checkout was not opened.", {"error": str(exc)})
        raise HTTPException(502, "Order creation failed safely. Please retry.")
    audit.log("PAYMENT", "create_order", "SUCCESS", "Confirmed order created. Checkout may now open.", {"order_id": order["id"], "amount": final})
    return {"status": "success", "message": "Order created after confirmation. Checkout may now open.", "order": order, "amount": final}

@app.get("/api/audit")
def audit_log(): return audit.recent()

@app.get("/api/metrics")
def metrics():
    from scripts.run_simulation import simulate
    return simulate(100, seed=42)

@app.post("/api/demo/failure")
def demo_failure(request: FailureRequest):
    data = as_map(load_catalogue())
    if request.scenario == "invalid_product": result = policy.validate_order([{"id":"not_a_product","quantity":1}], 0, True, data)
    elif request.scenario == "excess_discount": result = policy.validate_order([{"id":"product_001","quantity":1}], 25, True, data)
    elif request.scenario == "out_of_stock":
        out=next(p for p in data.values() if p["stock"] == 0); result=policy.validate_order([{"id":out["id"],"quantity":1}],0,True,data)
    elif request.scenario == "no_confirmation": result=policy.validate_order([{"id":"product_001","quantity":1}],0,False,data)
    else:
        audit.log("PAYMENT", "create_order", "FAILED", "Simulated provider outage. Checkout was not opened.")
        return {"status":"FAILED", "reason":"Simulated Razorpay API failure; safe retry offered."}
    audit.log("POLICY", "failure_demo", "REJECTED" if not result.approved else "SUCCESS", result.reason)
    return {"status":"REJECTED" if not result.approved else "SUCCESS", "reason":result.reason}
