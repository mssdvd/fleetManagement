from flask import jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields
from models import Message
from playhouse.shortcuts import model_to_dict


class MessageSchema(Schema):
    id = fields.Int()
    vehicle = fields.Int(required=True)
    company = fields.Int(require=True)
    to_vehicle = fields.Bool(require=True)
    message = fields.Str(require=True)
    time = fields.DateTime(require=True)


def message_validator(data, id=None):
    valid_data, errors = MessageSchema().load(data)
    if not errors:
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        id = Message.insert(valid_data).execute()
        return jsonify(model_to_dict(Message.get_by_id(id)))
    else:
        return jsonify(message=errors), 400


class MessageAPI(MethodView):
    def delete(self, id):
        Message.delete().where(Message.id == id).execute()
        return '', 204

    def get(self, id):
        if id is None:
            query = Message.select().order_by(Message.id)
            return jsonify([model_to_dict(row) for row in query])
        else:
            return jsonify(model_to_dict(Message.get_by_id(id)))

    def post(self):
        data = request.get_json(force=True)
        return message_validator(data)

    def put(self, id):
        data = request.get_json(force=True)
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        Message.delete().where(Message.id == id).execute()
        return message_validator(data)
