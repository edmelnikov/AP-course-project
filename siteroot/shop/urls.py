from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('<int:product_id>', views.single_product_page, name='product_by_id'),  # how does it work
    #path('<int:product_id>/post_review', views.post_review, name='post_review'),
    #path('<int:product_id>/post_review/error', views.print_review_error, name='print_error'),
    path('sign_up/', views.sign_up_page, name='signup'),
    path('login/', views.log_in_page, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:product_id>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change/<int:product_id>/', ChangeQuantityView.as_view(), name='change_quantity'),
	path('featured/', FeaturedView.as_view(), name='featured'),
	path('addfeature/<int:product_id>/', AddToFeaturedView.as_view(), name='add_to_featured'),
    path('removefeature/<int:product_id>/', DeleteFromFeatured.as_view(), name='delete_from_featured'),
]
