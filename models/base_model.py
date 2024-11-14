#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv

# Define Base for SQLAlchemy declarative mapping
Base = declarative_base()

class BaseModel:
    """Defines the base model with common attributes and methods for all tables"""

    # Set the storage type as a class attribute, which other models can check
    storage_type = getenv('HBNB_TYPE_STORAGE', 'file')

    # Common columns for all models
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes a new model instance"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

        # Update attributes if they exist in kwargs
        for key, value in kwargs.items():
            if key != '__class__':
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls_name = self.__class__.__name__
        return f"[{cls_name}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates `updated_at` and saves the instance to storage"""
        from models import storage
        self.updated_at = datetime.now(timezone.utc)
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Converts the instance into a dictionary format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__

        if 'created_at' in dictionary:
            dictionary['created_at'] = self.created_at.isoformat(timespec='microseconds')
        if 'updated_at' in dictionary:
            dictionary['updated_at'] = self.updated_at.isoformat(timespec='microseconds')

        dictionary.pop('_sa_instance_state', None)  # Remove SQLAlchemy state

        return dictionary

    def delete(self):
        """Deletes the current instance from storage"""
        from models import storage
        storage.delete(self)
