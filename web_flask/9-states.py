#!/usr/bin/python3
"""
This script starts a Flask web application to display states and their cities.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage session after each request."""
    storage.close()

@app.route('/states', strict_slashes=False)
def display_states():
    """Displays an HTML page with a list of all State objects."""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('9-states.html', states=states, single_state=False)

@app.route('/states/<id>', strict_slashes=False)
def display_state_cities(id):
    """Displays an HTML page with cities of a specific State if the State exists."""
    state = storage.all(State).get(f"State.{id}")
    if state:
        return render_template('9-states.html', states=[state], single_state=True)
    else:
        return render_template('9-states.html', single_state=True, not_found=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
