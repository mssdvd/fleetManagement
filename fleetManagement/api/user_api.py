from flask import jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields
from playhouse.shortcuts import model_to_dict
from werkzeug.security import generate_password_hash

from models import User


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    birth = fields.Date(required=True)
    employer = fields.Int(required=True)
    role = fields.Int(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)


def user_validator(data, id=None):
    valid_data, errors = UserSchema().load(data)
    if not errors:
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        valid_data['password'] = generate_password_hash(valid_data['password'])
        id = User.insert(valid_data).execute()
        return jsonify(
            model_to_dict(User.get_by_id(id), exclude=[User.password]))
    else:
        return jsonify(message=errors), 400


class UserAPI(MethodView):
    def delete(self, id):
        User.delete().where(User.id == id).execute()
        return '', 204

    def get(self, id):
        if id is None:
            if 'username' in request.args:
                query = User.get_or_none(
                    User.username == request.args.get('username'))
                if query is None:
                    result = query
                else:
                    result = query.id
                return jsonify(id=result)
            else:
                query = User.select().order_by(User.id)
                return jsonify([
                    model_to_dict(row, exclude=[User.password])
                    for row in query
                ])
        else:
            return jsonify(
                model_to_dict(User.get_by_id(id), exclude=[User.password]))

    def post(self, id):
        data = request.get_json(force=True)
        if 'password' in request.args:
            user = User.get_by_id(id)
            sended_password = data.get('password')
            return jsonify(result=user.check_password(sended_password))
        else:
            return user_validator(data)

    def put(self, id):
        data = request.get_json(force=True)
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        User.delete().where(User.id == id).execute()
        return user_validator(data)
