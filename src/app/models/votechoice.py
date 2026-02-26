from sqlmodel import Column,Integer,ForeignKey
from sqlmodel.orm import relationship
from app.core.database import Base

class VoteChoice(Base):
    __tablename__ = "vote_choices"
    vote_id = Column(Integer,ForeignKey("votes.vote_id",ondelete="CASCADE"),
    primary_key = True                 
    )
    option_id = Column(Integer,ForeignKey("options.option_id",ondelete="CASCADE"),
    primary_key = True                 
    )

    vote = relationship("Vote",back_populates="vote_choices")
    option = relationship("Option",back_populates = "vote_choices")