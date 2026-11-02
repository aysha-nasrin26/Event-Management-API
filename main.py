from multiprocessing import get_context

from fastapi import FastAPI, Depends, HTTPException
from schemas import Event as Eventschema, EventCreate, EventUpdate
from schemas import UserCreate, UserResponse, UserLogin
from sqlalchemy.orm import session
from database import session_local, Base, engine
from models import Event, User
from security import pwd_context, create_access_token, verify_token, hash_password
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from schemas import AIDescriptionRequest
from services.ai_services import generate_event_description

Base.metadata.create_all(bind=engine)
app = FastAPI()

#dependency for db session
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
#Bearer token
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload
@app.get("/protected")
def protected_route(
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": "You can access this route",
        "user": current_user
    }

#Authorization check
def get_event_owner(event_id: int,current_user: dict,db: session):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )
    if event.user_id != int(current_user["sub"]):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to modify this event"
        )
    return event
    
#POST - Register User
@app.post("/users/register", response_model=UserResponse)
def register_user(user: UserCreate,db: session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")    
    hashed_password = hash_password(user.password)
    
    db_user = User(
    name=user.name,
    email=user.email,
    password_hash=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# POST - User Login
@app.post("/users/login")
def user_login(user: UserLogin, db: session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    if pwd_context.verify(
        user.password,
        existing_user.password_hash
    ):
        token_data = {
            "sub": str(existing_user.id),
            "email": existing_user.email
        }
        access_token = create_access_token(token_data)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=401,
        detail="Incorrect password"
    )
       
# POST - Create Event
@app.post("/events", response_model=Eventschema)
def create(event: EventCreate,db: session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = int(current_user["sub"])
    if not event.description:
        generated_description = generate_event_description(
            event.title,
            event.category,
            "General Audience",
            event.location,
            str(event.event_date)
        )
        if generated_description is None:
            raise HTTPException(
                status_code=503,
                detail="AI description service is temporarily unavailable"
            )
        event.description = generated_description
    db_event = Event(**event.model_dump(), user_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

#GET - ALL events
@app.get("/events",response_model=list[Eventschema])
def read_events(db: session = Depends(get_db)):
    return db.query(Event).all()
@app.get("/events")
def get_events(category: str | None = None,location: str | None = None,skip: int = 0,limit:int = 10,db: session = Depends(get_db)):
    query = db.query(Event)
    if category:
        query = query.filter(Event.category == category)
    if location:
        query = query.filter(Event.location == location)
    return query.offset(skip).limit(limit).all()

#GET - single event
@app.get("/events/{event_id}",response_model=Eventschema)
def read_event(event_id: int, db: session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first() #Table filter even_id
    if not event:
        raise HTTPException(status_code=404, detail="Event Not Found")
    print(event.owner.name)
    print(event.owner.email)
    return event

#GET - particular user
@app.get("/users/me/events", response_model=list[Eventschema])
def get_my_events(
    db: session = Depends(get_db),
    current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["sub"])
    events = db.query(Event).filter(Event.user_id == user_id).all()
    return events

#PUT - Update event
@app.put("/events/{event_id}",response_model=Eventschema)
def update_event(event_id: int, updated:EventCreate, db: session = Depends(get_db),
                 current_user: dict = Depends(get_current_user)):
    event = get_event_owner(event_id,current_user,db)
    
    for key, value in updated.dict().items():
        setattr(event, key, value)
        
    db.commit()
    db.refresh(event)
    return event

#PATCH - update single 
@app.patch("/events/{event_id}", response_model=Eventschema)
def update_single(event_id: int, event:EventUpdate, db: session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)):
    db_event = get_event_owner(event_id,current_user,db)
    update_data = event.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

#DELETE - delete event
@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: session = Depends(get_db),
                 current_user: dict = Depends(get_current_user)):
    event = get_event_owner(event_id,current_user,db)
    db.delete(event)
    db.commit()
    return{"message" : "Event deleted successfully!"}

#AI -generate description
@app.post("/ai/generate-description")
def generate_description(data: AIDescriptionRequest,
    current_user: dict = Depends(get_current_user)):

    description = generate_event_description(
        data.title,
        data.category,
        data.audience,
        data.location,
        data.event_date
)
    return {
        "description": description
    }