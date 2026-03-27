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

    status = Column(String, default="Wishlist")  
    

    total_seasons = Column(Integer, nullable=True)
    seasons_watched = Column(Integer, default=0)

    rating = Column(Integer, nullable=True)
    review = Column(String, nullable=True)

    poster_url = Column(String, nullable=True)

   
  