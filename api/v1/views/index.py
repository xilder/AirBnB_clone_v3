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
    return {"status": "OK"}

@app_views.route("/stats", strict_slashes=False)
def stats():
    """
    stats of each class
    """
    all_stat = {}
    for cls in classes:
        all_stat[cls.lower()] = storage.count(classes[cls])
    return jsonify(all_stat)
