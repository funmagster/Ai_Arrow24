from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse

from app.model.rooms import *
from app.db.db import get_rooms, join_room, insert_room, password_check
from app.func.room import download_pdf
import random
from dotenv import load_dotenv
import os

routers = APIRouter()
load_dotenv()
SECRET = os.getenv("SECRET")


@routers.post("/create_room")
async def get_movie_images(room: Room):
    if room.secret != SECRET:
        return HTTPException(status_code=422, detail='Incorrect SECRET')

    rooms = await get_rooms()
    active_room = str(random.randint(100000, 999999))
    for room_name in range(10000, 100000):
        for room_base in rooms:
            if room_base[0] == str(room_name):
                break
        else:
            active_room = str(room_name)
            break

    await insert_room(active_room, room.password, 4)
    return JSONResponse(status_code=200, content={'status_code': 200, 'success': True, 'room': active_room})


@routers.post("/join_room")
async def recommend_films(room_name: Room_name):
    ok = await join_room(room_name.name)
    if ok:
        return JSONResponse(status_code=200, content={'status_code': 200, 'success': True})
    else:
        return HTTPException(status_code=400, detail='Room crowded or not found')


@routers.post("/download_pdf")
async def recommend_films(organizer: Organizer):
    ok = await password_check(organizer.name, organizer.password)
    if not ok:
        return HTTPException(status_code=422, detail='Wrong password')
    file_path, file_name = await download_pdf()
    return FileResponse(path=file_path, filename="file_name.pdf", media_type='application/pdf')
