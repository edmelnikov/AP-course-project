from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('<int:product_id>', views.get_product, name='product_by_id'),  # how does it work
    path('<int:product_id>/post_review', views.post_review, name='post_review'),
	path('<int:product_id>/post_review/error', views.print_review_error, name='print_error'),
    path('register/', views.register_page, name='register'),
    path('login/', views.log_in_page, name='login')

]
