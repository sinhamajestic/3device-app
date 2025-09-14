from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class User(BaseModel):
    full_name: str
    phone_number: str

class Device(BaseModel):
    device_id: str

class ForceLogout(BaseModel):
    device_to_logout: str
    new_device_id: str

class ActiveSession(BaseModel):
    id: str
    user_id: str
    device_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SessionLoginResponse(BaseModel):
    status: str  # "active" or "limit_exceeded"
    devices: List[ActiveSession] = []

class SessionStatus(BaseModel):
    status: str # "active" or "inactive"