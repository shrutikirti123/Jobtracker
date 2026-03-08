from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    status = Column(String)
    description = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")