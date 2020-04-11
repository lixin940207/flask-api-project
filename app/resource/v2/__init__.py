from flask import Blueprint

blueprint = Blueprint('v2', __name__, url_prefix='/v1')

from app.entity import *
from . import dashboard, mark, other, model, predict


