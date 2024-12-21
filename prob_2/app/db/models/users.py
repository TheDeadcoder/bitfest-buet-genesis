import uuid
from sqlalchemy import Column, String, ARRAY, TIMESTAMP, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True, default='N/A')
    country = Column(String, nullable=True, default='N/A')
    occupation = Column(String, nullable=True, default='N/A')
    email = Column(String, nullable=False, unique=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # one to many relationship with Ingredient
    ingredients = relationship("Ingredient", back_populates="user", cascade="all, delete-orphan")
    
    # one tyo many relationship with Recipe
    recipes = relationship("Recipe", back_populates="user", cascade="all, delete-orphan")
