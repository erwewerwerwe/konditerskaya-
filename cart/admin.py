from django.contrib import admin
from .models import Cart, CartItem, Favorite

admin.site.register(Cart)
admin.site.register(CartItem)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')