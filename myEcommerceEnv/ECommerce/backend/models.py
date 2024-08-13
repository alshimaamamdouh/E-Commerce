
from pymongo import MongoClient
from django.db import models
from django.contrib.auth.models import User

""" #MongoDB connection
url = 'mongodb://localhost:27017'
client = MongoClient(url)
db = client["test"]

#set new collection
products = db['product'] """


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    category = models.CharField(max_length=255)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

