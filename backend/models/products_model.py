from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base
from models.cart_model import CartItem

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Integer)
    stock = Column(Integer)
    image = Column(String)

    cart = relationship("CartItem", back_populates="product")

