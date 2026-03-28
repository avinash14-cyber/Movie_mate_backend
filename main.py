from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Media
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Dependency (DB session)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Backend running"}


# 🔹 Schema
class MediaCreate(BaseModel):
    title: str
    genre: str
    platform: str
    type: str
    description: Optional[str] = None
    total_seasons: Optional[int] = None
    poster_url: Optional[str] = None




class ProgressUpdate(BaseModel):
    status: str
     

class RatingUpdate(BaseModel):
    rating: int
       


# 🔹 POST API
@app.post("/media")
def create_media(media: MediaCreate, db: Session = Depends(get_db)):
    new_media = Media(
        title=media.title,
        genre=media.genre,
        platform=media.platform,
        type=media.type,
        description=media.description,
        total_seasons=media.total_seasons,
        poster_url=media.poster_url
    )
    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    return new_media


# 🔹 GET API
@app.get("/media")
def get_all_media(type: str = None,db: Session = Depends(get_db)):
    query = db.query(Media)

    if type:
        query = query.filter(Media.type == type)

    return query.all()

# updating progres

@app.put("/media/{id}/progress")
def update_progress(id: int, data: ProgressUpdate, db: Session = Depends(get_db)):

    media = db.query(Media).filter(Media.id == id).first()

    if not media:
        return {"error": "Media not found"}

    media.status = data.status

    

    db.commit()
    db.refresh(media)

    return media



@app.put("/media/{id}/rating")
def update_rating(id: int, data: RatingUpdate, db: Session = Depends(get_db)):

    media = db.query(Media).filter(Media.id == id).first()

    if not media:
        return {"error": "Media not found"}

    if media.status != "Watched":
        return {"error": "Can only rate completed media"}

    media.rating = data.rating
    

    db.commit()
    db.refresh(media)

    return media



@app.delete("/media/{id}")
def delete_media(id: int, db: Session = Depends(get_db)):

    media = db.query(Media).filter(Media.id == id).first()

    if not media:
        return {"error": "Media not found"}

    db.delete(media)
    db.commit()

    return {"message": "Media deleted successfully"}