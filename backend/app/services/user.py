from app.schemas.user import UserUpdate
from app.models.user import User,UserRole
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Query
from sqlalchemy import asc,desc
import math

class User_Services():
    @staticmethod
    def me(db:Session,current_user):
        user=db.query(User).filter(User.id==current_user.id).first()
        return user
    
    @staticmethod
    def modifyme(data:UserUpdate,db:Session,current_user):
        user=db.query(User).filter(User.id==current_user.id).first()
        if not user:
            return None
        if data.email:
            user.email=data.email
        if data.name:    
            user.name=data.name
            
        db.commit()    
        db.refresh(user)
        return user
    
    @staticmethod
    def deleteme(db:Session,current_user):
        user=db.query(User).filter(User.id==current_user.id).first()
        db.delete(user)
        db.commit()
        return{
            "message":"you have been removed with all of your related info"
        }
            
    @staticmethod
    def all(db:Session,current_user,page:int=1,limit:int=10,search:str=None,sort:str="desc"):
        user=db.query(User)
        if current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="access denied")
            
        if search:
            user=user.filter(
                User.name.ilike(f"%{search}%")
            )
        if sort:
            if sort=="name":
                user=user.order_by(asc(User.name))
            else:
                user=user.order_by(desc(User.name))
        else:
             
            if sort=="created_at":
                user=user.order_by(asc(User.created_at))
            else:
                user=user.order_by(desc(User.created_at))
                
        totaluser=user.count()        
        totalpages=math.ceil(page/limit)
        skip=(page-1)*limit
        user=user.offset(skip).limit(limit).all()
                    
        return {
            "page":page,
            "limit":limit,
            "totaluser":totaluser,
            "totalpages":totalpages,
            "users":user
        }
            