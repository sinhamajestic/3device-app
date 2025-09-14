from sqlalchemy import Column, String, DateTime
import uuid
from datetime import datetime, timezone

from database import Base
class ActiveSession(Base):
    __tablename__ = "active_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    device_id = Column(String, nullable=False)
    # This now uses the modern, timezone-aware method to avoid deprecation warnings.
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))