import pytest

@pytest.mark.asyncio
async def test_create_and_read_address(client):
    payload = {
        "street": "123 Test Ave",
        "city": "Test City",
        "country": "Testland",
        "latitude": 50.0,
        "longitude": 10.0
    }
    
    response = await client.post("/api/v1/addresses/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["id"] is not None
    assert data["street"] == "123 Test Ave"
    
    address_id = data["id"]
    
    # Read address
    get_response = await client.get(f"/api/v1/addresses/{address_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == address_id

@pytest.mark.asyncio
async def test_search_addresses(client):
    # Create address
    await client.post("/api/v1/addresses/", json={
        "street": "Close",
        "latitude": 50.0,
        "longitude": 10.0
    })
    
    await client.post("/api/v1/addresses/", json={
        "street": "Far",
        "latitude": 60.0,
        "longitude": 20.0
    })
    
    # Search close
    response = await client.get("/api/v1/addresses/search/radius", params={
        "lat": 50.1,
        "lon": 10.1,
        "radius_km": 50.0
    })
    
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["street"] == "Close"

@pytest.mark.asyncio
async def test_delete_address(client):
    response = await client.post("/api/v1/addresses/", json={
        "latitude": 0.0,
        "longitude": 0.0
    })
    address_id = response.json()["id"]
    
    del_response = await client.delete(f"/api/v1/addresses/{address_id}")
    assert del_response.status_code == 204
    
    get_response = await client.get(f"/api/v1/addresses/{address_id}")
    assert get_response.status_code == 404
