from flask import Blueprint, Response, request, jsonify

from services.books import books_request, book_request, book_add_request, book_delete_request
from services.users import auth

books_bp = Blueprint('books', __name__)


@books_bp.route('/books', methods=['GET'])
def books():
    if auth(request.headers.get('Authorization')):
        books_list = books_request()
        return jsonify(books_list)
    else:
        return Response(status=401)


@books_bp.route('/book/<book_id>', methods=['GET'])
def book(book_id: str):
    if auth(request.headers.get('Authorization')):
        _book, status = book_request(book_id)
        if status == 404:
            return Response('Book not found', status=404)
        return jsonify(_book)
    else:
        return Response(status=401)


@books_bp.route('/book/add', methods=['POST'])
def book_add():
    if auth(request.headers.get('Authorization'), True):
        res = book_add_request(request.json)
        return Response(res, status=200)
    else:
        return Response(status=401)


@books_bp.route('/book/delete/<book_id>', methods=['POST'])
def books_delete(book_id):
    if auth(request.headers.get('Authorization'), True):
        res = book_delete_request(book_id)
        return Response(res, status=200)
    else:
        return Response(status=401)
