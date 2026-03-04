from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from geopy.distance import geodesic
from app.repositories.address import address_repository
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse
from app.exceptions.address import AddressNotFoundError, InvalidCoordinatesError
from app.models.address import Address

class AddressService:
    
    @staticmethod
    async def create_address(db: AsyncSession, address_in: AddressCreate) -> Address:
        return await address_repository.create(db, obj_in=address_in)

    @staticmethod
    async def get_address(db: AsyncSession, address_id: str) -> Address:
        address = await address_repository.get(db, id=address_id)
        if not address:
            raise AddressNotFoundError(address_id)
        return address

    @staticmethod
    async def update_address(db: AsyncSession, address_id: str, address_in: AddressUpdate) -> Address:
        address = await address_repository.get(db, id=address_id)
        if not address:
            raise AddressNotFoundError(address_id)
        return await address_repository.update(db, db_obj=address, obj_in=address_in)

    @staticmethod
    async def delete_address(db: AsyncSession, address_id: str) -> None:
        address = await address_repository.get(db, id=address_id)
        if not address:
            raise AddressNotFoundError(address_id)
        await address_repository.remove(db, id=address_id)

    @staticmethod
    async def get_addresses_within_radius(db: AsyncSession, lat: float, lon: float, radius_km: float) -> List[Address]:
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise InvalidCoordinatesError(lat, lon)
        
        # Bounding box calculation for DB pre-filtering
        # 1 degree of latitude is ~111km
        lat_diff = radius_km / 111.0
        # 1 degree of longitude is ~111km at equator, but shrinks at distance
        # To be safe, we calculate max lon diff with a margin
        import math
        lon_diff = radius_km / (111.0 * math.cos(math.radians(lat))) if math.cos(math.radians(lat)) > 0.01 else 360
        
        min_lat, max_lat = lat - lat_diff, lat + lat_diff
        min_lon, max_lon = lon - lon_diff, lon + lon_diff
        
        # Retrieve candidates from DB within bounding box
        candidates = await address_repository.get_within_bounding_box(
            db, min_lat, max_lat, min_lon, max_lon
        )
        
        # Precise distance filtering using geopy
        target_coords = (lat, lon)
        results = []
        for addr in candidates:
            addr_coords = (addr.latitude, addr.longitude)
            distance = geodesic(target_coords, addr_coords).kilometers
            if distance <= radius_km:
                results.append(addr)
                
        return results

address_service = AddressService()
