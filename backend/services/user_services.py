from fastapi import HTTPException
from config.database import Session
from models.user_model import User
import hashlib #metodo de encriptacion  


class UserService:
  def create_user(self, user_data):
    db = Session()
    try:
      user = User(username=user_data.username, email=user_data.email, hashed_password=self.hashed_password(user_data.hashed_password))
      db.add(user)
      db.commit()
      db.refresh(user)
      db.close()
      return user
    except Exception as e:
      db.rollback()
      db.close()
      raise HTTPException(status_code=400, detail=str(e))
    
  def hashed_password(self, password):
    combined_string = f"{password}"
    password = hashlib.sha256(combined_string.encode()).hexdigest()
    return password