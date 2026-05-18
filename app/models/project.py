from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)

    places = relationship(
        "ProjectPlace",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def is_completed(self) -> bool:
        if not self.places:
            return False
        return all(place.is_visited for place in self.places)
