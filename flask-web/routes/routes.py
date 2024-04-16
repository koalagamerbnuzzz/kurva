from flask import request, jsonify

from ..models import db, Key, User
from flask_jwt_extended import jwt_required, create_access_token, decode_token
from flask_security import login_required

from . import main

from json import load, dumps


@main.route('/login', methods=['GET'])
def validate():
    pass

@main.route('/register', methods=['GET'])
def validate():
    pass

@main.route('/auth', methods=['POST'])
def validate():
    pass

@login_required
@main.route('/checker', methods=['GET'])
def validate():
    pass



