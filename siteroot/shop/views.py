from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from django.urls import reverse
from  django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, SignupForm
from  django.contrib.auth.models import User


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


def single_product_page(request, product_id):
	try:
		product = Product.objects.get(id=product_id)
	except:
		raise Http404('Товар не найден :(')
	reviews = Review.objects.filter(product_key=product_id)

	text_error = None
	rating_error = None
	if request.method == 'POST':
		text = request.POST['text']
		rating = request.POST['rating']
		if not text or text.isspace():
			text_error = 'Пожалуйста, напишите отзыв'

		if int(rating) == 0:
			rating_error = 'Пожалуйста, оцените товар'

		if rating_error is not None or text_error is not None:
			return render(request, 'shop/single_product.html', {'product': product,
																'reviews': reviews[::-1],
																'text_error': text_error,
																'rating_error': rating_error})
		else:
			new_review = Review(product_key=product, review_text=text, rating=rating,
								author=request.user.username).save()
			return HttpResponseRedirect(reverse('product_by_id', kwargs={'product_id': product.id}))

	else: # GET
		return render(request, 'shop/single_product.html', {'product': product,
														'reviews': reviews[::-1],
														'text_error': text_error,
														'rating_error': rating_error})


def sign_up_page(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			logout(request)
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			password_confirm = form.cleaned_data['password_confirm']
			if User.objects.filter(username=username).exists():
				form.add_error('username', 'This user already exists')

			elif password != password_confirm:
				form.add_error('password_confirm', 'Mismatch')
			else:
				new_user = User.objects.create_user(username=username, email=email, password=password)
				login(request, new_user)
				return redirect(reverse('index'))

	elif request.method == 'GET':
		form = SignupForm()

	return render(request, 'shop/signup.html', {'form': form})


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


def log_out(request):
	if request.user.is_authenticated:
		logout(request)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # возвращение на ту же страницу, из которой был совершен запрос

