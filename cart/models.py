from django.db import models
from shop.models import Product
from django.contrib.auth import get_user_model
from custom_cake.models import CustomCakeOrder
from decimal import Decimal

User = get_user_model()

class Cart(models.Model):
    cart_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        if self.cart_id:
            return self.cart_id
        elif self.user:
            return f"Cart of {self.user.username}"
        return "Anonymous Cart"

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.sub_total for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    custom_cake = models.ForeignKey(CustomCakeOrder, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # <--- Добавьте это поле

    class Meta:
        ordering = ['product']
        unique_together = (
            ('cart', 'product'),
            ('cart', 'custom_cake'),
        )

    @property
    def sub_total(self):
        if self.product:
            return self.product.price * self.quantity
        elif self.custom_cake:
            if hasattr(self.custom_cake, 'price'):
                return self.custom_cake.price * self.quantity
            elif hasattr(self.custom_cake, 'get_price'):
                return self.custom_cake.get_price() * self.quantity
        return 0

    @property
    def name(self):
        if self.custom_cake:
            return str(self.custom_cake)
        elif self.product:
            return self.product.name
        return "Товар"

    def __str__(self):
        if self.product:
            return f"{self.product.name} ({self.quantity})"
        elif self.custom_cake:
            return f"{self.custom_cake} ({self.quantity})"
        return f"CartItem ({self.quantity})"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
