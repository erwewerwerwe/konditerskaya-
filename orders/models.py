from django.db import models
from django.conf import settings
from shop.models import Product  # Предполагается, что есть приложение shop с моделью Product


class Order(models.Model):
    PICKUP_CHOICES = [
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз'),
    ]

    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    comments = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pickup_method = models.CharField(
        max_length=10,
        choices=PICKUP_CHOICES,
        default='delivery',
        verbose_name='Способ получения'
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Заказ #{self.id} от {self.full_name}'

    def get_total_cost(self):
        return self.total_price + self.delivery_cost


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.product:
            return f'{self.product.name} x {self.quantity}'
        return f'{self.custom_name or "Кастомный товар"} x {self.quantity}'

    def get_cost(self):
        return self.price * self.quantity
