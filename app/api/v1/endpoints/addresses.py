from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse
from app.services.address import address_service

router = APIRouter()

@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(
    address_in: AddressCreate,
    db: AsyncSession = Depends(get_db_session)
):
    return await address_service.create_address(db, address_in)

@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(
    address_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    return await address_service.get_address(db, address_id)

@router.put("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: str,
    address_in: AddressUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    return await address_service.update_address(db, address_id, address_in)

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    await address_service.delete_address(db, address_id)

@router.get("/search/radius", response_model=List[AddressResponse])
async def search_addresses_by_radius(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Latitude"),
    lon: float = Query(..., ge=-180.0, le=180.0, description="Longitude"),
    radius_km: float = Query(..., gt=0.0, description="Radius in kilometers"),
    db: AsyncSession = Depends(get_db_session)
):
    return await address_service.get_addresses_within_radius(db, lat, lon, radius_km)
