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

@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displays an HTML page with a list of all states and their cities."""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('cities_by_states.html', states=states)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
