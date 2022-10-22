from pickletools import long1
import string
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None

class StopBase(BaseModel):
    StopAreaCode: str
    TimingPointName: str
    latitude: float
    longitude: float
    StopAreaCode: str
    TimingPointTown: str

class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class StopCreate(BaseModel):
    TimingPointName: str
    latitude: float
    longitude: float
    StopAreaCode: str
    TimingPointTown: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True

class Stop(StopBase):
    id: int
    items: list[Item] = []

    class Config:
        orm_mode = True
