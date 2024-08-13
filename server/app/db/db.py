import sqlite3
from app.db.executes import *


async def get_connection(name="rooms.db"):
    return sqlite3.connect(f'app/db/{name}')


async def create_start_table():
    conn = await get_connection()
    cur = conn.cursor()
    for execute in create_start_databases:
        cur.execute(execute)
        conn.commit()
    conn.close()


async def get_rooms():
    conn = await get_connection()
    cur = conn.cursor()
    cur.execute(select_all_rooms)
    result = cur.fetchall()
    conn.close()
    return result


async def join_room(room_name):
    conn = await get_connection()
    cur = conn.cursor()
    cur.execute(select_one_room, (room_name, ))
    room = cur.fetchone()

    ok = False
    print(room)
    if room and room[2] - room[3] > 0:
        cur.execute(update_room, (room[3] + 1, room[0]))
        conn.commit()
        ok = True
    conn.close()
    return ok


async def insert_room(name, password, count_members):
    conn = await get_connection()
    cur = conn.cursor()
    cur.execute(insert_room_q, (name, password, count_members, 0))
    conn.commit()
    conn.close()
