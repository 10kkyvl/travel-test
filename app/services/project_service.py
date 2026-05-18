from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestException, NotFoundException
from app.external.art_institute import art_client
from app.models.place import ProjectPlace
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Project]:
        result = await self.session.execute(select(Project).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_by_id(self, project_id: int) -> Project:
        result = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalars().first()
        if not project:
            raise NotFoundException("Project not found")
        return project

    async def create(self, data: ProjectCreate) -> Project:
        places_data = data.places or []
        if len(places_data) > 10:
            raise BadRequestException("Maximum 10 places allowed")

        if len(places_data) != len(set(places_data)):
            raise BadRequestException("Duplicate places are not allowed")

        for external_id in places_data:
            artwork = await art_client.get_artwork(external_id)
            if not artwork:
                raise BadRequestException(
                    f"Place {external_id} not found in Art Institute API"
                )

        project = Project(
            name=data.name, description=data.description, start_date=data.start_date
        )
        self.session.add(project)
        await self.session.flush()

        for external_id in places_data:
            place = ProjectPlace(project_id=project.id, external_place_id=external_id)
            self.session.add(place)

        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def update(self, project_id: int, data: ProjectUpdate) -> Project:
        project = await self.get_by_id(project_id)
        project.name = data.name
        if data.description is not None:
            project.description = data.description
        if data.start_date is not None:
            project.start_date = data.start_date

        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def delete(self, project_id: int) -> None:
        project = await self.get_by_id(project_id)
        if any(place.is_visited for place in project.places):
            raise BadRequestException("Cannot delete project with visited places")

        await self.session.delete(project)
        await self.session.commit()
