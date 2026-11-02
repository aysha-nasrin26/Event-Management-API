from pydantic import BaseModel
from datetime import date, time

class EventBase(BaseModel):
    title: str
    description: str | None = None
class EventCreate(EventBase):
    location: str
    event_date: date
    start_time: time
    end_time: time
    category: str
    max_attendees: int
class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    event_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    category: str | None = None
    max_attendees: int | None = None
class Event(BaseModel):
    id: int
    title: str
    description: str | None = None
    location: str
    event_date: date
    start_time: time
    end_time: time
    category: str
    max_attendees: int
    status: str
    user_id: int

    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class Config:
    from_attributes = True
    
class UserLogin(BaseModel):
    email: str
    password: str
    
class UserBasic(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
        
class AIDescriptionRequest(BaseModel):
    title: str
    category: str
    audience: str
    location: str
    event_date: date