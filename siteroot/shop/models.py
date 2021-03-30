from django.db import models
from django.db.models import *
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

# Product.objects.get(<some parameters>)
# Product.objects.all()
User = get_user_model()


class Product(Model):
	title = CharField(max_length=50)
	price = IntegerField()
	# in_stock = BooleanField()
	color = CharField(max_length=50, default=None)
	description = TextField(max_length=2048)
	materials = CharField(max_length=50)
	image = models.ImageField(blank=True, null=True)
	def __str__(self):  # Blog.objects.all() returns the title
		return str(self.title)


class Review(Model):
	product_key = ForeignKey(Product, on_delete=CASCADE)
	author = CharField(max_length=50)
	review_text = TextField()
	created_at = DateTimeField(auto_now_add=True)
	rating = IntegerField()

	def __str__(self):
		return str(self.author)


class CartProd(Model):
	user = ForeignKey(User, on_delete=CASCADE, null=True)
	cart = ForeignKey('Cart', on_delete=CASCADE, related_name='related_cart')
	product = ForeignKey(Product, on_delete=CASCADE, null=True)
	quantity = PositiveIntegerField(default=1)
	total_price = PositiveIntegerField(default=0)
	object_id = PositiveIntegerField()

	def __str__(self):
		return str(self.product.title)

	def calc(self):
		self.total_price = self.get_product().price * self.quantity
		super().save()

	def get_product(self):
		return Product.objects.get(id=self.object_id)


class Cart(Model):
	owner = ForeignKey(User, null=True, on_delete=CASCADE)
	products = ManyToManyField(CartProd, blank=True, related_name='related_products')
	final_price = PositiveIntegerField(default=0)
	for_unauthorized = BooleanField(default=False)

	def __str__(self):
		return str(self.id)


class Featured(Model):
	owner = ForeignKey(User, on_delete=CASCADE)
	products = ManyToManyField(Product, blank=True)

	def __str__(self):
		return str(self.id)
