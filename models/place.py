#!/usr/bin/python3
"""
Place class that inherits from BaseModel
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

# Creates the association table for the many-to-many relationship between Place and Amenity
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """
    Place class that inherits from BaseModel and Base
    Public class attributes:
        __tablename__: string - name of the table
        city_id: string - foreign key to cities.id
        user_id: string - foreign key to users.id
        name: string - name of the place
        description: string - description of the place
        number_rooms: integer - number of rooms
        number_bathrooms: integer - number of bathrooms
        max_guest: integer - max number of guests
        price_by_night: integer - price per night
        latitude: float - latitude of the place
        longitude: float - longitude of the place
        amenities: relationship with Amenity class
        reviews: relationship with Review class
    """
    amenity_ids = []
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Relationship with Amenity using the place_amenity association table
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            back_populates="place_amenities",
            viewonly=False
        )
    
    reviews = relationship("Review", cascade="all, delete-orphan", backref="place")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs:
            self.city_id = ""
            self.user_id = ""
            self.name = ""
            self.description = ""
            self.number_rooms = 0
            self.number_bathrooms = 0
            self.max_guest = 0
            self.price_by_night = 0
            self.latitude = 0.0
            self.longitude = 0.0
            self.amenity_ids = []
