from models import storage
from models.state import State

# Fetch all State objects
states = storage.all(State).values()
for state in states:
    print(state.id, state.name)
    
    
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER', 'hbnb_dev')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD', 'hbnb_dev_pwd')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST', 'localhost')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB', 'hbnb_dev_db')
        HBNB_ENV = getenv('HBNB_ENV')