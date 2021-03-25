from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.urls import reverse

# TODO: добавить ошибку 404, добавить ошибку при попытке запостить пустой отзыв


def index(request):
    return render(request, 'shop/index.html')


def catalogue(request):
    products = Product.objects.all()
    return render(request, 'shop/catalogue.html', {'products': products})


def get_product(request, product_id):
    product = Product.objects.get(id=product_id)
    reviews = Review.objects.filter(product_key=product_id)

    return render(request, 'shop/single_product.html', {'product': product, 'reviews': reviews[::-1]})


def post_review(request, product_id):
    product = Product.objects.get(id=product_id)
    new_review = Review(product_key=product, review_text=request.POST['text'], rating=4, author='dude').save()  # заглушки в виде фиксированного рейтинга и имени


    return HttpResponseRedirect(reverse('product_by_id', kwargs={'product_id': product.id}))