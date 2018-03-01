from django.shortcuts import render
from django.http import HttpResponse
from django.http import QueryDict

# Create your views here.


def home(request):
    return render(request, 'home.html')
