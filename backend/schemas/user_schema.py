from pydantic import BaseModel

class User(BaseModel): #User schema for registering a new user
    username: str
    email: str
    hashed_password: str


#User schema for login
class UserS(BaseModel):
    username: str
    password: str