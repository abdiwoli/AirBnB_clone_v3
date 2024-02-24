#!/usr/bin/python3
""" api/v1/views/cities.py """
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('/states/<sid>/cities', methods=['GET'], strict_slashes=False)
def ret_cities(sid):
    """ list cities by state """
    s = storage.get(State, sid)
    if s:
        s = s.to_dict()
        all = []
        for k, v in storage.all(City).items():
            if v.state_id == s.id:
                all.append(v.to_dict())
        return jsonify(all)
    return abort(404)


@app_views.route('/states/<sid>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities(sid):
    """ create new city for existing state """
    s = storage.get(State, sid)
    if not s:
        abort(404)
    try:
        dict_json = request.get_json()
    except Exception as e:
        abort(404, description=f"Not a JSON")

    if 'name' not in dict_json:
        abort(404, description=f"Missing name")
    c = City(**dict_json)
    storage.new(c)
    storage.save()
    return jsonify(c.to_dict()), 201


@app_views.route('/cities/<sid>', methods=['GET'], strict_slashes=False)
def get_cities(sid):
    """ get cities without state """
    s = storage.get(City, sid)
    if s:
        s = s.to_dict()
        return jsonify(s)
    return abort(404)


@app_views.route('/cities/<sid>', methods=['DELETE'], strict_slashes=False)
def delete_cities(sid):
    """ delete city """
    s = storage.get(City, sid)
    if s:
        storage.delete(s)
        return jsonify({}), 200
    return abort(404)


@app_views.route('/cities/<sid>', methods=['PUT'], strict_slashes=False)
def update_cities(sid):
    """ update city """
    city = storage.get(City, sid)
    if not city:
        return abort(404)
    try:
        dict_json = request.get_json()
    except Exception as e:
        abort(404, description=f"Not a JSON")

    if 'name' not in dict_json:
        abort(404, description=f"Missing name")
    ignore = ['updated_at', 'created_at', 'id', 'state_id']
    for key, value in dict_json.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
