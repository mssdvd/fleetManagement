from flask import jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields
from models import Report
from playhouse.shortcuts import model_to_dict


class ReportSchema(Schema):
    id = fields.Int()
    trip = fields.Int(required=True)
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    alt = fields.Float(required=True)
    speed = fields.Float(required=True)
    event = fields.Int(required=True)
    time = fields.DateTime(required=True)


def report_validator(data, id=None):
    valid_data, errors = ReportSchema().load(data)
    if not errors:
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        id = Report.insert(valid_data).execute()
        return jsonify(model_to_dict(Report.get_by_id(id)))
    else:
        return jsonify(message=errors), 400


class ReportAPI(MethodView):
    def delete(self, id):
        Report.delete().where(Report.id == id).execute()
        return '', 204

    def get(self, id):
        if id is None:
            query = Report.select().order_by(Report.id)
            return jsonify([model_to_dict(row) for row in query])
        else:
            return jsonify(model_to_dict(Report.get_by_id(id)))

    def post(self):
        data = request.get_json(force=True)
        return report_validator(data)

    def put(self, id):
        data = request.get_json(force=True)
        if data.get('id') != id and id is None:
            return jsonify(message="The ids don't match"), 400
        Report.delete().where(Report.id == id).execute()
        return report_validator(data)
