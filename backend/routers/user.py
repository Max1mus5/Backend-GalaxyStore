from fastapi import APIRouter, Depends
from schemas.user_schema import User as UserSchema
from services.user_services import UserService
from fastapi.responses import JSONResponse
from schemas.user_schema import UserS
from utils.jwt_manager import create_token
from utils.getUser import get_current_user
from models.user_model import User


user_router = APIRouter()

@user_router.post("/create_user/", response_model=UserSchema, status_code=200)
def create_user(user_data: UserSchema):
    newUser= UserService().create_user(user_data=user_data)
    try:
        return newUser
    except Exception as e:
        return e
    
@user_router.post("/login/", response_model=dict, status_code=200)
def login(user: UserS):
    
    if UserService().login_user(user_data=user):
        token = create_token(data=user.model_dump())
        result = JSONResponse(content={"token": token},status_code=200)

    else:
        result = JSONResponse(content={"message":"Invalid credentials"}, status_code=401)
    return result

@user_router.delete("/delete_user/", response_model=dict, status_code=200)
def delete_user(current_user: User = Depends(get_current_user)):
    if UserService().delete_user(current_user.id):
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}

@user_router.put("/update_user/", status_code=200)
def update_user(user_data: UserSchema, current_user: User = Depends(get_current_user)):
    updated_user = UserService().update_user(user_data=user_data, user_id=current_user.id)
    try:
        return JSONResponse(content={"message":"User updated successfully actual user: "+str(updated_user.username)+" Please Login Again and validate new token"}, status_code=200)
    except Exception as e:
        return e
    