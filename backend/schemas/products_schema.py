from pydantic import BaseModel

class Product(BaseModel):
    name: str
    image: str
    price: float
    stock: int