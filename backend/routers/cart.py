from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from utils.getUser import get_current_user
from models.user_model import User
from schemas.products_schema import Product as Product_Schema
from schemas.cart_schema import Order, CartItemSchema
from services.cart_services import CartService
from typing import List


cart_router = APIRouter()

@cart_router.get("/get_cart/", response_model=List[CartItemSchema], status_code=200)
def get_cart(current_user: User = Depends(get_current_user)):
    mycart = CartService().get_cart(current_user=current_user)
    return mycart

@cart_router.delete("/delete_cart/", status_code=200)
def delete_cart(current_user: User = Depends(get_current_user)):
    CartService().delete_cart(current_user=current_user)
    return JSONResponse(content={"message":"Cart deleted"}, status_code=200)

@cart_router.put("/update_cart/", response_model=Order, status_code=200)
def update_cart(current_user: User = Depends(get_current_user), product_id: int = 0, new_quantity: int = 0):
    if product_id == 0 or new_quantity == 0:
        return JSONResponse(content={"message":"Product id and new quantity are required"}, status_code=400)
    else:
        CartService().update_cart(current_user=current_user, product_id=product_id, new_quantity=new_quantity)
    return JSONResponse(content={"message":"Cart updated"}, status_code=200)

@cart_router.put("/buy_cart/", status_code=200)
def buy_cart(current_user: User = Depends(get_current_user)):
    total_price = CartService().buy_cart(current_user=current_user)
    return JSONResponse(content={"message":"Cart bought", "total_price":total_price}, status_code=200)	