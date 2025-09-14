from sqlalchemy.orm import Session
from . import models
import uuid

def get_session_by_device_id(db: Session, device_id: str):
    return db.query(models.ActiveSession).filter(models.ActiveSession.device_id == device_id).first()

def get_active_sessions_for_user(db: Session, user_id: str):
    return db.query(models.ActiveSession).filter(models.ActiveSession.user_id == user_id).order_by(models.ActiveSession.created_at).all()

def create_user_session(db: Session, user_id: str, device_id: str):
    db_session = models.ActiveSession(id=str(uuid.uuid4()), user_id=user_id, device_id=device_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def delete_session_by_device_id(db: Session, device_id: str):
    db_session = get_session_by_device_id(db, device_id)
    if db_session:
        db.delete(db_session)
        db.commit()
    return db_session

def update_session_last_seen(db: Session, device_id: str):
    db_session = get_session_by_device_id(db, device_id)
    if db_session:
        db.commit() # onupdate=func.now() handles the timestamp update automatically
    return db_session

