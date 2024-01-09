#!/usr/bin/python3
"""
State module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """
    gets all states from the database
    """
    all_states = storage.all("State").values()
    list_states = [obj.to_dict() for obj in all_states]
    return jsonify(list_states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """
    gets the state with the id
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def del_state(state_id):
    """
    deletes the state with the given id
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """
    it creates a new state
    """
    if not request.get_json():
        return abort(400, "Not a JSON")
    if "name" not in request.get_json():
        return abort(400, "Missing a name")
    state_obj = request.get_json()
    state = State(**state_obj)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def put_state(state_id):
    """
    it updates a state by updating parameters
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return abort(400, "Not a JSON")
    request_body = request.get_json()

    for k, v in request_body.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
