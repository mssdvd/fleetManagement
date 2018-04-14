from flask import jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields
from models import Trip
from playhouse.shortcuts import model_to_dict


class TripSchema(Schema):
    id = fields.Int()
    driver = fields.Int(required=True)
    vehicle = fields.Int(required=True)
    dest_lat = fields.Float(required=True)
    dest_lon = fields.Float(required=True)
    dep_time = fields.DateTime(required=True)
    ret_time = fields.DateTime()


def trip_validator(data, id=None):
    valid_data, errors = TripSchema().load(data)
    if not errors:
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        id = Trip.insert(valid_data).execute()
        return jsonify(model_to_dict(Trip.get_by_id(id)))
    else:
        return jsonify(message=errors), 400


class TripAPI(MethodView):
    def delete(self, id):
        Trip.delete().where(Trip.id == id).execute()
        return '', 204

    def get(self, id):
        if id is None:
            query = Trip.select().order_by(Trip.id)
            return jsonify([model_to_dict(row) for row in query])
        else:
            return jsonify(model_to_dict(Trip.get_by_id(id)))

    def post(self):
        data = request.get_json(force=True)
        return trip_validator(data)

    def put(self, id):
        data = request.get_json(force=True)
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        Trip.delete().where(Trip.id == id).execute()
        return trip_validator(data)
