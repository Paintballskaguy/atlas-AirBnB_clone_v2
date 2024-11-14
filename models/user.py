#!/usr/bin/python3
"""
User class that inherits from BaseModel and Base
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class User(BaseModel, Base):
    """
    User class that inherits from BaseModel and Base
    Public class attributes:
        __tablename__: name of the MySQL table ('users')
        email: Column - string with max length of 128, cannot be null
        password: Column - string with max length of 128, cannot be null
        first_name: Column - string with max length of 128, nullable
        last_name: Column - string with max length of 128, nullable
        places: relationship with Place class
        reviews: relationship with Review class
    """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship("Place", cascade="all, delete-orphan", backref="user")
        reviews = relationship("Review", cascade="all, delete-orphan", backref="user")
