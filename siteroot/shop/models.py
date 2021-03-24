from django.db import models
from django.db.models import *

# Product.objects.get(<some parameters>)
# Product.objects.all()

class Product(Model):
    title = CharField(max_length=50)
    price = IntegerField()
    in_stock = BooleanField()
    color = CharField(max_length=50, default=None)

    def __str__(self):  # Blog.objects.all() returns the title
        return str(self.title)


class ProductReview(Model):
    product_key = ForeignKey(Product, on_delete=CASCADE)

    author = CharField(max_length=50)
    review_text = TextField()
    created_at = DateTimeField(auto_now_add=True)
    rating = IntegerField()

    def __str__(self):
        return str(self.author)
