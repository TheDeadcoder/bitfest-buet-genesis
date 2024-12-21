from fastapi import APIRouter
from app.api.api_v1.endpoints import users
api_router_v1 = APIRouter()

api_router_v1.include_router(users.router, prefix="/users", tags=["users"])
