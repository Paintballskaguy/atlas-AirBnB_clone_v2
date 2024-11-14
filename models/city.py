#!/usr/bin/python3
"""
City class that inherits from BaseModel and Base
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from os import getenv

class City(BaseModel, Base):
    """
    City class that inherits from BaseModel and Base
    Public class attributes:
        __tablename__: name of the MySQL table ('cities')
        name: Column - string with max length of 128, cannot be null
        state_id: Column - foreign key to states.id, cannot be null
        places: relationship with Place class
    """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship("Place", cascade="all, delete-orphan", backref="city")
