from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class ActiveSession(Base):
    __tablename__ = "active_sessions"

    id = Column(String, primary_key=True, index=True) # Using a separate UUID for the primary key
    device_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

