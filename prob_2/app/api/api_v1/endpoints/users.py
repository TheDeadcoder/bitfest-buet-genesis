from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.api import deps
from app.db.models.users import User as UserModel
from app.schemas.users import UserInDBBase, UserCreate, UserUpdate
from app.helpers.validators import validate_email, validate_phone
router = APIRouter()


#################################################################################################
#   GET USER BY ID
#################################################################################################
@router.get("/{user_id}", response_model=UserInDBBase)
async def get_user_by_id(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    
    try:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   CREATE USER
#################################################################################################
@router.post("/", response_model=UserInDBBase)
async def create_user(*, db: Session = Depends(deps.get_db), user_in: UserCreate):
    
    try:
        if user_in.email:
            if validate_email(user_in.email) == "invalid":
                raise HTTPException(status_code=400, detail="Invalid Email")
            
        db_user = UserModel(
            name=user_in.name,
            address=user_in.address,
            country=user_in.country,
            occupation=user_in.occupation,
            email=user_in.email
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   UPDATE USER BY ID
#################################################################################################
@router.put("/{user_id}", response_model=UserInDBBase)
async def update_user_by_id(*, db: Session = Depends(deps.get_db), user_id: uuid.UUID, user_in: UserUpdate):
    try:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        
        return db_user
    except HTTPException as http_exc:
        raise http_exc
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


#################################################################################################
#   DELETE USER BY ID
#################################################################################################
@router.delete("/{user_id}", status_code=204)
async def delete_user_by_id(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        db.delete(db_user)
        db.commit()
        
        return {"detail": "User successfully deleted"}
    except HTTPException as http_exc:
        raise http_exc
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
