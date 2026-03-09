from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    status = Column(String)
    description = Column(String)
    match_score = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")