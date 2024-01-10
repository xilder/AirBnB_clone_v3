#!/usr/bin/python3
"""
main api app
"""
from api.v1.views import app_views
from flask import Flask
import models
from flask import jsonify
from flask import make_response
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


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
