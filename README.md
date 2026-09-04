# GROWTHPILOT AI

**An Autonomous Merchant Growth Agent for Intelligent Commerce.**

GrowthPilot turns a shopper's request into an explainable, compatible recommendation and a controlled bundle opportunity. It is deliberately more than a chatbot: an agent orchestrates tools, while a deterministic policy layer retains final authority over money-related actions.

## What it demonstrates

- Intent/device extraction and in-stock catalogue search
- Explainable recommendation scoring: compatibility (40%), intent (30%), history (15%), popularity (10%), and margin (5%)
- Relevant companion-item discovery, rather than indiscriminate upsell
- A hard server-side policy gate: confirmation required, discount capped at 10%, products must exist and have stock
- Razorpay Test Mode integration when credentials exist; otherwise a clearly labelled local demo provider
- SQLite audit log, activity view, synthetic 100-session simulation, and interactive failure lab

## Architecture

See [architecture documentation](docs/architecture.md). The agent never directly calls payment authority. The backend validates the order again at the boundary before requesting a payment order.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_data.py
uvicorn app.main:app --app-dir backend --reload
```

Open `http://127.0.0.1:8000`. The app includes the Shopping Agent, Growth Dashboard, Agent Activity, Audit Log, and Safety Lab.

## Razorpay Test Mode

Copy `.env.example` to `.env` and set `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` to Test Mode credentials. Keep `.env` out of version control. The secret is consumed only by `backend/app/tools/razorpay_tool.py`; it is never returned to or bundled with the browser. Without credentials, checkout returns a demo order so the full demo remains runnable.

## Verification

```powershell
pytest backend/tests -q
python scripts/run_simulation.py
```

The evaluation assumptions and method are in [docs/evaluation.md](docs/evaluation.md). The Safety Lab demonstrates invalid IDs, 25% discount rejection, stock failure, provider outage, and no-confirmation blocking.

## Project layout

```text
backend/app/agents       agent orchestration
backend/app/policies     deterministic money-action guardrail
backend/app/tools        catalogue, customer, payment tools
backend/app/services     recommendations and SQLite audit ledger
data/                    100 synthetic products / 50 synthetic customers
scripts/                 data generator and metrics simulation
frontend/public          polished single-page demo dashboard
```

## Failure behavior

The product never claims an order succeeded after a provider error. Any rejected or failed action is written to the audit log, checkout is not opened, and the UI shows a safe retry message.

## Screenshot placeholders

Add screenshots here before submission: Shopping Agent, Growth Dashboard, Audit Log, and Safety Lab.

## Future improvements

Provider-swappable LLM function calling, durable merchant multi-tenancy, signed Razorpay payment verification/webhooks, real catalogue connectors, and online experimentation with merchant-approved controls.
