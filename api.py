import peewee
from flask import jsonify
from flask_restful import Api, Resource, abort, inputs, reqparse
from models import Event, Report, Role, User, Vehicle
from playhouse.shortcuts import model_to_dict

api = Api()


def abort_404(id=None):
    if id is None:
        abort(404)
    abort(404, message=str(id) + " doesn't exist")


def user_parser_query(id=None):
    parser = reqparse.RequestParser()
    if id is not None:
        parser.add_argument(
            'id', default=id, type=int, help="User's id, {error_msg}")
    parser.add_argument('name', required=True, help="User's name, {error_msg}")
    parser.add_argument(
        'surname', required=True, help="User's surname, {error_msg}")
    parser.add_argument(
        'birth', type=inputs.date, help="User's birth, {error_msg}")
    parser.add_argument(
        'role', required=True, type=int, help="User's  role, {error_msg}")
    args = parser.parse_args(strict=True)
    if args.get('id') != id:
        abort(400, message="The ids don't match")
    id = User.insert(args).execute()
    return jsonify(model_to_dict(User.get_by_id(id)))


class User_id_API(Resource):
    def get(self, id):
        try:
            return jsonify(model_to_dict(User.get_by_id(id)))
        except User.DoesNotExist:
            abort_404(id)

    def put(self, id):
        try:
            User.delete().where(User.id == id).execute()
            return user_parser_query(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))

    def delete(self, id):
        try:
            User.delete().where(User.id == id).execute()
            return '', 204
        except User.DoesNotExist:
            abort_404(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(User_id_API, '/api/user/<int:id>')


class User_all_API(Resource):
    def get(self):
        try:
            query = User.select().order_by(User.id)
            return jsonify([model_to_dict(row) for row in query])
        except User.DoesNotExist:
            abort_404()

    def post(self):
        try:
            return user_parser_query()
        except peewee.DataError as e:
            abort(400, message=(str(e)))
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(User_all_API, '/api/user/')


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
    id = Event.insert(args).execute()
    return jsonify(model_to_dict(Event.get_by_id(id)))


class Event_id_API(Resource):
    def get(self, id):
        try:
            return jsonify(model_to_dict(Event.get_by_id(id)))
        except Event.DoesNotExist:
            abort_404(id)

    def put(self, id):
        try:
            Event.delete().where(Event.id == id).execute()
            return event_parser_query(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))

    def delete(self, id):
        try:
            Event.delete().where(Event.id == id).execute()
            return '', 204
        except Event.DoesNotExist:
            abort_404(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(Event_id_API, '/api/event/<int:id>')


class Event_all_API(Resource):
    def get(self):
        try:
            query = Event.select().order_by(Event.id)
            return jsonify([model_to_dict(row) for row in query])
        except Event.DoesNotExist:
            abort_404()

    def post(self):
        try:
            return event_parser_query()
        except peewee.DataError as e:
            abort(400, message=(str(e)))


api.add_resource(Event_all_API, '/api/event/')


def report_parser_query(id=None):
    parser = reqparse.RequestParser()
    if id is not None:
        parser.add_argument(
            'id', default=id, type=int, help="Report's id, {error_msg}")
    parser.add_argument('user', type=int, help="User, {error_msg}")
    parser.add_argument('vehicle', type=int, help="Vehicle, {error_msg}")
    parser.add_argument('lat', type=float, help="Latitude, {error_msg}")
    parser.add_argument('lon', type=float, help="Longitude, {error_msg}")
    parser.add_argument('alt', type=float, help="Altitude, {error_msg}")
    parser.add_argument('speed', type=float, help="Speed, {error_msg}")
    parser.add_argument('event', type=int, help="Event, {error_msg}")
    parser.add_argument('time', help="Time, {error_msg}")
    args = parser.parse_args(strict=True)
    if args.get('id') != id:
        abort(400, message="The ids don't match")
    id = Report.insert(args).execute()
    return jsonify(model_to_dict(Report.get_by_id(id)))


class Report_id_API(Resource):
    def get(self, id):
        try:
            return jsonify(model_to_dict(Report.get_by_id(id)))
        except Report.DoesNotExist:
            abort_404(id)

    def put(self, id):
        try:
            Report.delete().where(Report.id == id).execute()
            return report_parser_query(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))

    def delete(self, id):
        try:
            Report.delete().where(Report.id == id).execute()
            return '', 204
        except Report.DoesNotExist:
            abort_404(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(Report_id_API, '/api/report/<int:id>')


class Report_all_API(Resource):
    def get(self):
        try:
            query = Report.select().order_by(Report.id)
            return jsonify([model_to_dict(row) for row in query])
        except Report.DoesNotExist:
            abort_404()

    def post(self):
        try:
            return report_parser_query()
        except peewee.DataError as e:
            abort(400, message=(str(e)))
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(Report_all_API, '/api/report/')


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
    id = Vehicle.insert(args).execute()
    return jsonify(model_to_dict(Vehicle.get_by_id(id)))


class Vehicle_id_API(Resource):
    def get(self, id):
        try:
            return jsonify(model_to_dict(Vehicle.get_by_id(id)))
        except Vehicle.DoesNotExist:
            abort_404(id)

    def put(self, id):
        try:
            Vehicle.delete().where(Vehicle.id == id).execute()
            return vehicle_parser_query(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))

    def delete(self, id):
        try:
            Vehicle.delete().where(Vehicle.id == id).execute()
            return '', 204
        except Vehicle.DoesNotExist:
            abort_404(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(Vehicle_id_API, '/api/vehicle/<int:id>')


class Vehicle_all_API(Resource):
    def get(self):
        try:
            query = Vehicle.select().order_by(Vehicle.id)
            return jsonify([model_to_dict(row) for row in query])
        except Vehicle.DoesNotExist:
            abort_404()

    def post(self):
        try:
            return vehicle_parser_query()
        except peewee.DataError as e:
            abort(400, message=(str(e)))


api.add_resource(Vehicle_all_API, '/api/vehicle/')


def role_parser_query(id=None):
    parser = reqparse.RequestParser()
    if id is not None:
        parser.add_argument(
            'id', default=id, type=int, help="Role's id, {error_msg}")
    parser.add_argument(
        'role', required=True, help="Role's description, {error_msg}")
    args = parser.parse_args(strict=True)
    if args.get('id') != id:
        abort(400, message="The ids don't match")
    id = Role.insert(args).execute()
    return jsonify(model_to_dict(Role.get_by_id(id)))


class Role_id_API(Resource):
    def get(self, id):
        try:
            return jsonify(model_to_dict(Role.get_by_id(id)))
        except Role.DoesNotExist:
            abort_404(id)

    def put(self, id):
        try:
            Role.delete().where(Role.id == id).execute()
            return role_parser_query(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))

    def delete(self, id):
        try:
            Role.delete().where(Role.id == id).execute()
            return '', 204
        except Role.DoesNotExist:
            abort_404(id)
        except peewee.IntegrityError as e:
            abort(500, message=str(e))


api.add_resource(Role_id_API, '/api/role/<int:id>')


class Role_all_API(Resource):
    def get(self):
        try:
            query = Role.select().order_by(Role.id)
            return jsonify([model_to_dict(row) for row in query])
        except Role.DoesNotExist:
            abort_404()

    def post(self):
        try:
            return role_parser_query()
        except peewee.DataError as e:
            abort(400, message=(str(e)))


api.add_resource(Role_all_API, '/api/role/')
