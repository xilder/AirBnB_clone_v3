#!/usr/bin/python3
"""
main api app
"""
from flask import Flask
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

app = Flask(__name__)


@app.route("/api/v1/status", strict_slashes=False)
def status():
    """
    app status
    """
    return {"status": "OK"}


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(debug=True, host=host, port=int(port))

