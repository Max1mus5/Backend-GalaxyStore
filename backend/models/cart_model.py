from sqlalchemy import Column, Integer, ForeignKey,Float
from sqlalchemy.orm import relationship
from config.database import Base

class CartItem(Base):
    __tablename__ = "cart_item"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("cart.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    # Definir la relación con la tabla Cart
    cart = relationship("Cart", back_populates="items")

    # Definir la relación con la tabla Products
    product = relationship("Products", back_populates="cart")


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float)

    # Definir la relación inversa con la tabla User
    user = relationship("User", back_populates="cart")

    # Definir la relación inversa con la tabla CartItem
    items = relationship("CartItem", back_populates="cart")
