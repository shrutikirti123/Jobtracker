from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    skills = Column(String)

    jobs = relationship("Job", back_populates="user")