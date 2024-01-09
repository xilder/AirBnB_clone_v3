#!/usr/bin/python3
"""
Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """
    gets all places from the database
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    all_places = city.places
    list_places = [obj.to_dict() for obj in all_places]
    return jsonify(list_places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """
    gets the place with the id
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def del_place(place_id):
    """
    deletes the place with the given id
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def post_place(city_id):
    """
    it creates a new place
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing a name"}), 400)
    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    place_obj = request.get_json()
    user = storage.get("User", place_obj["user_id"])
    place_obj["city_id"] = city_id
    if not user:
        abort(404)
    place = Place(**place_obj)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """
    it updates a place by updating parameters
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        make_response(jsonify({"error": "Not a JSON"}), 400)
    request_body = request.get_json()

    for k, v in request_body.items():
        if k not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, k, v)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
