from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse
from typing import Optional,List


class NoteCreate(BaseModel):
    title:str
    content:str


class NoteUpdate(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None

class NoteResponse(BaseModel):
    id:int
    title:str
    content:str
    owner:int
    uploadfile:Optional[int]=None
    created_at:datetime
    updated_at:datetime
    user:Optional[UserResponse]=None
        
    class Config:
        from_attributes=True

class PaginationResponse(BaseModel):
    page:int
    limit:int
    totalnote:int
    totalpages:int
    notes:List[NoteResponse]=None


        