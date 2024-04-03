from fastapi import HTTPException
from config.database import Session
from models.cart_model import Cart, CartItem
from models.products_model import Products
from schemas.products_schema import Product_cart as Product_Schema_cart
from models.user_model import User


class ProductService:
  def create_product(self, product_data):
    db = Session()
    try:
      product = Products(name=product_data.name, image=product_data.image, price=product_data.price, stock=product_data.stock)
      db.add(product)
      db.commit()
      db.refresh(product)
      db.close()
      return product
    except Exception as e:
      db.rollback()
      db.close()
      raise HTTPException(status_code=400, detail=str(e))
    
  def get_products(self):
    db = Session()
    products = db.query(Products).all()
    #reccorrer los productos y solo motrar los que tengan stock > 0
    products = [product for product in products if product.stock > 0]
    db.close()

    
    return products

  def update_product(self, product_data):
    db = Session()
    product = db.query(Products).filter(Products.id == product_data.id).first()
    if product:
      product.name = product_data.name
      product.image = product_data.image
      product.price = product_data.price
      product.stock = product_data.stock
      db.commit()
      db.refresh(product)
      db.close()
      return product
    else:
      db.close()
      raise HTTPException(status_code=404, detail="Product not found")
    
  def delete_product(self, product_data):
    db = Session()
    product = db.query(Products).filter(Products.name == product_data.name).first()
    if product:
      db.delete(product)
      db.commit()
      db.close()
      return product
    else:
      db.close()
      raise HTTPException(status_code=404, detail="Product not found")
    
  def product_add_cart(self, product_data: Product_Schema_cart, current_user: User):
    db = Session()
    user = db.query(User).filter(User.id == current_user.id).first()

    if not db.query(Cart).filter(Cart.user_id == current_user.id).first():
    # Si no tiene carrito, crear uno
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    else:
       cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    product = db.query(Products).filter(Products.id == product_data.product_id).first()

    if product:
        if product.stock > 0:
            cart_item = db.query(CartItem).filter(
                CartItem.cart_id == cart.id,
                CartItem.product_id == product.id
            ).first()


            if cart_item:
                cart_item.quantity += 1
            else:
                cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
                db.add(cart_item)

            # Actualizar el precio total del carrito
            cart.total_price = product.price * cart_item.quantity
            db.commit()
            db.close()
            return product_data
        else:
            db.close()
            raise HTTPException(status_code=400, detail="Product out of stock")
    else:
        db.close()
        raise HTTPException(status_code=404, detail="Product not found")