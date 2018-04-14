from flask import Blueprint

from .company_api import CompanyAPI
from .event_api import EventAPI
from .report_api import ReportAPI
from .role_api import RoleAPI
from .trip_api import TripAPI
from .user_api import UserAPI

api = Blueprint('api', __name__, url_prefix='/api')

user_view = UserAPI.as_view('user_api')
api.add_url_rule(
    '/user/', defaults={'id': None}, view_func=user_view, methods=['GET'])
api.add_url_rule('/user/', view_func=user_view, methods=['POST'])
api.add_url_rule(
    '/user/<int:id>', view_func=user_view, methods=['DELETE', 'GET', 'PUT'])

company_view = CompanyAPI.as_view('company_api')
api.add_url_rule(
    '/company/',
    defaults={'id': None},
    view_func=company_view,
    methods=['GET'])
api.add_url_rule('/company/', view_func=company_view, methods=['POST'])
api.add_url_rule(
    '/company/<int:id>',
    view_func=company_view,
    methods=['DELETE', 'GET', 'PUT'])

role_view = RoleAPI.as_view('role_api')
api.add_url_rule(
    '/role/', defaults={'id': None}, view_func=role_view, methods=['GET'])
api.add_url_rule('/role/', view_func=role_view, methods=['POST'])
api.add_url_rule(
    '/role/<int:id>', view_func=role_view, methods=['DELETE', 'GET', 'PUT'])

event_view = EventAPI.as_view('event_api')
api.add_url_rule(
    '/event/', defaults={'id': None}, view_func=event_view, methods=['GET'])
api.add_url_rule('/event/', view_func=event_view, methods=['POST'])
api.add_url_rule(
    '/event/<int:id>', view_func=event_view, methods=['DELETE', 'GET', 'PUT'])

report_view = ReportAPI.as_view('report_api')
api.add_url_rule(
    '/report/', defaults={'id': None}, view_func=report_view, methods=['GET'])
api.add_url_rule('/report/', view_func=report_view, methods=['POST'])
api.add_url_rule(
    '/report/<int:id>',
    view_func=report_view,
    methods=['DELETE', 'GET', 'PUT'])

trip_view = TripAPI.as_view('trip_api')
api.add_url_rule(
    '/trip/', defaults={'id': None}, view_func=trip_view, methods=['GET'])
api.add_url_rule('/trip/', view_func=trip_view, methods=['POST'])
api.add_url_rule(
    '/trip/<int:id>', view_func=trip_view, methods=['DELETE', 'GET', 'PUT'])
