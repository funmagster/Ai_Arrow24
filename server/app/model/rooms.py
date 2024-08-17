from pydantic import BaseModel


class Room(BaseModel):
    secret: str
    password: str


class Organizer(BaseModel):
    name: str
    password: str


class Room_name(BaseModel):
    name: str
