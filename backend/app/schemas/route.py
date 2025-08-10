from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RouteSearch(BaseModel):
    origin: str
    destination: str

class HistoricalSpotResponse(BaseModel):
    id: int
    place_id: str
    name: str
    address: Optional[str]
    lat: float
    lng: float
    description: Optional[str]
    types: Optional[List[str]]
    
    class Config:
        orm_mode = True

class RouteCreate(BaseModel):
    origin: str
    destination: str
    origin_lat: float
    origin_lng: float
    dest_lat: float
    dest_lng: float
    distance: str
    duration: str
    polyline: str

class RouteResponse(BaseModel):
    id: int
    origin: str
    destination: str
    origin_lat: float
    origin_lng: float
    dest_lat: float
    dest_lng: float
    distance: str
    duration: str
    polyline: str
    created_at: datetime
    historical_spots: List[HistoricalSpotResponse] = []
    
    class Config:
        orm_mode = True