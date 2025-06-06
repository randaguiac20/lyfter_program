from flask.views import MethodView
from flask import jsonify, request
from validators.validator import reject_fields


class Login(MethodView):
    def __init__(self):
        pass
