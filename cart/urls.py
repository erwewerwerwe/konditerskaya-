from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
]
