from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.services.user import User_Services
from app.schemas.user import UserResponse,UserUpdate,PaginationResponse
from app.core.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.user import UserResponse


router=APIRouter(prefix="/user",tags=["User"])

@router.get("/me",response_model=UserResponse)
def myprofile(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return User_Services.me(db,current_user)

@router.put("/me",response_model=UserResponse)
def update(data:UserUpdate,db:Session=Depends(get_db),
             current_user:User=Depends(get_current_user)):
    return User_Services.modifyme(data,db,current_user)

@router.delete("/me")
def delete(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return User_Services.deleteme(db,current_user)

@router.get("",response_model=PaginationResponse)
def alluser(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return User_Services.all(db,current_user)

