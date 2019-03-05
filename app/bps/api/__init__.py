from flask import Blueprint

from .result.json_result import JSONResult

api = Blueprint("api", __name__)

blueprint = api

__bp_prefix__ = '/api'

from . import auth
