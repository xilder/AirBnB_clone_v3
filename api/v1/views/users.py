#!/usr/bin/python3
"""
State module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.user import User
from models import storage


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """
    gets all users from the database
    """
    all_users = storage.all("User").values()
    list_users = [obj.to_dict() for obj in all_users]
    return jsonify(list_users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """
    gets the user with the id
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def del_user(user_id):
    """
    deletes the user with the given id
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """
    it creates a new user
    """
    if not request.get_json():
        return make_request(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in request.get_json():
        return make_request(jsonify({"error": "Missing email"}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    user_obj = request.get_json()
    user = User(**user_obj)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """
    it updates a user by updating parameters
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_request(jsonify({"error": "Not a JSON"}), 400)
    request_body = request.get_json()

    for k, v in request_body.items():
        if k not in ["id", "email" "created_at", "updated_at"]:
            setattr(user, k, v)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
