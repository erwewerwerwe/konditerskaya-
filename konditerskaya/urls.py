from django.contrib import admin
from django.urls import path, include # обязательно импортируем include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('shop.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # стандартные маршруты аутентификации
    path('cart/', include('cart.urls', namespace='cart')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('custom-cake/', include('custom_cake.urls')),
    path('orders/', include('orders.urls', namespace='orders')),


# маршруты приложения
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)