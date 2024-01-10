#!/usr/bin/python3
"""
Review module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.review import Review
from models import storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_places_amenities(place_id):
    """
    gets all reviews with the place_id
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    all_amenities = place.amenities
    list_amenities = [obj.to_dict() for obj in all_amenities]
    return jsonify(list_amenities)



@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def del_places_amenities(place_id, amenity_id):
    """
    deletes the amenities in a place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def post_places_amenities(place_id, amenity_id):
    """
    it adds a new amenity to a place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
