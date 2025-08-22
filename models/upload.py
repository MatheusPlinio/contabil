from sqlalchemy import Column, Integer, Text, Date, DateTime, func
from database.config import Base


class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    date = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
