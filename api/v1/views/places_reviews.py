#!/usr/bin/python3
"""
Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.review import Review
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    gets all reviews with the place_id
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    all_reviews = place.reviews
    list_reviews = [obj.to_dict() for obj in all_reviews]
    return jsonify(list_reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """
    gets the review with the id
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def del_review(review_id):
    """
    deletes the review with the given id
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """
    it creates a new review
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if "text" not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    review_obj = request.get_json()
    user = storage.get("User", review_obj["user_id"])
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    review_obj["place_id"] = place_id
    if not user:
        abort(404)
    review = Review(**review_obj)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def put_review(review_id):
    """
    it updates a review by updating parameters
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        make_response(jsonify({"error": "Not a JSON"}), 400)
    request_body = request.get_json()

    for k, v in request_body.items():
        if k not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, k, v)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
