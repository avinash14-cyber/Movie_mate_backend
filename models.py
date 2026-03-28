from sqlalchemy import Column, Integer, String
from database import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    genre = Column(String)
    platform = Column(String)

    type = Column(String, nullable=False)  
    # "movie" or "series"
    description = Column(String, nullable=True)
    status = Column(String, default="Not watched") 
    

    total_seasons = Column(Integer, nullable=True)
   

    rating = Column(Integer, nullable=True)
    

    poster_url = Column(String, nullable=True)

   
  