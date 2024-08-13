from pydantic import BaseModel


class Room(BaseModel):
    name: str
    password: str
    count_members: int


class Organizer(BaseModel):
    name: str
    password: str


class Room_name(BaseModel):
    name: str
