from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.api import api_router
from app.exceptions.address import AddressNotFoundError, InvalidCoordinatesError
from app.exceptions.handlers import address_not_found_handler, invalid_coordinates_handler, global_exception_handler
import structlog

setup_logging()
logger = structlog.get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Exception handlers
app.add_exception_handler(AddressNotFoundError, address_not_found_handler)
app.add_exception_handler(InvalidCoordinatesError, invalid_coordinates_handler)
# Generic handler for internal server errors
app.add_exception_handler(Exception, global_exception_handler)

@app.middleware("http")
async def logging_middleware(request, call_next):
    logger.info("Incoming Request", method=request.method, url=str(request.url))
    response = await call_next(request)
    logger.info("Outgoing Response", status_code=response.status_code)
    return response

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
