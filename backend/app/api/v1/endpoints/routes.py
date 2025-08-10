from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api.deps import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.models.route import Route, HistoricalSpot
from app.schemas.route import RouteSearch, RouteResponse, HistoricalSpotResponse
from app.services.google_maps import google_maps_service

router = APIRouter()

@router.post("/search", response_model=Dict)
async def search_route(
    route_search: RouteSearch,
    current_user: User = Depends(get_current_active_user)
):
    # Search route using Google Maps
    route_data = await google_maps_service.search_route(
        route_search.origin,
        route_search.destination
    )
    
    if not route_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    # Get historical spots along the route
    historical_spots = await google_maps_service.get_historical_spots_along_route(
        route_data['polyline'],
        num_points=5
    )
    
    return {
        'route': route_data,
        'historical_spots': historical_spots
    }

@router.post("/save", response_model=RouteResponse)
async def save_route(
    route_data: Dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Create route record
    db_route = Route(
        user_id=current_user.id,
        origin=route_data['origin'],
        destination=route_data['destination'],
        origin_lat=route_data['origin_coords']['lat'],
        origin_lng=route_data['origin_coords']['lng'],
        dest_lat=route_data['dest_coords']['lat'],
        dest_lng=route_data['dest_coords']['lng'],
        distance=route_data['distance'],
        duration=route_data['duration'],
        polyline=route_data['polyline']
    )
    db.add(db_route)
    await db.flush()
    
    # Save historical spots
    for spot_data in route_data.get('historical_spots', []):
        # Check if spot already exists
        result = await db.execute(
            select(HistoricalSpot).where(HistoricalSpot.place_id == spot_data['place_id'])
        )
        existing_spot = result.scalar_one_or_none()
        
        if not existing_spot:
            db_spot = HistoricalSpot(
                route_id=db_route.id,
                place_id=spot_data['place_id'],
                name=spot_data['name'],
                address=spot_data.get('address'),
                lat=spot_data['lat'],
                lng=spot_data['lng'],
                description=spot_data.get('description'),
                types=spot_data.get('types', [])
            )
            db.add(db_spot)
    
    await db.commit()
    await db.refresh(db_route)
    
    # Load relationships
    result = await db.execute(
        select(Route)
        .where(Route.id == db_route.id)
        .options(selectinload(Route.historical_spots))
    )
    db_route = result.scalar_one()
    
    return db_route

@router.get("/history", response_model=List[RouteResponse])
async def get_route_history(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(Route)
        .where(Route.user_id == current_user.id)
        .options(selectinload(Route.historical_spots))
        .order_by(Route.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    routes = result.scalars().all()
    return routes

@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(
    route_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(Route)
        .where(Route.id == route_id, Route.user_id == current_user.id)
        .options(selectinload(Route.historical_spots))
    )
    route = result.scalar_one_or_none()
    
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    
    return route