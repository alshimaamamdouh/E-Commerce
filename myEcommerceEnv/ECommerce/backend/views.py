from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
   #template = loader.get_template('backend/index.html')
   #return HttpResponse(template.render())
   data = {'name':'alshimaa', 'job':'engineer'}
   return render(request, 'backend/index.html', data)
