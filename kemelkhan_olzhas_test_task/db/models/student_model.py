from sqlalchemy import Column, Integer, String
from db.database import Base

class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    score = Column(Integer, default=None, index=True)
