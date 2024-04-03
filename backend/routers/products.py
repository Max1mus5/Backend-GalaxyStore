from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from utils.getUser import get_current_user
from models.user_model import User
from schemas.products_schema import Product as Product_Schema
from schemas.products_schema import Product_cart as Product_Schema_cart
from services.product_services import ProductService
from typing import List

products_router = APIRouter()

@products_router.post("/create_product/", response_model=List[Product_Schema], status_code=200)
def create_product(product_data: List[Product_Schema], current_user: User = Depends(get_current_user)):
    if not current_user.username == "admin":
        return JSONResponse(content={"message":"Unauthorized"}, status_code=401)
    
    else:
        created_products = []
        if isinstance(product_data, list):  # Verifica si product_data es una lista
            for product in product_data:
                new_product = ProductService().create_product(product_data=product)
                created_products.append(new_product)
        else:
            new_product = ProductService().create_product(product_data=product_data)
            created_products.append(new_product)
            
        return created_products

@products_router.get("/get_products/", status_code=200)
def get_products(current_user: User = Depends(get_current_user)):
    products = ProductService().get_products()
    return products

@products_router.put("/update_product/", response_model=Product_Schema, status_code=200)
def update_product(product_data: Product_Schema, current_user: User = Depends(get_current_user)):
    if not current_user.username == "admin":
        return JSONResponse(content={"message":"Unauthorized"}, status_code=401)
    else:
        updated_product = ProductService().update_product(product_data=product_data)
        return updated_product
    
@products_router.delete("/delete_product/", response_model=Product_Schema, status_code=200)
def delete_product(product_data: Product_Schema, current_user: User = Depends(get_current_user)):
    if not current_user.username == "admin":
        return JSONResponse(content={"message":"Unauthorized"}, status_code=401)
    else:
        deleted_product = ProductService().delete_product(product_data=product_data)
        return deleted_product

@products_router.post("/product_add_cart/", response_model=Product_Schema_cart, status_code=200)
def product_add_cart(product_data: Product_Schema_cart, current_user: User = Depends(get_current_user)):
    product = ProductService().product_add_cart(product_data=product_data, current_user=current_user)
    return JSONResponse(content={"message":"Product added to cart"}, status_code=200)   