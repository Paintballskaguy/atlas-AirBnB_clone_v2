#!/usr/bin/python3

"""
State class that inherits from BaseModel
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage
from models import City


class State(BaseModel, Base):
    """
    State class that inherits from BaseModel and Base
    Public class attributes:
        __tablename__: string - name of the table
        name: string - empty string
        cities: relationship with City class
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City",
                          cascade="all, delete-orphan", backref="state")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs:
            self.name = ""
            
    @property
    def cities(self):
        """Return a list of City instances related to the current State."""
        if storage._FileStorage__objects:
            all_cities = storage.all(City).values()
            return [city for city in all_cities if city.state_id == self.id]
        return []
