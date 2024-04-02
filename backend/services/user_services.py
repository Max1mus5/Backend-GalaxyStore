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
  
  def login_user(self, user_data):
    db = Session()
    try:
      user = db.query(User).filter(User.username == user_data.username).first()
      if not user:
        raise HTTPException(status_code=404, detail="User not found")
      if user.hashed_password != self.hashed_password(user_data.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
      return True
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
    finally:
      db.close()
    
  def delete_user(self, user_id):
    db = Session()
    try:
      user = db.query(User).filter(User.id == user_id).first()
      if not user:
        raise HTTPException(status_code=404, detail="User not found")
      db.delete(user)
      db.commit()
      return True
    except Exception as e:
      db.rollback()
      raise HTTPException(status_code=400, detail=str(e))
    finally:
      db.close()
  def update_user(self, user_data, user_id):
    db = Session()
    try:
      user = db.query(User).filter(User.id == user_id).first()
      if not user:
        raise HTTPException(status_code=404, detail="User not found")
      user.username = user_data.username
      user.email = user_data.email
      user.hashed_password = self.hashed_password(user_data.hashed_password)
      db.commit()
      db.refresh(user)
      return user
    except Exception as e:
      db.rollback()
      raise HTTPException(status_code=400, detail=str(e))
    finally:
      db.close()
  