#!/usr/bin/python3
"""places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from datetime import datetime
import uuid


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_places_by_city(city_id):
    '''list names of all Place selected idof the city'''
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    places = [obj.to_dict() for obj in storage.all(Place).values()
                   if city_id == obj.city_id]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    '''Retrieves a Place object'''
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a Place of after finding by city'''
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Creates a new Place'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    city_obj = storage.get(Place, city_id)
    if not city_obj:
        abort(404)
    places = []
    new_place = Place(name=request.json['name'],
                      user_id=request.json['user_id'], city_id=city_id)
    user_obj  = storage.get(User, new_place.user_id)
    if not user_obj:
        abort(404)
    storage.new(new_place)
    storage.save()
    places.append(new_place.to_dict())
    return jsonify(places[0]), 201
