from app.core.database import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship 
from datetime import datetime


class Media(Base):
    __tablename__="uploads"
    
    id=Column(Integer,primary_key=True,index= True)
    uploaded_by=Column(Integer,ForeignKey("users.id"))
    filename=Column(String,nullable=False)
    new_filename=Column(String,nullable=False)
    file_path=Column(String,nullable=False)
    mime_type=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.now)
    updated_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    
    user=relationship("User",back_populates="media")
    note=relationship("Note",back_populates="media")
    