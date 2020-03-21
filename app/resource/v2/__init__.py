from flask import Blueprint

blueprint = Blueprint('v2', __name__, url_prefix='/v2')

from app.entity import *
from . import dashboard


