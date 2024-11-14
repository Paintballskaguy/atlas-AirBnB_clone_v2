#!/usr/bin/python3

"""
State class that inherits from BaseModel and Base
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """
    State class that inherits from BaseModel and Base
    Public class attributes:
        __tablename__: name of the MySQL table ('states')
        name: Column - string with max length of 128, cannot be null
        cities: relationship with the City class, or a property for FileStorage
    """
    __tablename__ = 'states'
    
    # Check if the storage type is set to 'db' to define columns accordingly
    storage_type = getenv('HBNB_TYPE_STORAGE')

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete-orphan", backref="state")
    else:
        name = ""  # Default empty string for FileStorage

        @property
        def cities(self):
            """Returns a list of City objects related to the current State."""
            from models import storage
            from models.city import City
            # Collect City instances with matching state_id
            return [city for city in storage.all(City).values() if city.state_id == self.id]
