from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class RecipeBase(BaseModel):
    recipe_name: str
    recipe_text: Optional[str] = None
    user_id: UUID

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    recipe_name: Optional[str] = None
    recipe_text: Optional[str] = None

class RecipeInDBBase(RecipeBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True