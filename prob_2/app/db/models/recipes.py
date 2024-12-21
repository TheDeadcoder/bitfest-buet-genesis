import uuid
from sqlalchemy import Column, String, Boolean, DateTime, UUID, Integer, ForeignKey, Enum, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    recipe_name = Column(String, nullable=False)
    recipe_text = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="recipes")

