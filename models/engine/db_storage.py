#!/usr/bin/python3
"""
This is the engine to save data to the MySQL database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv


class DBStorage:
    """Database storage engine for MySQL databases.

    This class manages interactions with the MySQL database using SQLAlchemy.
    It supports CRUD operations, as well as additional methods for retrieving
    and counting objects by type.
    """
    __engine = None
    __session = None

    def __init__(self):
        HBNB_MYSQL_USER = getenv('hbnb_dev')
        HBNB_MYSQL_PWD = getenv('hbnb_dev_pwd')
        HBNB_MYSQL_HOST = getenv('localhost')
        HBNB_MYSQL_DB = getenv('hbnb_dev_db')
        HBNB_ENV = getenv('db')


    def all(self, cls=None):
        objects = {}
        if cls:  # look for a specific class
            if isinstance(cls, str):
                cls = eval(cls)
            objects = {
                f"{obj.__class__.__name__}.{obj.id}": obj
                for obj in self.__session.query(cls)
            }
        else:  # check all classes individually
            for cls in [User, State, City, Amenity, Place, Review]:
                objects.update({
                    f"{obj.__class__.__name__}.{obj.id}": obj
                    for obj in self.__session.query(cls)
                })
        return objects

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
            )
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        self.__session.close()

    def get(self, cls, id):
        """Retrieve one object"""
        if cls and id:
            obj = self.__session.query(cls).get(id)
            return obj
        return None
