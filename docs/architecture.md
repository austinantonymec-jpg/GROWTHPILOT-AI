# Architecture

```text
Customer → Web application → Growth Agent → Catalogue & Customer tools
                                      ↓
                           Explainable recommendation
                                      ↓
                 Deterministic Policy Engine (hard gate)
                                      ↓
           confirmed only → Razorpay Test Mode → audit + metrics
```

The agent can propose, but it cannot create an order. `PolicyEngine.validate_order` runs server-side immediately before the payment provider is called. It verifies explicit confirmation, a maximum 10% discount, valid catalogue IDs, and available stock.
