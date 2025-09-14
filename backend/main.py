import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud
import models
import schemas
import auth
from database import SessionLocal, engine
from config import settings

# This line ensures that a .env file is loaded if present
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="N-Device Login API",
    description="API for managing user sessions with an N-device limit.",
    version="1.0.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "https://3device-app.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Health"])
def read_root():
    """Health check endpoint."""
    return {"status": "API is running"}

@app.post("/api/v1/sessions/login", response_model=schemas.SessionLoginResponse, tags=["Sessions"])
async def login_session(
    session_data: schemas.Device,
    db: Session = Depends(get_db),
    token: str = Depends(auth.verify_token),
):
    """
    Handles a user login attempt from a new device.
    Checks if the number of active sessions is below the limit.
    """
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user information in token")

    active_sessions = crud.get_active_sessions_for_user(db, user_id=user_id)
    
    # Check if the current device is already registered
    is_existing_device = any(s.device_id == session_data.device_id for s in active_sessions)
    if is_existing_device:
        crud.update_session_last_seen(db, device_id=session_data.device_id)
        return schemas.SessionLoginResponse(status="active", devices=[])

    # If new device and limit reached
    if len(active_sessions) >= settings.MAX_SESSIONS:
        logger.info(f"Session limit reached for user {user_id}")
        return schemas.SessionLoginResponse(
            status="limit_exceeded",
            devices=[schemas.ActiveSession.from_orm(s) for s in active_sessions]
        )
    
    # If limit not reached, create a new session
    crud.create_user_session(db=db, user_id=user_id, device_id=session_data.device_id)
    logger.info(f"New session created for user {user_id} on device {session_data.device_id}")
    return schemas.SessionLoginResponse(status="active", devices=[])


@app.post("/api/v1/sessions/force-logout", response_model=schemas.SessionStatus, tags=["Sessions"])
async def force_logout_and_login(
    force_logout_data: schemas.ForceLogout,
    db: Session = Depends(get_db),
    token: str = Depends(auth.verify_token),
):
    """
    Forcefully logs out an old device to make space for a new one.
    """
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user information in token")

    # Ensure the device being logged out belongs to the user
    session_to_delete = crud.get_session_by_device_id(db, force_logout_data.device_to_logout)
    if not session_to_delete or session_to_delete.user_id != user_id:
        raise HTTPException(status_code=403, detail="Device does not belong to the current user")

    crud.delete_session_by_device_id(db, device_id=force_logout_data.device_to_logout)
    logger.info(f"Forcefully logged out device {force_logout_data.device_to_logout} for user {user_id}")
    
    crud.create_user_session(db=db, user_id=user_id, device_id=force_logout_data.new_device_id)
    logger.info(f"New session created for user {user_id} on device {force_logout_data.new_device_id}")
    
    return schemas.SessionStatus(status="active")


@app.post("/api/v1/sessions/heartbeat", response_model=schemas.SessionStatus, tags=["Sessions"])
async def session_heartbeat(
    device: schemas.Device,
    db: Session = Depends(get_db),
    token: str = Depends(auth.verify_token),
):
    """
    Periodically checked by the frontend to ensure the session is still valid.
    """
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user information in token")

    session = crud.get_session_by_device_id(db, device.device_id)

    if session and session.user_id == user_id:
        crud.update_session_last_seen(db, device.device_id)
        return schemas.SessionStatus(status="active")
    
    logger.warning(f"Heartbeat failed for user {user_id} on non-existent device {device.device_id}")
    return schemas.SessionStatus(status="inactive")


@app.post("/api/v1/sessions/logout", status_code=204, tags=["Sessions"])
async def logout_session(
    device: schemas.Device,
    db: Session = Depends(get_db),
    token: str = Depends(auth.verify_token),
):
    """
    Logs out a specific device.
    """
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user information in token")
    
    session_to_delete = crud.get_session_by_device_id(db, device.device_id)
    if session_to_delete and session_to_delete.user_id == user_id:
        crud.delete_session_by_device_id(db, device_id=device.device_id)
        logger.info(f"User {user_id} logged out from device {device.device_id}")
    
    return

@app.get("/api/v1/user/profile", response_model=schemas.User, tags=["User"])
async def get_user_profile(token: dict = Depends(auth.verify_token)):
    """
    Retrieves the user's full name and phone number from the JWT.
    This requires setting up a custom claim in Auth0.
    """
    return {
        "full_name": token.get("name", "N/A"),
        "phone_number": token.get("https://3device-app.com/phone_number", "Not Provided")
    }
