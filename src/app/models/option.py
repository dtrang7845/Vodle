from sqlmodel import Column,Integer,String,ForeignKey

from sqlmodel.orm import relationship
from app.core.database import Base

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer,primary_key = True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    option_text = Column(String,nullable = False)

    question = relationship("Question",back_populates = "options")
    votes = relationship("Vote",back_populates = "option")
