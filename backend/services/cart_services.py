from fastapi import HTTPException
from config.database import Session
from models.cart_model import Cart, CartItem
from models.products_model import Products
from schemas.cart_schema import Order, CartItemSchema

class CartService:
  def get_cart(self, current_user):
        cart_items = []
        db = Session()
        try:
            cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
            if cart:
                for item in cart.items:
                    if item.product_id:
                        product = db.query(Products).filter(Products.id == item.product_id).first()
                        cart_item = CartItemSchema(product_id=product.id, product_name=product.name, quantity=item.quantity, unity_price=product.price,total_price=product.price * item.quantity)
                        cart_items.append(cart_item)
                    else:
                        db.delete(item)
                db.commit()
                return cart_items
            else:
                #retrona un carro vacio
                return []
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()

  def update_cart(self, current_user, product_id, new_quantity):
        db = Session()
        try:
            cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
            if cart:
                item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
                if item:
                    product = db.query(Products).filter(Products.id == product_id).first()
                    item.quantity = new_quantity
                    db.commit()
                    return Order(user_id=current_user.id, items=[CartItemSchema(product_id=product.id, product_name=product.name, quantity=item.quantity, unity_price=product.price,total_price=product.price * item.quantity)])
                else:
                    raise HTTPException(status_code=404, detail="Product not found in cart")
            else:
                raise HTTPException(status_code=404, detail="Cart not found")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()

  def delete_cart(self, current_user):
        db = Session()
        try:
            cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
            if cart:
                for item in cart.items:
                    db.delete(item)
                db.delete(cart)
                db.commit()
            else:
                raise HTTPException(status_code=404, detail="Cart not found")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()

  def buy_cart(self, current_user):
        db = Session()
        try:
            cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
            if cart:
                total_price = 0
                for item in cart.items:
                    product = db.query(Products).filter(Products.id == item.product_id).first()
                    if product.stock >= item.quantity:
                        total_price += product.price * item.quantity
                        product.stock -= item.quantity  
                    else:
                        #se vende lo que haya en stock
                        total_price += product.price * product.stock
                        product.stock = 0
                        
                cart.total_price = total_price
                db.delete(cart)
                db.commit()
                return total_price
            else:
                raise HTTPException(status_code=404, detail="Cart not found")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()