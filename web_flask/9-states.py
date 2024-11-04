#!/usr/bin/python3
"""
This script starts a Flask web application to display states and cities.
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
def states():
    """Displays an HTML page with a list of all State objects."""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('9-states.html', states=states, not_found=False)

@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Displays an HTML page with cities of a State if the State exists."""
    state = storage.all(State).get("State." + id)
    if state:
        return render_template('9-states.html', state=state, not_found=False)
    else:
        return render_template('9-states.html', not_found=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
