from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base
from models.products_model import Products
from models.cart_model import Cart

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    products = relationship("Products", back_populates="owner")
    cart = relationship("Cart", back_populates="user")