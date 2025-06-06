from django.db import models
from django.conf import settings
from shop.models import Product
from django.contrib.auth.models import User

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=0)
    comment = models.TextField(blank=True)
    helpful_yes = models.PositiveIntegerField(default=0)
    helpful_no = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class ReviewFeedback(models.Model):
    review = models.ForeignKey(Review, related_name='feedbacks', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    was_helpful = models.BooleanField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')  # чтобы один пользователь мог проголосовать и прокомментировать один раз
