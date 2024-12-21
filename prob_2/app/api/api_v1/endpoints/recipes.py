from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, File as FastAPIFile, Form, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.api import deps
from app.db.models.recipes import Recipe as RecipeModel
from app.schemas.recipes import RecipeCreate, RecipeUpdate, RecipeInDBBase

router = APIRouter()

#################################################################################################
#   GET ALL RECIPES
#################################################################################################
@router.get("/", response_model=List[RecipeInDBBase])
async def get_recipes(db: Session = Depends(deps.get_db)):
    try:
        recipes = db.query(RecipeModel).all()
        return recipes
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   GET RECIPE BY ID
#################################################################################################
@router.get("/{recipe_id}", response_model=RecipeInDBBase)
async def get_recipe_by_id(recipe_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
#   GET ALL RECIPES for a user
#################################################################################################
@router.get("/user/{user_id}", response_model=List[RecipeInDBBase])
async def get_recipes_of_user(user_id: uuid.UUID,db: Session = Depends(deps.get_db)):
    try:
        recipes = db.query(RecipeModel).filter(RecipeModel.user_id == user_id).all()
        return recipes
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   CREATE RECIPE
#################################################################################################
@router.post("/", response_model=RecipeInDBBase)
async def create_recipe(recipe_in: RecipeCreate, db: Session = Depends(deps.get_db)):
    try:
        new_recipe = RecipeModel(
            recipe_name=recipe_in.recipe_name,
            recipe_text=recipe_in.recipe_text,
            user_id=recipe_in.user_id,
        )
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   UPDATE RECIPE BY ID
#################################################################################################
@router.put("/{recipe_id}", response_model=RecipeInDBBase)
async def update_recipe_by_id(
    recipe_id: uuid.UUID, recipe_in: RecipeUpdate, db: Session = Depends(deps.get_db)
):
    try:
        recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        update_data = recipe_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(recipe, key, value)

        db.commit()
        db.refresh(recipe)
        return recipe
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   DELETE RECIPE BY ID
#################################################################################################
@router.delete("/{recipe_id}", status_code=204)
async def delete_recipe_by_id(recipe_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        db.delete(recipe)
        db.commit()
        return {"detail": "Recipe successfully deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))

#################################################################################################
#   CREATE RECIPE FROM FILE
#################################################################################################
@router.post("/from-file", response_model=RecipeInDBBase)
async def create_recipe_from_file(
    recipe_name: str = Form(...),
    user_id: uuid.UUID = Form(...),
    recipe_file: UploadFile = FastAPIFile(...),
    db: Session = Depends(deps.get_db)
):
    try:
        if not recipe_file or recipe_file.content_type != "text/plain":
            raise HTTPException(status_code=400, detail="Invalid file type. Only text files are allowed.")

        recipe_text = (await recipe_file.read()).decode("utf-8")

        new_recipe = RecipeModel(
            recipe_name=recipe_name,
            recipe_text=recipe_text,
            user_id=user_id,
        )
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)

        return new_recipe

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding file. Please upload a valid text file.")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))