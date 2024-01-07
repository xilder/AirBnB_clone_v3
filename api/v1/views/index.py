#!/usr/bin/bash
"""
blueprint for app_views
"""
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """
    app status
    """
    return {"status": "OK"}
