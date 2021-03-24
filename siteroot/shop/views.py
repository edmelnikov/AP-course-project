from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):
    return render(request, 'shop/index.html')


def catalogue(request):
    products = Product.objects.all()
    return render(request, 'shop/catalogue.html', {'products': products})


def get_product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'shop/single_product.html', {'product': product})