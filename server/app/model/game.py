from pydantic import BaseModel


class Game_start(BaseModel):
    prompt: str
    room: str

