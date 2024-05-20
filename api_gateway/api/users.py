from flask import Blueprint, Response

from services.users import sign_up_request, sign_in_request, sign_out_request

users_bp = Blueprint('users', __name__)


@users_bp.route('/sign_up/<username>/<password>', methods=['POST'])
def sign_up(username: str, password: str):
    msg, status = sign_up_request(username, password)
    return Response(msg, status)


@users_bp.route('/sign_in/<username>/<password>', methods=['POST'])
def sign_in(username: str, password: str):
    msg, status = sign_in_request(username, password)
    print(msg, status)
    return Response(msg, status)


@users_bp.route('/sign_out/<auth_token>', methods=['POST'])
def sign_out(auth_token):
    msg, status = sign_out_request(auth_token)
    return Response(msg, status)
