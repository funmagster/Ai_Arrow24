from fastapi import APIRouter
from app.routers.rooms import routers as room_routers
from app.routers.game import routers as game_routers

api_router = APIRouter()
api_router.include_router(room_routers, prefix="/rooms")
api_router.include_router(game_routers, prefix="/game")
