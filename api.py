import peewee
from flask import jsonify
from flask_restful import Api, Resource, abort, inputs, reqparse
from models import Drivers, Events, Reports, Vehicles
from playhouse.shortcuts import model_to_dict

api = Api()


def abort_404(id=None):
    if id is None:
        abort(404)
    abort(404, message=str(id) + " doesn't exist")


def driver_parser_query(id=None):
    parser = reqparse.RequestParser()
    if id is not None:
        parser.add_argument(
            'id', default=id, type=int, help="Driver's id, {error_msg}")
    parser.add_argument(
        'name', required=True, help="Driver's name, {error_msg}")
    parser.add_argument(
        'surname', required=True, help="Driver's surname, {error_msg}")
    parser.add_argument(
        'birth', type=inputs.date, help="Driver's birth, {error_msg}")
    args = parser.parse_args(strict=True)
    if args.get('id') != id:
        abort(400, message="The ids don't match")
    id = Drivers.insert(args).execute()
    return jsonify(model_to_dict(Drivers.get_by_id(id)))


class Driver_id_API(Resource):
    def get(self, id):
        try:
            return jsonify(model_to_dict(Drivers.get_by_id(id)))
        except Drivers.DoesNotExist:
            abort_404(id)

    def put(self, id):
        try:
            Drivers.delete().where(Drivers.id == id).execute()
            return driver_parser_query(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))

    def delete(self, id):
        try:
            Drivers.delete().where(Drivers.id == id).execute()
            return '', 204
        except Drivers.DoesNotExist:
            abort_404(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(Driver_id_API, '/api/drivers/<int:id>')


class Driver_all_API(Resource):
    def get(self):
        try:
            query = Drivers.select().order_by(Drivers.id)
            return jsonify([model_to_dict(row) for row in query])
        except Drivers.DoesNotExist:
            abort_404()

    def post(self):
        try:
            return driver_parser_query()
        except peewee.DataError as e:
            abort(400, message=(str(e)))


api.add_resource(Driver_all_API, '/api/drivers/')


def event_parser_query(id=None):
    parser = reqparse.RequestParser()
    if id is not None:
        parser.add_argument(
            'id', default=id, type=int, help="Event's id, {error_msg}")
    parser.add_argument(
        'description', required=True, help="Event's description, {error_msg}")
    args = parser.parse_args(strict=True)
    if args.get('id') != id:
        abort(400, message="The ids don't match")
    id = Events.insert(args).execute()
    return jsonify(model_to_dict(Events.get_by_id(id)))


class Event_id_API(Resource):
    def get(self, id):
        try:
            return jsonify(model_to_dict(Events.get_by_id(id)))
        except Events.DoesNotExist:
            abort_404(id)

    def put(self, id):
        try:
            Events.delete().where(Events.id == id).execute()
            return event_parser_query(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))

    def delete(self, id):
        try:
            Events.delete().where(Events.id == id).execute()
            return '', 204
        except Events.DoesNotExist:
            abort_404(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(Event_id_API, '/api/events/<int:id>')


class Event_all_API(Resource):
    def get(self):
        try:
            query = Events.select().order_by(Events.id)
            return jsonify([model_to_dict(row) for row in query])
        except Events.DoesNotExist:
            abort_404()

    def post(self):
        try:
            return event_parser_query()
        except peewee.DataError as e:
            abort(400, message=(str(e)))


api.add_resource(Event_all_API, '/api/events/')


def report_parser_query(id=None):
    parser = reqparse.RequestParser()
    if id is not None:
        parser.add_argument(
            'id', default=id, type=int, help="Report's id, {error_msg}")
    parser.add_argument('driver', type=int, help="Driver, {error_msg}")
    parser.add_argument('vehicle', type=int, help="Vehicle, {error_msg}")
    parser.add_argument('lat', type=float, help="Latitude, {error_msg}")
    parser.add_argument('lon', type=float, help="Longitude, {error_msg}")
    parser.add_argument('alt', type=float, help="Altitude, {error_msg}")
    parser.add_argument('speed', type=float, help="Speed, {error_msg}")
    parser.add_argument('event', type=int, help="Event, {error_msg}")
    parser.add_argument('time', type=str, help="Time, {error_msg}")
    args = parser.parse_args(strict=True)
    if args.get('id') != id:
        abort(400, message="The ids don't match")
    id = Reports.insert(args).execute()
    return jsonify(model_to_dict(Reports.get_by_id(id)))


class Report_id_API(Resource):
    def get(self, id):
        try:
            return jsonify(model_to_dict(Reports.get_by_id(id)))
        except Reports.DoesNotExist:
            abort_404(id)

    def put(self, id):
        try:
            Reports.delete().where(Reports.id == id).execute()
            return report_parser_query(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))

    def delete(self, id):
        try:
            Reports.delete().where(Reports.id == id).execute()
            return '', 204
        except Reports.DoesNotExist:
            abort_404(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(Report_id_API, '/api/reports/<int:id>')


class Report_all_API(Resource):
    def get(self):
        try:
            query = Reports.select().order_by(Reports.id)
            return jsonify([model_to_dict(row) for row in query])
        except Reports.DoesNotExist:
            abort_404()

    def post(self):
        try:
            return report_parser_query()
        except peewee.DataError as e:
            abort(400, message=(str(e)))
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(Report_all_API, '/api/reports/')


def vehicle_parser_query(id=None):
    parser = reqparse.RequestParser()
    if id is not None:
        parser.add_argument(
            'id', default=id, type=int, help="Vehicle's id, {error_msg}")
    parser.add_argument(
        'plate', required=True, help="Vehicle's plate, {error_msg}")
    parser.add_argument(
        'description', help="Vehicle's description, {error_msg}")
    args = parser.parse_args(strict=True)
    if args.get('id') != id:
        abort(400, message="The ids don't match")
    id = Vehicles.insert(args).execute()
    return jsonify(model_to_dict(Vehicles.get_by_id(id)))


class Vehicle_id_API(Resource):
    def get(self, id):
        try:
            return jsonify(model_to_dict(Vehicles.get_by_id(id)))
        except Vehicles.DoesNotExist:
            abort_404(id)

    def put(self, id):
        try:
            Vehicles.delete().where(Vehicles.id == id).execute()
            return vehicle_parser_query(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))

    def delete(self, id):
        try:
            Vehicles.delete().where(Vehicles.id == id).execute()
            return '', 204
        except Vehicles.DoesNotExist:
            abort_404(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(Vehicle_id_API, '/api/vehicles/<int:id>')


class Vehicle_all_API(Resource):
    def get(self):
        try:
            query = Vehicles.select().order_by(Vehicles.id)
            return jsonify([model_to_dict(row) for row in query])
        except Vehicles.DoesNotExist:
            abort_404()

    def post(self):
        try:
            return vehicle_parser_query()
        except peewee.DataError as e:
            abort(400, message=(str(e)))


api.add_resource(Vehicle_all_API, '/api/vehicles/')
