from app.schemas.user import UserCreate,UserUpdate
from app.models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.core.security import hash_password,verify_password,create_acess_token


class Auth_Services():
    @staticmethod
    def create_user(data:UserCreate,db:Session):
        existing=db.query(User).filter(User.email==data.email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="email alredy exist")
        user=User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password)
            
        )   
        db.add(user)
        db.commit()
        db.refresh(user)
    
        return user

    @staticmethod
    def login(email:str,password:str,db:Session):
        user=db.query(User).filter(User.email==email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="please check to your email")
        if  not verify_password(password,user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="please check to your pasword")
        token  = create_acess_token({"sub":user.email})
    
        return {
            "access_token":token,
            "token_type":"Bearer"
        }

 
    