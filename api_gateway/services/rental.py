import pika
import requests

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='borrow')
channel.queue_declare(queue='retrieve')


def borrow_request(book_id: str, user_id: int):
    channel.basic_publish(routing_key='borrow', body=f'{book_id}:{user_id}', exchange='')


def retrieve_request(book_id: str, user_id: int):
    channel.basic_publish(routing_key='retrieve', body=f'{book_id}:{user_id}', exchange='')


def status_request(book_id: str):
    r = requests.get(f'http://rental:5000/rental/status/{book_id}')

    if r.status_code == 404:
        return {'available': True}

    data = r.json()
    if data.get('retrieved_date') is None:
        return {
            'available': False,
            'borrowed_date': data.get('borrowed_date'),
        }

    return {
        'available': True,
        'retrieved_date': data.get('retrieved_date'),
    }

