from fastapi import FastAPI
from config.database import engine, Base
from routers.products import products_router
from routers.user import user_router
from routers.cart import cart_router


app = FastAPI()

app.title = "GalaxyStore_Backend"
app.version = "1.0" 


# Creación de la base de datos
Base.metadata.create_all(bind=engine)

# Inclusión de los routers
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(cart_router, prefix="/cart", tags=["My Cart"])
app.include_router(products_router, prefix="/store", tags=["Store"])



