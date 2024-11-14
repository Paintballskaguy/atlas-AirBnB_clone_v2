#!/usr/bin/python3
"""
Review class that inherits from BaseModel and Base
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Review(BaseModel, Base):
    """
    Review class that inherits from BaseModel and Base
    Public class attributes:
        __tablename__: name of the MySQL table ('reviews')
        text: Column - string with max length of 1024, cannot be null
        place_id: Column - foreign key to places.id, cannot be null
        user_id: Column - foreign key to users.id, cannot be null
    """
    __tablename__ = 'reviews'
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
