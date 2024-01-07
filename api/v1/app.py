#!/usr/bin/python3
"""
main api app
"""
from api.v1.views import app_views
from flask import Flask
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from flask import jsonify
from flask import make_response
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(obj):
    """
    closes storage
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """ Loads a custom 404 page not found """
    return make_response(jsonify(error="Not found"), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=int(port), debug=True, threaded=True)
