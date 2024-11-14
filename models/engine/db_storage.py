from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from os import getenv

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database engine and connection."""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER', 'hbnb_dev')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD', 'hbnb_dev_pwd')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST', 'localhost')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB', 'hbnb_dev_db')
        HBNB_ENV = getenv('HBNB_ENV')
        HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE')

        self.__engine = create_engine(
            f'mysql+pymysql://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}',
            pool_pre_ping=True
        )

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the database session for all objects, or those of a specific class."""
        objects = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        else:
            for cls in [User, State, City, Amenity, Place, Review]:
                for obj in self.__session.query(cls).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add an object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session if specified."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create tables in the database and start a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Remove the current session."""
        self.__session.remove()
