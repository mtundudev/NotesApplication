from app.core.database import Base
from sqlalchemy import Column,Integer,String,DateTime,Text,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime



class Note(Base):
    __tablename__="notes"
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=True)
    content=Column(Text)
    uploadfile=Column(Integer,ForeignKey("uploads.id"))
    owner=Column(Integer,ForeignKey("users.id"))
    created_at=Column(DateTime,default=datetime.now)
    updated_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    
    
    user=relationship("User",back_populates="note")
    media=relationship("Media",back_populates="note")