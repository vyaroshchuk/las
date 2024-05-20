from flask import Blueprint, Response, request, jsonify
from services.rental import borrow_request, retrieve_request, status_request
from services.users import auth

rental_bp = Blueprint('rental', __name__)


@rental_bp.route('/rental/borrow/<book_id>', methods=['POST'])
def borrow(book_id: str):
    user_id = auth(request.headers.get('Authorization'))
    if not user_id:
        return Response(status=401)
    borrow_request(book_id, user_id)
    return Response('Borrow request created', status=200)


@rental_bp.route('/rental/retrieve/<book_id>', methods=['POST'])
def retrieve(book_id):
    user_id = auth(request.headers.get('Authorization'))
    if not user_id:
        return Response(status=401)
    retrieve_request(book_id, user_id)
    return Response('Retrieve request created', status=200)


@rental_bp.route('/rental/status/<book_id>', methods=['GET'])
def status(book_id: str):
    user_id = auth(request.headers.get('Authorization'))
    if not user_id:
        return Response(status=401)
    return jsonify(status_request(book_id))
