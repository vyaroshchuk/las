import threading

from flask import Flask, Response, jsonify
from db import session, RentalRecord
from queue_worker import mq_worker

app = Flask(__name__)


@app.route('/rental/status/<book_id>', methods=['GET'])
def status(book_id: int):
    rental_record = session.query(
        RentalRecord
    ).filter_by(book_id=book_id).order_by(RentalRecord.borrowed_date.desc()).first()

    if not rental_record:
        return Response('Not found', status=404)

    return jsonify({
        'book_id': rental_record.book_id,
        'borrowed_date': rental_record.borrowed_date,
        'retrieved_date': rental_record.retrieved_date,
        'user_id': rental_record.user_id,
    })


if __name__ == "__main__":
    print('Creating mq thread')
    mq_thread = threading.Thread(target=mq_worker)
    mq_thread.start()
    print('Thread started')
    app.run(debug=True, host='0.0.0.0')
