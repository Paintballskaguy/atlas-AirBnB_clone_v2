#!/usr/bin/python3

"""
State class that inherits from BaseModel
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage
from models.city import City


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
        """Returns the list of City objects related to the current State."""
        if storage.__class__.__name__ != 'DBStorage':
            # Return a list of City instances related to this State
            return [city for city in storage.all(City).values() if city.state_id == self.id]
        return []
