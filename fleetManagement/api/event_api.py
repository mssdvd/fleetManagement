from flask import jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields
from models import Event
from playhouse.shortcuts import model_to_dict


class EventSchema(Schema):
    id = fields.Int()
    description = fields.Str(required=True)


def event_validator(data, id=None):
    valid_data, errors = EventSchema().load(data)
    if not errors:
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        id = Event.insert(valid_data).execute()
        return jsonify(model_to_dict(Event.get_by_id(id)))
    else:
        return jsonify(message=errors), 400


class EventAPI(MethodView):
    def delete(self, id):
        Event.delete().where(Event.id == id).execute()
        return '', 204

    def get(self, id):
        if id is None:
            query = Event.select().order_by(Event.id)
            return jsonify([model_to_dict(row) for row in query])
        else:
            return jsonify(model_to_dict(Event.get_by_id(id)))

    def post(self):
        data = request.get_json(force=True)
        return event_validator(data)

    def put(self, id):
        data = request.get_json(force=True)
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        Event.delete().where(Event.id == id).execute()
        return event_validator(data)
