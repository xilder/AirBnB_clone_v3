#!/usr/bin/python3
"""
Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """
    gets all amenities from the database
    """
    all_amenities = storage.all("Amenity").values()
    list_amenities = [obj.to_dict() for obj in all_amenities]
    return jsonify(list_amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """
    gets the amenity with the id
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def del_amenity(amenity_id):
    """
    deletes the amenity with the given id
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """
    it creates a new state
    """
    if not request.get_json():
        return make_request(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_request(jsonify({"error": "Missing name"}), 400)
    amenity_obj = request.get_json()
    amenity = Amenity(**amenity_obj)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
    it updates a state by updating parameters
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_request(jsonify({"error": "Not a JSON"}), 400)
    request_body = request.get_json()

    for k, v in request_body.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
