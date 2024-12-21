from fastapi import APIRouter
from app.api.api_v1.endpoints import users, ingredients, recipes
api_router_v1 = APIRouter()

api_router_v1.include_router(users.router, prefix="/users", tags=["users"])
api_router_v1.include_router(ingredients.router, prefix="/ingredients", tags=["ingredients"])
api_router_v1.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
