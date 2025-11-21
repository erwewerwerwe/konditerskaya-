from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.user_orders, name='user_orders'),
    path('delete/<int:order_id>/', views.order_delete, name='order_delete'),
]
