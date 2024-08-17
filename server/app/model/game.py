from pydantic import BaseModel


class Game_start(BaseModel):
    prompt: str
    room: str


class Game_play(BaseModel):
    room: str
    prompt: str
    character: str
    count_room_complete: int
    history: str
    story: str

