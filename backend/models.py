from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

# Changed from relative to absolute import
from database import Base

class ActiveSession(Base):
    __tablename__ = "active_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    device_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False)