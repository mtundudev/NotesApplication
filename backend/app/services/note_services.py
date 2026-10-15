from app.schemas.note import NoteCreate,NoteUpdate
from sqlalchemy.orm import Session
from app.models.user import UserRole
from app.models.notes import Note
from fastapi import HTTPException,status,Query
from sqlalchemy import or_,asc,desc
import math

class Note_Services():
    @staticmethod
    def create_note(data:NoteCreate,db:Session,current_user):
        note=Note(
            title=data.title,
            content=data.content,
            owner=current_user.id
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        
        return note
    
    @staticmethod
    def get_notes(db:Session,current_user,page:int=Query(1 ,ge=1),limit:int=Query(10,ge=10,le=100),search:str=None,sort:str="desc"):
        note=db.query(Note).filter(Note.owner==current_user.id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detsil="note not found")
            
        if search:
            note=note.filter(or_(
                Note.title.ilike(f"%{search}%"),
                Note.content.ilike(f"%{search}%")
            ))
        if sort:
            if sort=="title":
                note=note.order_by(asc(Note.title))
            else:
                note=note.order_by(desc(Note.title))
        else:
             
            if sort=="created_at":
                note=note.order_by(asc(Note.created_at))
            else:
                note=note.order_by(desc(Note.created_at))
        totalnote=note.count()        
        totalpages=math.ceil(page/limit)
        skip=(page-1)*limit
        note=note.offset(skip).limit(limit).all()
                    
        return {
            "page":page,
            "limit":limit,
            "totalnote":totalnote,
            "totalpages":totalpages,
            "notes":note
        }
    
    @staticmethod
    def note_by_id(note_id:int,db:Session,current_user):
        note=db.query(Note).filter(Note.id==note_id).first()
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="note not found")
        if note.owner != current_user.id and current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" your note not found")
            
        return note
    
    @staticmethod
    def modify_note(note_id,data:NoteUpdate,db:Session,current_user):
        note=db.query(Note).filter(Note.id==note_id).first()
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="note not found")
        if note.owner != current_user.id and current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="note not found")
                    
        if data.title:
            note.title=data.title
        if data.content:
             note.content=data.content   
        
        db.commit()     
        db.refresh(note)
        
        return note
    
    @staticmethod
    def delete_note(note_id:int,db:Session,current_user):
        note=db.query(Note).filter(Note.id==note_id).first()
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="note not found")
        if note.owner != current_user.id or current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="note not found")
                    
        db.delete(note)
        db.commit()
        
        return {
            "message":"note is successful deleted"
        }
        
