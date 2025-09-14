from sqlalchemy.orm import Session
from datetime import datetime
import uuid

# Changed from relative to absolute imports
import models
import schemas

def get_active_sessions_for_user(db: Session, user_id: str):
    return db.query(models.ActiveSession).filter(models.ActiveSession.user_id == user_id).all()

def create_user_session(db: Session, user_id: str, device_id: str):
    db_session = models.ActiveSession(
        id=str(uuid.uuid4()),
        user_id=user_id,
        device_id=device_id,
        created_at=datetime.utcnow()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def delete_session_by_device_id(db: Session, device_id: str):
    session = db.query(models.ActiveSession).filter(models.ActiveSession.device_id == device_id).first()
    if session:
        db.delete(session)
        db.commit()
    return

def get_session_by_device_id(db: Session, device_id: str):
    return db.query(models.ActiveSession).filter(models.ActiveSession.device_id == device_id).first()

def update_session_last_seen(db: Session, device_id: str):
    session = db.query(models.ActiveSession).filter(models.ActiveSession.device_id == device_id).first()
    if session:
        session.created_at = datetime.utcnow() # Treat created_at as last_seen
        db.commit()
    return