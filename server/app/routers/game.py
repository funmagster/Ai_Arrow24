from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import asyncio
from app.model.game import *
from app.db.db import close_room
routers = APIRouter()


@routers.post("/start_game")
async def get_movie_images(game_start: Game_start):
    await close_room(game_start.room)
    await asyncio.sleep(1000)
    return JSONResponse(status_code=200, content={
        'status_code': 200, 'success': True,
        'history': 'yo yo yo',
        'img': 'yo yo yo',
        'voice': 'yo yo yo'
    })
