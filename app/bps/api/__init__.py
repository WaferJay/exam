
from flask import Blueprint

from .result.json_result import JSONResult, ResultCode, json_result

api = Blueprint("api", __name__)


from . import auth
del auth

import logging
_logger = logging.getLogger(__name__)
del logging


@api.errorhandler(Exception)
@json_result
def _unhandled_exception(error):
    _logger.exception("Unhandled exception", exc_info=error)
    return JSONResult(ResultCode.UNHANDLED_EXCEPTION, exception=error)


blueprint = api
__bp_prefix__ = '/api'
