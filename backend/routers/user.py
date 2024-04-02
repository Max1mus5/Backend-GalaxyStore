from fastapi import APIRouter
from schemas.user_schema import User
from services.user_services import UserService

user_router = APIRouter()

@user_router.post("/create_user/", response_model=User, status_code=200)
def create_user(user_data: User):
    newUser= UserService().create_user(user_data=user_data)
    try:
        return newUser
    except Exception as e:
        return e
    
