# FastAPI Address Book API

A production-grade Address Book REST API built with FastAPI, Python 3.11+, and SQLite.

## Core Features
1. **CRUD Operations**: Create, Read, Update, Delete addresses.
2. **Proximity Search**: Find all addresses within a given radius (in km) from specific coordinates.
3. **Robust Architecture**: Built following Clean Architecture and SOLID principles.
4. **Validation**: Full Pydantic validation preventing invalid data from entering the service layer.
5. **Distance Filtering Strategy**: 
    - Database bounding box pre-filter to reduce data fetched.
    - Precise geodesic distance calculation using `geopy` locally in the service.
    - *Trade-off*: SQLite does not have native geospatial indexes without Spatialite. This hybrid approach allows fast DB querying combined with high accuracy in Python without requiring a heavy external geospatial database extension.

## Tech Stack
- **FastAPI**
- **SQLAlchemy 2.x (Async)**
- **Alembic**
- **Pydantic v2**
- **geopy**
- **structlog**
- **pytest & httpx**
- **Docker & Compose**

## Quick Start (Under 5 Minutes)

### Local Setup
1. **Create Virtual Environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run Migrations**
```bash
alembic upgrade head
```

4. **Start Application**
```bash
uvicorn app.main:app --reload
```
View Swagger Docs: [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)  
View Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

5. **Run Tests**
```bash
pytest -v
```

### Docker Setup
```bash
docker-compose up --build
```
This automatically runs migrations and starts the hot-reloading server on port 8000.
