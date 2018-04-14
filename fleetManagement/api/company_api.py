from flask import jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields
from models import Company
from playhouse.shortcuts import model_to_dict


class CompanySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    location = fields.Str(required=True)


def company_validator(data, id=None):
    valid_data, errors = CompanySchema().load(data)
    if not errors:
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        id = Company.insert(valid_data).execute()
        return jsonify(model_to_dict(Company.get_by_id(id)))
    else:
        return jsonify(message=errors), 400


class CompanyAPI(MethodView):
    def delete(self, id):
        Company.delete().where(Company.id == id).execute()
        return '', 204

    def get(self, id):
        if id is None:
            query = Company.select().order_by(Company.id)
            return jsonify([model_to_dict(row) for row in query])
        else:
            return jsonify(model_to_dict(Company.get_by_id(id)))

    def post(self):
        data = request.get_json(force=True)
        return company_validator(data)

    def put(self, id):
        data = request.get_json(force=True)
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        Company.delete().where(Company.id == id).execute()
        return company_validator(data)
