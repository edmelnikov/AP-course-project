from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from  django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import LoginForm, SignupForm
from  django.contrib.auth.models import User
from .mixins import *
from datetime import datetime




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


def recalculate_final_price(cart):
	cart_data = cart.products.aggregate(models.Sum('total_price'), models.Count('id'))
	if cart_data.get('total_price__sum'):
		cart.final_price = cart_data['total_price__sum']
	else:
		cart.final_price = 0
	cart.total_products = cart_data['id__count']
	cart.save()


class AddToCartView(CartMixin, View):
	def get(self, request, *args, **kwargs):
		product_id = kwargs.get('product_id')
		product = Product.objects.get(id=product_id)
		cart_prod, created = CartProd.objects.get_or_create(user=self.cart.owner, cart=self.cart,
															object_id=product_id)
		if created:
			cart_prod.calc()
			self.cart.products.add(cart_prod)
		recalculate_final_price(self.cart)
		return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):
	def get(self, request, *args, **kwargs):
		product_id = kwargs.get('product_id')
		product = Product.objects.get(id=product_id)
		cart_prod = CartProd.objects.get(user=self.cart.owner, cart=self.cart, object_id=product.id)
		self.cart.products.remove(cart_prod)
		cart_prod.delete()
		recalculate_final_price(self.cart)
		return HttpResponseRedirect('/cart/')


class ChangeQuantityView(CartMixin, View):
	def post(self, request, *args, **kwargs):
		product_id = kwargs.get('product_id')
		product = Product.objects.get(id=product_id)
		cart_prod = CartProd.objects.get(user=self.cart.owner, cart=self.cart, object_id=product.id)
		#print(request.POST)
		quantity = int(request.POST.get('quantity'))
		cart_prod.quantity = quantity
		cart_prod.calc()
		cart_prod.save()
		recalculate_final_price(self.cart)
		return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
	def get(self, request):
		return render(request, 'shop/cart.html', {'cart': self.cart})


class AddToFeaturedView(FeaturedMixin, View):
	def get(self, request, *args, **kwargs):
		print(1)
		product_id = kwargs.get('product_id')
		print(1)
		product = Product.objects.get(id=product_id)
		print(1)
		self.featured.products.add(product)
		print(1)
		return HttpResponseRedirect('/' + str(product_id))


class DeleteFromFeatured(FeaturedMixin, View):
	def get(self, request, *args, **kwargs):
		product_id = kwargs.get('product_id')
		product = Product.objects.get(id=product_id)
		self.featured.products.remove(product)
		return HttpResponseRedirect('/featured/')


class FeaturedView(FeaturedMixin, View):
	def get(self, request):
		return render(request, 'shop/featured.html', {'featured': self.featured})
