from fastapi import APIRouter,Depends
from app.services.note_services import Note_Services
from app.schemas.note import NoteCreate,NoteResponse,NoteUpdate,PaginationResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user

router=APIRouter(prefix="/note",tags=["Note"])


@router.post("",response_model=NoteResponse)
def Create(data:NoteCreate,db:Session=Depends(get_db),
           current_user:User=Depends(get_current_user)):
    return Note_Services.create_note(data,db,current_user)

@router.get("/notes",response_model=PaginationResponse)
def show_all(db:Session=Depends(get_db),
            page:int=1,limit:int=10,search:str=None,sort:str="desc",
             current_user:User=Depends(get_current_user)):
    return Note_Services.get_notes(db,current_user,page,limit,search,sort)

@router.get("/{note_id}",response_model=NoteResponse)
def singe_note(note_id:int,db:Session=Depends(get_db),
               current_user:User=Depends(get_current_user)):
    return Note_Services.note_by_id(note_id,db,current_user)

@router.put("/{note_id}",response_model=NoteResponse)
def update(note_id:int,data:NoteUpdate,db:Session=Depends(get_db),
           current_user:User=Depends(get_current_user)):
    return Note_Services.modify_note(note_id,data,db,current_user)

@router.delete("/{note_ib}")
def Create(note_id:int,db:Session=Depends(get_db),
           current_user:User=Depends(get_current_user)):
    return Note_Services.delete_note(note_id,db,current_user)
