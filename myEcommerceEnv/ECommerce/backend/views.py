from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import products


def index(request):
   #template = loader.get_template('backend/index.html')
   #return HttpResponse(template.render())
   #data = {'name':'alshimaa', 'job':'engineer'}
   data = {'name':'Mobile', 'price':'123LE', 'seller_name':'global company'}
   products.insert_one(data)
   index_data = products.find()
   return render(request, 'backend/index.html',data)
