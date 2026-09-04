from pwdlib import PasswordHash
from datetime import datetime,timedelta
from app.core.config import settings
from jose import jwt,JWTError


password_hash=PasswordHash.recommended()


def hash_password(password):
    return password_hash.hash(password)

def verify_password(Plain_password,hashed_password):
    return password_hash.verify(Plain_password,hashed_password)

#=======token+++++access==================
def create_acess_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now() + timedelta(minutes=settings.EXPIRE_ACCESS_TOKEN)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return token

def decode_token(token:str):
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise ValueError
        
        

    
    