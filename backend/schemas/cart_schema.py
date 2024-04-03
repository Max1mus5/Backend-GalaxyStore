from typing import List
from pydantic import BaseModel

class CartItemSchema(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unity_price: float
    total_price: float

class Order(BaseModel):
    user_id: int
    items: List[CartItemSchema]