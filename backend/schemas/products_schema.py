from pydantic import BaseModel

class Product(BaseModel):
    name: str
    image: str
    price: float
    stock: int

class ProductWithIndexSchema(Product):
    index: int

class Product_cart(BaseModel):
    product_id: int
