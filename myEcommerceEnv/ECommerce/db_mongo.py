import pymongo
import pymongo.mongo_client

url = 'mongodb://localhost:27017'
connect = pymongo.mongo_client(url)

db = connect["test"]