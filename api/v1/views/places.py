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
    city = storage.get("City", city_id)
    if not city:
        abort(404)
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


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places_by_id():
    """
    search places by id
    """
    list_places = []
    params = request.get_json()
    if not params:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if params and len(params):
        states = params.get("states", None)
        cities = params.get("cities", None)
        amenities = params.get("amenities", None)
    if not params or not len(params) or (
            not states and
            not cities and
            not amenities):
        places = storage.all("Place").values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)
    if states:
        states_obj = [storage.get("State", state_id) for state_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    for place in city.places:
                        list_places.append(place)

    if cities:
        cities_obj = [storage.get("City", city_id) for city_id in cities]
        for city in cities_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all("Place").values()
        amenities_obj = [storage.get("Amenity", amenity_id)
                for amenity_id in amenities]
        list_places = [place for place in list_places
                       if all([amenity in place.amenities
                               for amenity in amenities_obj])]
    new_list = []
    for place in list_places:
        place = place.to_dict()
        place.pop("amenities", None)
        new_list.append(place)
    return jsonify(new_list)

