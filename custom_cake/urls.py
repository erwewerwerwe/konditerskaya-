from django.urls import path
from . import views

app_name = 'custom_cake'

urlpatterns = [
    path('build/', views.build_cake, name='build_cake'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:cake_id>/', views.add_custom_cake_to_cart, name='add_custom_cake_to_cart'),
]