from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('<int:product_id>', views.get_product, name='product_by_id'),  # how does it work
    path('<int:product_id>/post_review', views.post_review, name='post_review'),
    path('<int:product_id>/post_review/error', views.print_review_error, name='print_error'),
    path('sign_up/', views.sign_up_page, name='signup'),
    path('login/', views.log_in_page, name='login'),
    path('logout/', views.log_out, name='logout')

]
