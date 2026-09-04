from fastapi import APIRouter,Depends,File,UploadFile
from app.services.uploads import Uploads_Services
from sqlalchemy.orm import Session
from app.core.database import get_db
from typing import List
from app.models.user import User
from app.dependencies.auth  import get_current_user




router=APIRouter(prefix="/uploads",tags=["UploadFileNote"])


@router.post("/{note_id}")
async def file(note_id:int,file:UploadFile=File(...),
         current_user:User=Depends(get_current_user),
         db:Session=Depends(get_db)):
    return await Uploads_Services.uploadfile(note_id,db,current_user,file)

@router.get("/{note_id}")
def show(note_id:int,db:Session=Depends(get_db),
         current_user:User=Depends(get_current_user)
         ):
    return Uploads_Services.getfileuploads(note_id,db,current_user)

@router.delete("/{note_id}")
def show(note_id:int,db:Session=Depends(get_db),
         current_user:User=Depends(get_current_user)):
    return Uploads_Services.deleteuploads(note_id,db,current_user)

