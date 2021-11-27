from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, DateTime, Integer, Boolean, VARCHAR, BigInteger, ForeignKey, Sequence

Base = declarative_base()

class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    etag = Column(Text, nullable=False)
    
    video = relationship("Video")


class Channel(Base):
    __tablename__ = "channel"

    channel_id = Column(Text, primary_key=True)
    title = Column(Text, nullable=False)
    
    video = relationship("Video")
    
    
    
class Country(Base):
    __tablename__ = "country"

    country_id = Column(VARCHAR(length=2), primary_key=True)
    complete_name = Column(Text, nullable=False)
    
    video = relationship("Video")
    
    
    
class Time(Base):
    __tablename__ = "time"

    time_id = Column(Text, primary_key=True)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, nullable=False)
    
    
    
class Video(Base):
    __tablename__ = "video"

    video_id = Column(Text, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    view = Column(Integer, nullable=False)
    like = Column(Integer, nullable=False)
    dislike = Column(Integer, nullable=False)
    comments_count = Column(Integer)
    comments_disabled = Column(Boolean, nullable=False)
    ratings_disabled = Column(Boolean, nullable=False)
    video_error_or_removed = Column(Boolean, nullable=False)
    
    # Foreign keys
    category_id = Column(Integer, ForeignKey("category.category_id"))
    trending_date = Column(Text, ForeignKey("time.time_id"))
    publication_date = Column(Text, ForeignKey("time.time_id"))
    country_id = Column(VARCHAR(2), ForeignKey("country.country_id"))
    channel_id = Column(Text, ForeignKey("channel.channel_id"))
    tdr = relationship("Time", foreign_keys=[trending_date])
    pdr = relationship("Time", foreign_keys=[publication_date])
