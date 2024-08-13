from fastapi import APIRouter
from app.routers.rooms import routers as room_routers

api_router = APIRouter()
api_router.include_router(room_routers, prefix="/rooms")
