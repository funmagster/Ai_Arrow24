create_start_databases = [
    """
    CREATE TABLE IF NOT EXISTS rooms (
        room TEXT,
        password TEXT,
        count_members INTEGER,
        active_members INTEGER
    );
    """
]

select_all_rooms = "SELECT * FROM rooms"
select_one_room = "SELECT * FROM rooms WHERE room = ?"
insert_room_q = "INSERT INTO rooms (room, password, count_members, active_members) VALUES (?, ?, ?, ?)"
update_room = "UPDATE rooms SET active_members = ? WHERE room = ?"
