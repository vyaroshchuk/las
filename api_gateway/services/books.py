from json import loads

import requests

BOOKS_HOST = 'http://books:5000'


def books_request():
    r = requests.get(f'{BOOKS_HOST}/books')
    return loads(r.text)


def book_request(book_id: str):
    r = requests.get(f'{BOOKS_HOST}/book/{book_id}')
    return loads(r.text) if r.status_code == 200 else None, r.status_code


def book_add_request(data: dict):
    r = requests.post(f'{BOOKS_HOST}/book/add', json=data)
    return r.text


def book_delete_request(book_id: str):
    r = requests.post(f'{BOOKS_HOST}/book/delete/{book_id}')
    return r.text