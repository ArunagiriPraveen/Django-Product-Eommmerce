from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('products/', views.products, name='products'),

    # path('products/', views.product_list, name='products'),

    path('crud/', views.crud_updates, name='crud_updates'),

    path('cart/', views.cart, name='cart'),

    path('login/', views.user_login, name='login'),

    path('login/', views.user_logout, name='logout'),
    
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

]