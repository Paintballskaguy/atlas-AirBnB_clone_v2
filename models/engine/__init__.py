import os

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage


storage_t = os.environ.get('HBNB_TYPE_STORAGE')

if storage_t == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

try:
    storage.reload()
except Exception as e:
    print(f"Error during reload: {e}")

# Import all models AFTER storage is initialized and reloaded
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

import models
models.storage.storage = storage