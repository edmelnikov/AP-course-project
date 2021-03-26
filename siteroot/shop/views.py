from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from django.urls import reverse
from  django.contrib.auth import login, logout, authenticate
from .forms import LoginForm

# TODO: добавить ошибку 404, добавить ошибку при попытке запостить пустой отзыв


def index(request):
	if request.user.is_authenticated:  # проверка на аутентификацию пользователя
		name = request.user.username
	else:
		name = 'Аноним'

	return render(request, 'shop/index.html', {'username_name': name})


def catalogue(request):
    products = Product.objects.all()
    return render(request, 'shop/catalogue.html', {'products': products})


def get_product(request, product_id):
	try:
		product = Product.objects.get(id=product_id)
	except:
		raise Http404('Товар не найден :(')
	
	reviews = Review.objects.filter(product_key=product_id)
	
	return render(request, 'shop/single_product.html', {'product': product, 'reviews': reviews[::-1]})


def print_review_error(request, product_id):
	return render(request, 'shop/comment_error.html', {'product_id': product_id})


def post_review(request, product_id):
	try:
		product = Product.objects.get(id=product_id)
	except:
		raise Http404('Товар не найден :(')
	if len(request.POST['text']) != 0:
		new_review = Review(product_key=product, review_text=request.POST['text'], rating=4, author='dude').save()  # заглушки в виде фиксированного рейтинга и имени
	elif request.POST['text'] == '':
		print_review_error(request, product_id)
	return HttpResponseRedirect(reverse('product_by_id', kwargs={'product_id': product.id}))


def register_page(request):
	return render(request, 'shop/register.html')


def log_in_page(request):

	if request.method == 'POST':  # переданы данные форм
		logout(request)  # ?
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:  # если пользователь с таким логином и паролем существует
				login(request, user)  # "прикрепляем" аутентифицированного пользователя к текущей сессии

				return redirect(reverse('index'))

			else:  # если пользователя такого нет
				form.add_error(None, 'No such user!')

	elif request.method == 'GET':  # обычный запрос страницы
		form = LoginForm()

	return render(request, 'shop/login.html', {'form': form})