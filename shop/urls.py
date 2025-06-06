from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('cart/', include('cart.urls')),
    path('search/', views.search, name='search'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('custom_cake/', views.custom_cake, name='custom_cake'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('catalog/', views.category_list, name='category_list'),
    path('catalog/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

]