from sqlmodel import Column,Integer,ForeignKey,DateTime
from datetime import datetime
from sqlmodel.orm import relationship
from app.core.database import Base

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey("users.id"))
    question_id = Column(Integer,ForeignKey("questions.id"))
    option_id = Column(Integer,ForeignKey("options.id"))
    create_time = Column(DateTime,datetime.utcnow)

    vote_choices = relationship("Vote Choices",back_populate = "vote")
    user = relationship("User",back_populate ="votes")
    question = relationship("Question",back_populate = "votes")
