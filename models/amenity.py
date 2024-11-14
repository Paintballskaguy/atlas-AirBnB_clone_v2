#!/usr/bin/python3
"""
Amenity class that inherits from BaseModel, Base
"""

from models.place import place_amenity
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    Amenity class that inherits from BaseModel
    Public class attributes:
        __tablename__: name of the MySQL table ('amenities')
        name: Column - string with max length of 128, cannot be null for DBStorage
        place_amenities: relationship with Place through place_amenity table for DBStorage
    """
    __tablename__ = "amenities"

    # Check storage type to define columns conditionally
    if BaseModel.storage_type == 'db':
        name = Column(String(128), nullable=False)
        
        # Define many-to-many relationship with Place through place_amenity
        place_amenities = relationship(
            "Place",
            secondary=place_amenity,
            back_populates="amenities",
            viewonly=False
        )
    else:
        # Define name as an empty string for FileStorage
        name = ""
