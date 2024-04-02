from middlewares.authMiddleware import JWTBearer
from models.user_model import User
from fastapi import Depends

async def get_current_user(user: User = Depends(JWTBearer())):
    return user