from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.schemas.place import PlaceCreate, PlaceResponse, PlaceUpdate
from app.services.place_service import PlaceService

router = APIRouter(prefix="/projects/{project_id}/places", tags=["places"])


@router.get("/", response_model=list[PlaceResponse])
async def list_places(project_id: int, session: AsyncSession = Depends(get_db_session)):
    service = PlaceService(session)
    return await service.get_all_by_project(project_id)


@router.get("/{place_id}", response_model=PlaceResponse)
async def get_place(
    project_id: int, place_id: int, session: AsyncSession = Depends(get_db_session)
):
    service = PlaceService(session)
    return await service.get_by_id(project_id, place_id)


@router.post("/", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
async def create_place(
    project_id: int, data: PlaceCreate, session: AsyncSession = Depends(get_db_session)
):
    service = PlaceService(session)
    return await service.create(project_id, data)


@router.patch("/{place_id}", response_model=PlaceResponse)
async def update_place(
    project_id: int,
    place_id: int,
    data: PlaceUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    service = PlaceService(session)
    return await service.update(project_id, place_id, data)
