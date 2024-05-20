from uuid import uuid4

import redis
from flask import Flask, Response

from db import User, session

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route('/sign_in/<username>/<password>', methods=['POST'])
def sign_in(username: str, password: str):
    user = session.query(User).filter_by(username=username, password=password).first()
    if not user:
        return Response('Incorrect username or password', status=401)
    auth_token = str(uuid4())
    redis_client.set(auth_token, user.id, ex=3600)
    return Response(auth_token, status=200)


@app.route('/sign_up/<username>/<password>', methods=['POST'])
def sign_up(username: str, password: str):
    session.add(User(username=username, password=password))
    session.commit()
    return Response('Success', status=200)


@app.route('/sign_out/<auth_token>', methods=['POST'])
def sign_out(auth_token):
    if not redis_client.exists(auth_token):
        return Response('Incorrect auth_token', status=401)
    redis_client.delete(auth_token)
    return Response('Success', status=200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
