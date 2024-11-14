#!/usr/bin/python3
"""
This is the engine to save data to the MySQL database.
"""

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv, environ
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy.exc import InvalidRequestError


# Define a dictionary of valid classes for use in queries
classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

def metadata_create_all(engine):
    """
    Helper function to create all tables from models that inherit from Base.
    """
    from models.base_model import Base
    metadata = Base.metadata
    metadata.create_all(engine)
    return metadata


class DBStorage:
    """Database storage engine for MySQL databases."""

    __engine = None
    __session = None
    __session_generator = None
    __db_url = None

def __init__(self):
    """Initializes the DBStorage instance and creates the engine."""
    # Fetching storage type directly using os.environ to verify access
    HBNB_TYPE_STORAGE = environ.get("HBNB_TYPE_STORAGE")
    print("Verified HBNB_TYPE_STORAGE within __init__:", HBNB_TYPE_STORAGE)

    if HBNB_TYPE_STORAGE == 'db':
        # Continue initializing DBStorage...
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER', 'hbnb_dev')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD', 'hbnb_dev_pwd')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST', 'Johnselementary')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB', 'hbnb_dev_db')
        HBNB_ENV = getenv('HBNB_ENV')

        # Only create the engine if HBNB_TYPE_STORAGE is 'db'
        self.__db_url = f"mysql+pymysql://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}"
        self.__engine = create_engine(self.__db_url, pool_pre_ping=True)
        metadata_create_all(self.__engine)

        # Configure session generator
        self.__session_generator = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session_generator = scoped_session(self.__session_generator)

        # Drop all tables if in test environment
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

        # Initialize the session
        self.__session = self.__session_generator()

    def all(self, cls=None):
        """
        Queries and returns a dictionary of all objects or objects of a specific class.
        """
        results = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            results = self.construct_dict(query)
        else:
            for model_cls in classes.values():
                query = self.__session.query(model_cls)
                results.update(self.construct_dict(query))
        return results

    def new(self, obj):
        """Adds an object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session if not None."""
        if obj:
            ObjClass = type(obj)
            self.__session.query(ObjClass).filter(ObjClass.id == obj.id).delete(synchronize_session=False)
            self.save()

    def reload(self):
        """Creates all tables and initializes a new session."""
        try:
            self.__session.close()
        except InvalidRequestError:
            pass
        metadata_create_all(self.__engine)
        self.__session = self.__session_generator()

    def close(self):
        """Closes the current SQLAlchemy session."""
        self.__session.close()

    def construct_key(self, obj):
        """
        Helper method to construct key for object dictionary.
        """
        return f"{type(obj).__name__}.{obj.id}"

    def construct_dict(self, query_records):
        """
        Constructs a dictionary from query records with keys in the format <class>.<id>.
        """
        dictionary = {}
        for entry in query_records:
            key = self.construct_key(entry)
            dictionary[key] = entry
        return dictionary

    def get(self, cls, id):
        """
        Returns the object based on the class and its ID, or None if not found.
        """
        if cls in classes.values():
            objs = self.all(cls)
            for obj in objs.values():
                if obj.id == id:
                    return obj
        return None

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class.
        If no class is passed, returns the count of all objects in storage.
        """
        if cls is None:
            return len(self.all())
        else:
            return len(self.all(cls))
