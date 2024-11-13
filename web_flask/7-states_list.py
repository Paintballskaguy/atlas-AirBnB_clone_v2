#!/usr/bin/python3
"""
This script starts a Flask web application and displays a list of states.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(__exception):
    """Closes the storage session after each request."""
    storage.close()

@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays an HTML page with a list of all State objects sorted by name."""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
