from flask import Blueprint, jsonify
from sqlalchemy.sql.functions import current_user

from schemas import *
from models import *
from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth

blueprint = Blueprint("Rating",__name__)
auth = HTTPBasicAuth()


