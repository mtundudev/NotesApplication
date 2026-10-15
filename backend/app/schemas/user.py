from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime
from typing import Optional,List
from app.models.user import UserRole



class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserUpdate(BaseModel):
    name:Optional[str]=None
    email:Optional[EmailStr]=None
  

class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    role:UserRole
    is_active:bool
    created_at:datetime
    updated_at:datetime
    
    
    model_config=ConfigDict(
        from_attributes=True
    )
class PaginationResponse(BaseModel):
    page:int
    limit:int
    totaluser:int
    totalpages:int
    users:List[UserResponse]=None


    
        