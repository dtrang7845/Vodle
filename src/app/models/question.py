import enum
from sqlmodel import Column,Integer,String, Enum
from sqlmodel.orm import relationship
from app.core.database import Base

class QuestionType(str,enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_SELECT = "multiple_select"
    TRUE_FALSE = "true_false"

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer,primary_key = True)
    date_id = Column(Integer,nullable = False,index = True, unique = True)
    question_content = Column(String,nullable = False)
    question_type = Column(Enum(QuestionType),nullable = False)

    options = relationship("Option",back_populates = "question")
    votes = relationship("Vote", back_populates ="question")
   
