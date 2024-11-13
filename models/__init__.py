#!/bin/usr/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


storage = None
engine_url = f'mysql+pymysql://{getenv("HBNB_MYSQL_USER")}:{getenv("HBNB_MYSQL_PWD")}@{getenv("HBNB_MYSQL_HOST")}/{getenv("HBNB_MYSQL_DB")}'
engine = create_engine(engine_url, pool_pre_ping=True)

if getenv('HBNB_TYPE_STORAGE') == 'db':
    Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Import all models here
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

storage.reload()
