from datetime import datetime

import pika
from db import RentalRecord, session, RentalStatus

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))


def callback_borrow(ch, method, properties, body):
    book_id, user_id = body.decode('utf-8').split(':')
    rr = RentalRecord(
        book_id=book_id,
        user_id=int(user_id),
        status=RentalStatus.borrowed,
        borrowed_date=datetime.now(),
    )

    session.add(rr)
    session.commit()
    print('Borrowed:', rr.book_id, rr.user_id, rr.status, rr.borrowed_date, rr.retrieved_date)


def callback_retrieve(ch, method, properties, body):
    book_id, user_id = body.decode('utf-8').split(':')
    rr = session.query(
        RentalRecord
    ).filter_by(user_id=int(user_id), book_id=book_id).order_by(RentalRecord.borrowed_date.desc()).first()
    rr.status = RentalStatus.retrieved.value
    rr.retrieved_date = datetime.now()
    session.commit()
    print('Retrieved:', rr.book_id, rr.user_id, rr.status, rr.borrowed_date, rr.retrieved_date)


def mq_worker():
    channel = connection.channel()

    channel.queue_declare(queue='borrow')
    channel.queue_declare(queue='retrieve')

    channel.basic_consume(queue='borrow', on_message_callback=callback_borrow, auto_ack=True)
    channel.basic_consume(queue='retrieve', on_message_callback=callback_retrieve, auto_ack=True)

    channel.start_consuming()
