from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Many-to-many relationship tables
monument_tag = Table(
    'monument_tag',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.tag_id'), primary_key=True),
    Column('monument_id', Integer, ForeignKey('monument.monument_id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    location = Column(String(255))
    
    # Relationships
    preferences = relationship("UserPreference", back_populates="user")
    bookmarks = relationship("Bookmarks", back_populates="user")
    visited_monuments = relationship("UserVisitedMonument", back_populates="user")

class UserPreference(Base):
    __tablename__ = 'user_preference'
    
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.tag_id'))
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    tag = relationship("Tag")

class Tag(Base):
    __tablename__ = 'tag'
    
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String(255), nullable=False, unique=True)
    
    # Relationships
    monuments = relationship("Monument", secondary=monument_tag, back_populates="tags")

class Monument(Base):
    __tablename__ = 'monument'
    
    monument_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    popularity = Column(Float, nullable=False)
    indoor = Column(Boolean, default=False)
    
    # Relationships
    tags = relationship("Tag", secondary=monument_tag, back_populates="monuments")
    monument_events = relationship("MonumentEvent", back_populates="monument")
    slots = relationship("MonumentSlot", back_populates="monument")
    bookmarks = relationship("Bookmarks", back_populates="monument")
    visited_by = relationship("UserVisitedMonument", back_populates="monument")

class MonumentEvent(Base):
    __tablename__ = 'monument_event'
    
    monument_id = Column(Integer, ForeignKey('monument.monument_id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('event.event_id'), primary_key=True)
    name = Column(String(255))
    
    # Relationships
    monument = relationship("Monument", back_populates="monument_events")
    event = relationship("Event", back_populates="monument_events")

class Event(Base):
    __tablename__ = 'event'
    
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    related_type = Column(String(255))
    
    # Relationships
    monument_events = relationship("MonumentEvent", back_populates="event")

class MonumentSlot(Base):
    __tablename__ = 'monument_slot'
    
    monument_id = Column(Integer, ForeignKey('monument.monument_id'), primary_key=True)
    slot_id = Column(Integer, ForeignKey('day_slot.slot_id'), primary_key=True)
    
    # Relationships
    monument = relationship("Monument", back_populates="slots")
    slot = relationship("DaySlot", back_populates="monuments")

class DaySlot(Base):
    __tablename__ = 'day_slot'
    
    slot_id = Column(Integer, primary_key=True, autoincrement=True)
    slot_name = Column(String(255), nullable=False)
    
    # Relationships
    monuments = relationship("MonumentSlot", back_populates="slot")

class Bookmarks(Base):
    __tablename__ = 'bookmarks'
    
    bookmark_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    monument_id = Column(Integer, ForeignKey('monument.monument_id'))
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    monument = relationship("Monument", back_populates="bookmarks")

class UserVisitedMonument(Base):
    __tablename__ = 'user_visited_monument'
    
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    monument_id = Column(Integer, ForeignKey('monument.monument_id'), primary_key=True)
    visited_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="visited_monuments")
    monument = relationship("Monument", back_populates="visited_by")