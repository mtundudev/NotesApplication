from app.core.database import Base
from sqlalchemy import String,Column,Integer,DateTime,Enum,Boolean
import enum
from sqlalchemy.orm import relationship
from datetime import datetime

class UserRole(str,enum.Enum):
    admin="ADMIN"
    user="USER"

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    role=Column(Enum(UserRole ,native_enum=False),default=UserRole.user,nullable=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.now)
    updated_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    
    
    note=relationship("Note",back_populates="user",cascade="all, delete-orphan")
    media=relationship("Media",back_populates="user",cascade="all, delete-orphan")