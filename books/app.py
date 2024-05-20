from bson import ObjectId
from flask import Flask, Response, jsonify, request

from db import collection

app = Flask(__name__)


def unpack_id(doc):
    doc['id'] = str(doc["_id"])
    doc.pop('_id')


@app.route('/books', methods=['GET'])
def books():
    docs = []
    for doc in collection.find({}):
        unpack_id(doc)
        doc = {'id': doc['id'], 'title': doc['title'], 'genre': doc['genre']}
        docs.append(doc)
    return jsonify(docs)


@app.route('/book/<book_id>', methods=['GET'])
def book(book_id: str):
    _book = collection.find_one({"_id": ObjectId(book_id)})
    unpack_id(_book)
    return jsonify(_book)


@app.route('/book/add', methods=['POST'])
def book_add():
    doc = request.json
    if 'title' not in doc.keys() or 'genre' not in doc.keys() or 'author' not in doc.keys():
        return Response('Missing fields', 400)
    res = collection.insert_one(doc)
    return Response(str(res.inserted_id), 200)


@app.route('/book/delete/<book_id>', methods=['POST'])
def books_delete(book_id: str):
    book_id = ObjectId(book_id)
    res = collection.delete_one({"_id": book_id})
    if res.deleted_count == 0:
        return Response('Book not found', 404)
    return Response('Book deleted', 200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
