from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    origin = Column(String(200), nullable=False)
    destination = Column(String(200), nullable=False)
    origin_lat = Column(Float)
    origin_lng = Column(Float)
    dest_lat = Column(Float)
    dest_lng = Column(Float)
    distance = Column(String(50))
    duration = Column(String(50))
    polyline = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="routes")
    historical_spots = relationship("HistoricalSpot", back_populates="route")
    quiz_attempts = relationship("QuizAttempt", back_populates="route")

class HistoricalSpot(Base):
    __tablename__ = "historical_spots"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    place_id = Column(String(100), unique=True)
    name = Column(String(200), nullable=False)
    address = Column(String(300))
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    description = Column(Text)
    types = Column(JSON)  # List of place types from Google
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    route = relationship("Route", back_populates="historical_spots")