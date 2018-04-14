from flask import Blueprint, abort, jsonify

from .user_api import UserAPI

api = Blueprint('api', __name__, url_prefix='/api')

user_view = UserAPI.as_view('user_api')
api.add_url_rule(
    '/user/', defaults={'id': None}, view_func=user_view, methods=['GET'])
api.add_url_rule('/user/', view_func=user_view, methods=['POST'])
api.add_url_rule(
    '/user/<int:id>', view_func=user_view, methods=['DELETE', 'GET', 'PUT'])
