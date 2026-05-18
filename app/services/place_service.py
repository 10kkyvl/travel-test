from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestException, NotFoundException
from app.external.art_institute import art_client
from app.models.place import ProjectPlace
from app.schemas.place import PlaceCreate, PlaceUpdate
from app.services.project_service import ProjectService


class PlaceService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.project_service = ProjectService(session)

    async def get_all_by_project(self, project_id: int) -> list[ProjectPlace]:
        await self.project_service.get_by_id(project_id)
        result = await self.session.execute(
            select(ProjectPlace).where(ProjectPlace.project_id == project_id)
        )
        return list(result.scalars().all())

    async def get_by_id(self, project_id: int, place_id: int) -> ProjectPlace:
        await self.project_service.get_by_id(project_id)
        result = await self.session.execute(
            select(ProjectPlace).where(
                ProjectPlace.id == place_id, ProjectPlace.project_id == project_id
            )
        )
        place = result.scalars().first()
        if not place:
            raise NotFoundException("Place not found")
        return place

    async def create(self, project_id: int, data: PlaceCreate) -> ProjectPlace:
        project = await self.project_service.get_by_id(project_id)

        if len(project.places) >= 10:
            raise BadRequestException("Maximum 10 places allowed per project")

        if any(p.external_place_id == data.external_place_id for p in project.places):
            raise BadRequestException("Place already exists in this project")

        artwork = await art_client.get_artwork(data.external_place_id)
        if not artwork:
            raise BadRequestException(
                f"Place {data.external_place_id} not found in Art Institute API"
            )

        place = ProjectPlace(
            project_id=project_id,
            external_place_id=data.external_place_id,
            notes=data.notes,
        )
        self.session.add(place)
        await self.session.commit()
        await self.session.refresh(place)
        return place

    async def update(
        self, project_id: int, place_id: int, data: PlaceUpdate
    ) -> ProjectPlace:
        place = await self.get_by_id(project_id, place_id)

        if data.notes is not None:
            place.notes = data.notes
        if data.is_visited is not None:
            place.is_visited = data.is_visited

        await self.session.commit()
        await self.session.refresh(place)
        return place
