from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.address import AddressNotFoundError, InvalidCoordinatesError
import structlog

logger = structlog.get_logger(__name__)

async def address_not_found_handler(request: Request, exc: AddressNotFoundError):
    logger.warning("Address not found", address_id=exc.address_id, path=request.url.path)
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)},
    )

async def invalid_coordinates_handler(request: Request, exc: InvalidCoordinatesError):
    logger.warning("Invalid coordinates", lat=exc.lat, lon=exc.lon, path=request.url.path)
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )
