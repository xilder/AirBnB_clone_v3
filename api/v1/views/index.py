#!/usr/bin/python3
"""
blueprint for app_views
"""
from api.v1.views import app_views
from models.engine.db_storage import classes
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """
    app status
    """
    return jsonify(status="OK")


@app_views.route("/stats", strict_slashes=False)
def stats():
    """
    stats of each class
    """
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
