from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.api import deps
from app.db.models.ingredients import Ingredient as IngredientModel
from app.schemas.ingredients import IngredientCreate, IngredientUpdate, IngredientInDBBase

router = APIRouter()

#################################################################################################
#   GET ALL INGREDIENTS
#################################################################################################
@router.get("/", response_model=List[IngredientInDBBase])
async def get_ingredients(db: Session = Depends(deps.get_db)):
    try:
        ingredients = db.query(IngredientModel).all()
        return ingredients
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   GET INGREDIENT BY ID
#################################################################################################
@router.get("/{ingredient_id}", response_model=IngredientInDBBase)
async def get_ingredient_by_id(ingredient_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        ingredient = db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return ingredient
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
#   GET ALL INGREDIENTS for a user
#################################################################################################
@router.get("/user/{user_id}", response_model=List[IngredientInDBBase])
async def get_ingredients(user_id: uuid.UUID,db: Session = Depends(deps.get_db)):
    try:
        ingredients = db.query(IngredientModel).filter(IngredientModel.user_id == user_id).all()
        return ingredients
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   CREATE INGREDIENT
#################################################################################################
@router.post("/", response_model=IngredientInDBBase)
async def create_ingredient(ingredient_in: IngredientCreate, db: Session = Depends(deps.get_db)):
    try:
        new_ingredient = IngredientModel(
            ingredient_name=ingredient_in.ingredient_name,
            ingredient_description=ingredient_in.ingredient_description,
            ingredient_quantity=ingredient_in.ingredient_quantity,
            user_id=ingredient_in.user_id,
        )
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)
        return new_ingredient
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   UPDATE INGREDIENT BY ID
#################################################################################################
@router.put("/{ingredient_id}", response_model=IngredientInDBBase)
async def update_ingredient_by_id(
    ingredient_id: uuid.UUID, ingredient_in: IngredientUpdate, db: Session = Depends(deps.get_db)
):
    try:
        ingredient = db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")

        update_data = ingredient_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(ingredient, key, value)

        db.commit()
        db.refresh(ingredient)
        return ingredient
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   DELETE INGREDIENT BY ID
#################################################################################################
@router.delete("/{ingredient_id}", status_code=204)
async def delete_ingredient_by_id(ingredient_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        ingredient = db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")

        db.delete(ingredient)
        db.commit()
        return {"detail": "Ingredient successfully deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
