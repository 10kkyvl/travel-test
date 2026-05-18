from pydantic import BaseModel, ConfigDict


class PlaceBase(BaseModel):
    notes: str | None = None


class PlaceCreate(PlaceBase):
    external_place_id: str


class PlaceUpdate(PlaceBase):
    is_visited: bool | None = None


class PlaceResponse(PlaceBase):
    id: int
    project_id: int
    external_place_id: str
    is_visited: bool

    model_config = ConfigDict(from_attributes=True)
