#!/usr/bin/python3
"""
This script starts a Flask web application to display filters for AirBnB.
"""

from flask import Flask, render_template, redirect, url_for
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)

@app.teardown_appcontext
def close_database(exception):
    """Close the database after each request."""
    storage.close()

@app.route("/", strict_slashes=False)
def index():
    """Redirects to the /hbnb_filters route."""
    return redirect(url_for('hbnb_filters'))

@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Renders the template displaying states with cities and amenities."""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    amenities = sorted(storage.all(Amenity).values(), key=lambda amenity: amenity.name)
    
    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
