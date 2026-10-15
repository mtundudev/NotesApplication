from app.core.security import decode_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.models.user import User

from app.core.database import get_db

oauth2_schema=OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token:str=Depends(oauth2_schema),db:Session=Depends(get_db)):
    payload=decode_token(token)
    email=payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token has no user info")
    user=db.query(User).filter(User.email==email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    return user
        