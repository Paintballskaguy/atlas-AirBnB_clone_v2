from models import storage
from models.state import State

# Fetch all State objects
states = storage.all(State).values()
for state in states:
    print(state.id, state.name)