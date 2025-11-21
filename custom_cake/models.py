from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CustomCakeOrder(models.Model):


    WEIGHT_CHOICES = [
        (1, _('1 кг')),
        (1.5, _('1.5 кг')),
        (2, _('2 кг')),
        (3, _('3 кг')),
        (5, _('5 кг')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_cakes')
    biscuit = models.CharField(max_length=100, verbose_name='Бисквит', blank=True)
    cream = models.CharField(max_length=100, verbose_name='Крем', blank=True)
    filling = models.CharField(max_length=100, verbose_name='Начинка', blank=True)
    weight = models.FloatField(verbose_name='Вес (кг)', default=1)
    decoration = models.CharField(max_length=200, verbose_name='Оформление', blank=True)
    photo_example = models.ImageField(upload_to='custom_cakes/photos/', blank=True, null=True, verbose_name='Фото для примера')
    comment = models.TextField(blank=True, verbose_name='Пожелания')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1000)

    def __str__(self):
        return f"Кастомный торт #{self.id}"


    def get_weight_display_ru(self):
        return dict(self.WEIGHT_CHOICES).get(self.weight, f"{self.weight} кг")

    def get_biscuit_display_ru(self):
        biscuits = {
            'vanilla': _('Ванильный'),
            'chocolate': _('Шоколадный'),
            'carrot': _('Морковный'),
            'nut': _('Ореховый'),
            'other': _('Другое'),
        }
        return biscuits.get(self.biscuit, self.biscuit)

    def get_cream_display_ru(self):
        creams = {
            'butter': _('Масляный'),
            'cheese': _('Сырный'),
            'whipped': _('Взбитый'),
            'chocolate': _('Шоколадный'),
            'other': _('Другое'),
        }
        return creams.get(self.cream, self.cream)

    def get_filling_display_ru(self):
        fillings = {
            'strawberry': _('Клубника'),
            'cherry': _('Вишня'),
            'lemon': _('Лимон'),
            'caramel': _('Карамель'),
            'other': _('Другое'),
        }
        return fillings.get(self.filling, self.filling)


    def get_decoration_display_ru(self):
        decorations = {
            'cream': _('Крем'),
            'sprinkles': _('Посыпка'),
            'fruit': _('Фрукты'),
            'nuts': _('Орехи'),
            'other': _('Другое'),
        }
        if not self.decoration:
            return '-'
        parts = [part.strip() for part in self.decoration.split(',') if part.strip()]
        display_parts = [decorations.get(part, part) for part in parts]
        display_parts_str = [str(part) for part in display_parts]
        return ', '.join(display_parts_str)





