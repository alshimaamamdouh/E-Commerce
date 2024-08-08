
from pymongo import MongoClient
from django.db import models

#MongoDB connection
url = 'mongodb://localhost:27017'
client = MongoClient(url)
db = client["test"]

#set new collection
products = db['product']
