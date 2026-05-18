from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.place import PlaceResponse


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    start_date: date | None = None


class ProjectCreate(ProjectBase):
    places: list[str] | None = Field(default=None, max_length=10)


class ProjectUpdate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    is_completed: bool
    places: list[PlaceResponse] = []

    model_config = ConfigDict(from_attributes=True)
