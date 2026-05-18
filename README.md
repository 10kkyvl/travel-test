# Travel Planner Application

## Overview
This is a CRUD application for managing travel projects and places to visit. It integrates with the Art Institute of Chicago API to validate places of interest.

The project is built with:
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy (Async)**
- **Alembic** (for database migrations)
- **uv** (for fast dependency management)

## Prerequisites
- Docker & Docker Compose (for running PostgreSQL and the app in containers)
- (Optional) `uv` if you want to run the application locally without Docker.

## How to Run

### Using Docker Compose
This is the easiest way to start the application along with the PostgreSQL database.

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
2. In a separate terminal, apply the database migrations:
   ```bash
   docker-compose exec app uv run alembic upgrade head
   ```

The application will be available at `http://localhost:8000`.
You can access the Swagger UI documentation at `http://localhost:8000/docs`.

### Running Locally (Without Docker)

1. Ensure you have a running PostgreSQL instance and update the `DATABASE_URL` in `.env` (or pass it as an environment variable). The default expected URL for local testing is:
   `postgresql+asyncpg://travel_user:travel_password@localhost:5433/travel_planner`

2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

3. Run database migrations:
   ```bash
   uv run alembic revision --autogenerate -m "Initial migration"
   uv run alembic upgrade head
   ```

4. Start the server:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

## Application Structure

The application follows a clean architecture pattern:
- `app/api/`: Contains the FastAPI routers and route dependencies.
- `app/core/`: Application configuration and custom exception handling.
- `app/db/`: Database session setup and configuration.
- `app/external/`: Clients for interacting with third-party APIs (Art Institute API) using an in-memory cache.
- `app/models/`: SQLAlchemy ORM definitions representing database tables.
- `app/schemas/`: Pydantic models for request/response validation and serialization.
- `app/services/`: Core business logic, encapsulating interactions with the database and external systems.

## API Documentation

FastAPI automatically generates an OpenAPI schema. Once the application is running, you can view the fully interactive Swagger documentation, which functions effectively as a Postman collection:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Bonus Features Implemented
- **Docker Integration**: Provided `Dockerfile` and `docker-compose.yml`.
- **API Documentation**: Handled automatically via FastAPI's OpenAPI integration.
- **Extended Business Logic**: 
  - Pagination implemented on `GET /projects/` endpoints.
  - Basic in-memory LRU caching applied to the Art Institute API client responses to reduce latency on repeated queries.
- **Code Quality**: Structured the application strictly, formatted with Ruff, explicitly managed types, removed boilerplate comments, and separated concerns clearly.
