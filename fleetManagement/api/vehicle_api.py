from flask import jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields
from models import Vehicle
from playhouse.shortcuts import model_to_dict


class VehicleSchema(Schema):
    id = fields.Int()
    plate = fields.Str(required=True)
    description = fields.Str(required=True)


def vehicle_validator(data, id=None):
    valid_data, errors = VehicleSchema().load(data)
    if not errors:
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        id = Vehicle.insert(valid_data).execute()
        return jsonify(model_to_dict(Vehicle.get_by_id(id)))
    else:
        return jsonify(message=errors), 400


class VehicleAPI(MethodView):
    def delete(self, id):
        Vehicle.delete().where(Vehicle.id == id).execute()
        return '', 204

    def get(self, id):
        if id is None:
            query = Vehicle.select().order_by(Vehicle.id)
            return jsonify([model_to_dict(row) for row in query])
        else:
            return jsonify(model_to_dict(Vehicle.get_by_id(id)))

    def post(self):
        data = request.get_json(force=True)
        return vehicle_validator(data)

    def put(self, id):
        data = request.get_json(force=True)
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        Vehicle.delete().where(Vehicle.id == id).execute()
        return vehicle_validator(data)
