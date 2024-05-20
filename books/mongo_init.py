import pymongo

client = pymongo.MongoClient("mongodb://mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0")
db_names = client.list_database_names()
if 'library' not in db_names:
    db = client['library']
    books_collection = db['books']
    books = [
        {"title": "To Kill a Mockingbird", "genre": "Fiction", "author": "Harper Lee", "year": 1960},
        {"title": "1984", "genre": "Dystopian", "author": "George Orwell", "year": 1949},
        {"title": "Pride and Prejudice", "genre": "Romance", "author": "Jane Austen", "year": 1813},
        {"title": "The Great Gatsby", "genre": "Fiction", "author": "F. Scott Fitzgerald", "year": 1925},
        {"title": "Moby-Dick", "genre": "Adventure", "author": "Herman Melville", "year": 1851},
        {"title": "War and Peace", "genre": "Historical", "author": "Leo Tolstoy", "year": 1869},
        {"title": "The Catcher in the Rye", "genre": "Fiction", "author": "J.D. Salinger", "year": 1951},
        {"title": "The Hobbit", "genre": "Fantasy", "author": "J.R.R. Tolkien", "year": 1937},
        {"title": "Brave New World", "genre": "Dystopian", "author": "Aldous Huxley", "year": 1932},
        {"title": "The Odyssey", "genre": "Epic", "author": "Homer", "year": -800}  # Approximate year
    ]

    result = books_collection.insert_many(books)
