from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class IngredientBase(BaseModel):
    ingredient_name: str
    ingredient_description: Optional[str] = None
    ingredient_quantity: Optional[str] = None
    user_id: UUID

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    ingredient_name: Optional[str] = None
    ingredient_description: Optional[str] = None
    ingredient_quantity: Optional[str] = None


class IngredientInDBBase(IngredientBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True