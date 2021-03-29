from django.views.generic import View
from .models import *


class CartMixin(View):
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			cart = Cart.objects.filter(owner=request.user).first()
			if not cart:
				cart = Cart.objects.create(owner=request.user)
		else:
			cart = Cart.objects.filter(for_unauthorized=True).first()
			if not cart:
				cart = Cart.objects.create(for_unauthorized=True)
		self.cart = cart
		return super().dispatch(request, *args, **kwargs)


class FeaturedMixin(View):
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			featured = Featured.objects.filter(owner=request.user).first()
			if not featured:
				featured = Featured.objects.create(owner=request.user)
			self.featured = featured
		return super().dispatch(request, *args, **kwargs)
