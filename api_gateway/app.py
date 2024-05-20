from flask import Flask
from api import users_bp
from api import books_bp
from api import rental_bp

app = Flask(__name__)

app.register_blueprint(users_bp)
app.register_blueprint(books_bp)
app.register_blueprint(rental_bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
