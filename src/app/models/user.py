from sqlmodel import Column,Integer,String,DateTime
from datetime import datetime
from sqlmodel.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True,index = True)
    name = Column(String, nullable = False)
    username  = Column(String, nullable = False, unique = True, index = True)
    email = Column(String, nullable = False, unique = True)
    password_hash = Column(String, nullable = False)
    create_time = Column(DateTime, datetime.utcnow)

    votes = relationship("Vote", back_populates="user")
