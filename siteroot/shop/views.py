from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):
    return render(request, 'shop/index.html')


def catalogue(request):
    products = Product.objects.all()

    return render(request, 'shop/catalogue.html', {'products': products})