from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'main/index.html')

def mural(request):
    return render(request, 'mural/mural.html')
