#!/usr/bin/python3
"""
api/v1/views/places.py documentation
"""
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def ret_places(city_id):
    """ list places by cities """
    c = storage.get(City, city_id)
    if c:
        all = []
        for v in storage.all(Place).values():
            if v.city_id == c.id:
                all.append(v.to_dict())
        return jsonify(all)
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_places(city_id):
    """ create new place for existing city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        dict_json = request.get_json()
    except Exception as e:
        abort(404, "Not a JSON")

    if 'name' not in dict_json:
        abort(404, description=f"Missing name")
    c = Place(**dict_json)
    c.city_id = city.id
    storage.new(c)
    storage.save()
    return jsonify(c.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places(place_id):
    """ get place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete place """
    s = storage.get(Place, place_id)
    if s:
        storage.delete(s)
        return jsonify({}), 200
    return abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_places(place_id):
    """ update city """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    try:
        dict_json = request.get_json()
    except Exception as e:
        abort(404, "Not a JSON")

    if 'name' not in dict_json:
        abort(404, "Missing name")
    ignore = ['updated_at', 'created_at', 'id', 'state_id']
    for key, value in dict_json.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
