from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.services.auth_services import Auth_Services
from app.schemas.user import UserCreate,UserResponse
from app.core.database import get_db
from typing import List
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.auth import get_current_user
from app.schemas.user import UserResponse


router=APIRouter(prefix="/auth",tags=["Athentication"])


@router.post("",response_model=UserResponse)
def create(data:UserCreate,db:Session=Depends(get_db)):
    return Auth_Services.create_user(data,db)


@router.post("/login")
def login(data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    return Auth_Services.login(data.username,data.password,db)



