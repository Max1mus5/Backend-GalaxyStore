from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base
from models.cart_model import Cart

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    cart = relationship("Cart", back_populates="user")