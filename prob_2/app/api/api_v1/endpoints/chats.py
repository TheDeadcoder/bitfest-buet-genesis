from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.api import deps
from app.db.models.chats import Chat as ChatModel
from app.schemas.chats import ChatCreate, ChatInDBBase
from app.helpers.get_recipee_and_ingredients import generate_markdown_recipes, generate_markdown_ingredients  
from app.helpers.ai_chat import generate_recipe_completion

import uuid

router = APIRouter()

#################################################################################################
#   CREATE CHAT
#################################################################################################
@router.post("/", response_model=ChatInDBBase)
async def create_chat(chat_in: ChatCreate, db: Session = Depends(deps.get_db)):
    try:
        markdown_recipes = generate_markdown_recipes(chat_in.user_id, db)
        markdown_ingredients = generate_markdown_ingredients(chat_in.user_id, db)

        ai_response = generate_recipe_completion(chat_in.query, markdown_recipes, markdown_ingredients)

        new_chat = ChatModel(
            user_id=chat_in.user_id,
            query=chat_in.query,
            response=ai_response,
        )
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)

        return new_chat

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
