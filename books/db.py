import pymongo

mongo_client = pymongo.MongoClient("mongodb://mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0")
db = mongo_client["library"]
collection = db["books"]