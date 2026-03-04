import pytest
from app.services.address import address_service
from app.schemas.address import AddressCreate
from app.exceptions.address import InvalidCoordinatesError

@pytest.mark.asyncio
async def test_create_address_service(db_session):
    address_in = AddressCreate(
        street="123 Main St",
        city="Testville",
        latitude=40.7128,
        longitude=-74.0060
    )
    
    address = await address_service.create_address(db_session, address_in)
    
    assert address.id is not None
    assert address.street == "123 Main St"
    assert address.latitude == 40.7128
    assert address.longitude == -74.0060

@pytest.mark.asyncio
async def test_distance_filtering_service(db_session):
    # Create two addresses: one close, one far
    addr1 = AddressCreate(latitude=40.7128, longitude=-74.0060) # NYC
    addr2 = AddressCreate(latitude=34.0522, longitude=-118.2437) # LA
    
    await address_service.create_address(db_session, addr1)
    await address_service.create_address(db_session, addr2)
    
    # Search within 100km of NYC
    results = await address_service.get_addresses_within_radius(
        db_session, lat=40.7, lon=-74.0, radius_km=100.0
    )
    
    assert len(results) == 1
    assert results[0].latitude == 40.7128

@pytest.mark.asyncio
async def test_invalid_coordinates(db_session):
    with pytest.raises(InvalidCoordinatesError):
        await address_service.get_addresses_within_radius(
            db_session, lat=100.0, lon=200.0, radius_km=10.0
        )
