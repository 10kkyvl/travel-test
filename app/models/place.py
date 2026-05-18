from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class ProjectPlace(Base):
    __tablename__ = "project_places"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    external_place_id = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    is_visited = Column(Boolean, default=False, nullable=False)

    project = relationship("Project", back_populates="places")
