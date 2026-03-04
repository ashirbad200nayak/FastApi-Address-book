from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate

class AddressRepository(BaseRepository[Address, AddressCreate, AddressUpdate]):
    
    async def get_all_addresses(self, db: AsyncSession) -> List[Address]:
        result = await db.execute(select(Address))
        return list(result.scalars().all())
    
    # We will fetch coordinates to process precise geodesic filtering
    # at the service layer, but we could add a bounding box pre-filter here
    async def get_within_bounding_box(self, db: AsyncSession, min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> List[Address]:
        query = select(Address).filter(
            Address.latitude >= min_lat,
            Address.latitude <= max_lat,
            Address.longitude >= min_lon,
            Address.longitude <= max_lon
        )
        result = await db.execute(query)
        return list(result.scalars().all())

address_repository = AddressRepository(Address)
