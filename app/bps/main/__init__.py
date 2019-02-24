
from flask import Blueprint


main = Blueprint("main", __name__)

blueprint = main

__bp_prefix__ = "/"

from . import view
