from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from config.database import Base

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    quantity = Column(Integer)
    total_price = Column(Float)

    product = relationship("Products", back_populates="cart")
    user = relationship("User", back_populates="cart")