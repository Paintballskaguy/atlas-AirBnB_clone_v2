from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError, OperationalError, ProgrammingError
from os import getenv
from models.base_model import Base

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB),
                                      pool_pre_ping=True)

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

        try:
            Base.metadata.create_all(self.__engine)
            print("Tables created or verified successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
            # Optionally, you could re-raise the exception here
            raise

    def reload(self):
        try:
            sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
            Session = scoped_session(sess_factory)
            self.__session = Session()
            
            inspector = inspect(self.__engine)
            print("Existing tables:", inspector.get_table_names())

            from models.user import User
            from models.state import State
            from models.city import City
            from models.amenity import Amenity
            from models.place import Place
            from models.review import Review

            for cls in [User, State, City, Amenity, Place, Review]:
                if cls != Base:
                    try:
                        self.__session.query(cls).all()
                    except SQLAlchemyError:
                        print(f"Table '{cls.__name__}' does not exist")
        except Exception as e:
            print(f"Error during reload: {e}")

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        if cls is None:
            # Query all classes if no class is specified
            for model in Base.__subclasses__():
                objs = self.__session.query(model).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        else:
            # Query only the specified class
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        return new_dict
