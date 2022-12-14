from xmlrpc.client import DateTime
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True, index=True)
    StopAreaCode = Column(String, index=True)
    TimingPointName = Column(String, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    StopAreaCode = Column(String, index=True)
    TimingPointTown = Column(Integer)

class Vehicles(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    TimeStamp = Column(String, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    Operator = Column(String, index=True)
    LineNumber = Column(Integer, index=True)
