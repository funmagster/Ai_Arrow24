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
    return set(result)


async def join_room(room_name):
    conn = await get_connection()
    cur = conn.cursor()
    cur.execute(select_one_room, (room_name, ))
    room = cur.fetchone()

    ok = False
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


async def close_room(room_name):
    conn = await get_connection()
    cur = conn.cursor()
    cur.execute(select_one_room, (room_name, ))
    room = cur.fetchone()
    active_members = room[3]
    cur.execute(update_room, (room[2] + 1, room[0]))
    conn.commit()
    conn.close()

    return active_members


async def password_check(room, password):
    conn = await get_connection()
    cur = conn.cursor()
    cur.execute(select_one_room, (room,))
    room = cur.fetchone()

    ok = False
    if room and room[1] == password:
        ok = True
    conn.close()
    return ok


async def update_history(room, history):
    conn = await get_connection()
    cur = conn.cursor()
    cur.execute(select_history, (room, ))
    history_old = cur.fetchone()[2]
    history_new = history_old + history
    cur.execute(update_history_q, (history_new, room))
    conn.commit()
    conn.close()


async def insert_history(room, story, history, character):
    conn = await get_connection()
    cur = conn.cursor()
    cur.execute(insert_history_q, (room, story, history, character))
    conn.commit()
    conn.close()


async def get_history(room):
    conn = await get_connection()
    cur = conn.cursor()
    cur.execute(select_history, (room, ))
    history = cur.fetchone()
    conn.close()

    return history
