from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.model.rooms import *
from app.db.db import get_rooms, join_room, insert_room
from app.func.room import download_pdf
routers = APIRouter()


@routers.post("/create_room")
async def get_movie_images(room: Room):
    if not (len(room.name) == 5 and len(room.password) and 1 <= room.count_members <= 5):
        return HTTPException(status_code=422, detail='Incorrect input data')

    rooms = await get_rooms()
    for room_db in rooms:
        if room.name == room_db[0]:
            return HTTPException(status_code=400, detail="The room's already taken")

    await insert_room(room.name, room.password, room.count_members)
    return JSONResponse(status_code=200, content={'success': True})


@routers.post("/join_room")
async def recommend_films(room_name: Room_name):
    ok = await join_room(room_name.name)
    if ok:
        return JSONResponse(status_code=200, content={'success': True})
    else:
        return HTTPException(status_code=400, detail='Room crowded or not found')


@routers.post("/download_pdf")
async def recommend_films(organizer: Organizer):
    await download_pdf()
