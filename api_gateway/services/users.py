from typing import Tuple
from data import redis_client
import requests

USERS_HOST = 'http://users:5000'


def sign_up_request(username: str, password: str) -> Tuple[str, int]:
    r = requests.post(f'{USERS_HOST}/sign_up/{username}/{password}')
    if r.status_code != 200:
        return f'Failed to sign up user: {r.text}', r.status_code
    return f'Successfully signed up user: {username}', 200


def sign_in_request(username: str, password: str) -> Tuple[str, int]:
    r = requests.post(f'{USERS_HOST}/sign_in/{username}/{password}')
    if r.status_code != 200:
        return f'Failed to sign in user: {r.text}', r.status_code
    return r.text, 200


def sign_out_request(auth_token: str) -> Tuple[str, int]:
    r = requests.post(f'{USERS_HOST}/sign_out/{auth_token}')
    return r.text, r.status_code


def auth(token: str, check_admin=False):
    if token is None:
        return None
    user_id = int(redis_client.get(token) or 0)
    if not user_id or (check_admin and user_id != 1):
        return None
    else:
        return user_id
