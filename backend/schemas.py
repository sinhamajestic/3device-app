from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Literal

class Device(BaseModel):
    device_id: str = Field(..., example="a7b2c3d4-e5f6-7890-1234-567890abcdef")

class ForceLogout(BaseModel):
    device_to_logout: str
    new_device_id: str

class ActiveSession(BaseModel):
    device_id: str
    user_id: str
    created_at: datetime
    last_seen: datetime

    class Config:
        orm_mode = True

class SessionLoginResponse(BaseModel):
    status: Literal["active", "limit_exceeded"]
    devices: List[ActiveSession]

class SessionStatus(BaseModel):
    status: Literal["active", "inactive"]

