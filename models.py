from sqlalchemy import Column, Integer, String, Boolean, Date, Time, ForeignKey, DateTime
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

# Tables
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    location = Column(String)
    event_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    category = Column(String, nullable=False)
    max_attendees = Column(Integer)
    status = Column(String, default="Upcoming")
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="events")
        
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    
    events = relationship("Event", back_populates="owner")