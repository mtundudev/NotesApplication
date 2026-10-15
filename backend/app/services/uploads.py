from sqlalchemy.orm import Session
from app.models.notes import Note
from app.models.media import Media
from fastapi import HTTPException,status,File,UploadFile
from pathlib import Path
from app.models.user import UserRole
from uuid import uuid4

class Uploads_Services():
    @staticmethod
    async def uploadfile(note_id:int,db:Session,current_user,file:UploadFile=File(...)):
        upload=db.query(Note).filter(Note.id==note_id).first()
        if not upload:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="note not found")
       
        if upload.owner != current_user.id and current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" your note not found")
                                          
        ALLOWED_EXTENSION=(
            ".png",".jpg","jpeg",".pdf"
        )
        if not file.content_type:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="check your uploaded file")
            
        extension=Path(file.filename).suffix.lower()
        if extension not in ALLOWED_EXTENSION:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="check your file ")
        
        elif extension == ".pdf":
            UPLOAD_DIR=Path("storage/pdf")
            UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
        else:
            UPLOAD_DIR=Path("storage/image")
            UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
                
        new_filename=f"{uuid4()}{extension}"

        file_path=UPLOAD_DIR/new_filename
        
        with open(file_path ,"wb") as buffer:
            buffer.write(await file.read())
            
        media=db.query(Media).filter(Media.id==upload.uploadfile).first()
        if media:
            media.file_path=str(file_path)
            media.new_filename=new_filename
            media.filename=file.filename
            media.mime_type=file.content_type
        else:
            media=Media(
                file_path=str(file_path),
                new_filename=new_filename,
                filename=file.filename,
                uploaded_by=current_user.id,
                mime_type=file.content_type
            )
            db.add(media)
            db.flush()
            
            upload.uploadfile=media.id
            db.commit()
            db.refresh(upload)
            
        db.commit()    
        db.refresh(media)
        return media
    
    @staticmethod
    def getfileuploads(note_id:int,db:Session,current_user):
        note = db.query(Note).filter(Note.id==note_id).first()
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="note not found")
        if note.owner != current_user.id and current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" your note not found")
        media=db.query(Media).filter(Media.id==note.uploadfile).first()
                             
        if not media:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="note has no uploaded file")
                
        return media   
    
    @staticmethod
    def deleteuploads(note_id:int,db:Session,current_user):
        note = db.query(Note).filter(Note.id==note_id).first()
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="note not found")
        
        if note.owner != current_user.id and current_user.role != UserRole.admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" your note not found")
        
        media=db.query(Media).filter(Media.id==note.uploadfile).first()                   
        if not media:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="note has no uploaded file")
        db.delete(media)
        db.commit()
        
        return{
            "message":" file succesful removed"
        }