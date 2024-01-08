#!/usr/bin/python3
"""
State module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_states_cities(state_id):
    """
    gets cities by state_id
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    gets cities by state_id
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=False)
def del_city(city_id):
    """
    deletes the city with the given id
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_cities(state_id):
    """
    adds a city
    """
    if not request.get_json():
        return make_request(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_request(jsonify({"error": "Missing name"}), 400)
    city_obj = request.get_json()
    city = City(**city_obj)
    setattr(city, "state_id", state_id)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """
    updates a city
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_request(jsonify({"error": "Not a JSON"}), 400)
    request_body = request.get_json()

    for k, v in request_body.items():
        if k not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, k, v)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
