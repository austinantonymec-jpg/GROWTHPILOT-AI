from pydantic import BaseModel, Field
from typing import Literal

class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=500)
    customer_id: str = "cust_001"

class CartItem(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1, le=10)

class CheckoutRequest(BaseModel):
    items: list[CartItem]
    discount_percent: float = Field(default=0, ge=0, le=100)
    customer_confirmed: bool = False
    customer_id: str = "cust_001"

class FailureRequest(BaseModel):
    scenario: Literal["invalid_product", "excess_discount", "out_of_stock", "payment_failure", "no_confirmation"]
