class AddressNotFoundError(Exception):
    def __init__(self, address_id: str):
        self.address_id = address_id
        super().__init__(f"Address with ID {address_id} not found")

class InvalidCoordinatesError(Exception):
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        super().__init__(f"Invalid coordinates provided: lat={lat}, lon={lon}")
