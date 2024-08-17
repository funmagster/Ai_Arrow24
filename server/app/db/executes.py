create_start_databases = [
    """
    CREATE TABLE IF NOT EXISTS rooms (
        room TEXT,
        password TEXT,
        count_members INTEGER,
        active_members INTEGER
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS historys (
        room TEXT,
        story TEXT,
        history TEXT,
        character TEXT
    );
    """
]

select_all_rooms = "SELECT * FROM rooms"
select_one_room = "SELECT * FROM rooms WHERE room = ?"
insert_room_q = "INSERT INTO rooms (room, password, count_members, active_members) VALUES (?, ?, ?, ?)"
update_room = "UPDATE rooms SET active_members = ? WHERE room = ?"
select_history = "SELECT * FROM historys WHERE room = ?"
update_history_q = "UPDATE historys SET history = ? WHERE room = ?"
insert_history_q = "INSERT INTO historys (room, story, history, character) VALUES (?, ?, ?, ?)"
