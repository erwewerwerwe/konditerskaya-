from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, verbose_name='URL категории', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/catalog/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    details = models.TextField("Подробная информация", blank=True, null=True)  # Всё, что захочет админ
    nutrition_kcal = models.CharField("Калории (Ккал)", max_length=50, blank=True, null=True)
    nutrition_protein = models.CharField("Белки", max_length=50, blank=True, null=True)
    nutrition_fat = models.CharField("Жиры", max_length=50, blank=True, null=True)
    nutrition_carb = models.CharField("Углеводы", max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    weight = models.DecimalField(max_digits=8, decimal_places=1, verbose_name='Вес')
    persons_info = models.CharField(max_length=50, blank=True, null=True, verbose_name='Количество человек')
    shelf_life_days = models.CharField("Срок годности (в днях)",max_length=5, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория', null=True, blank=True)
    slug = models.SlugField(max_length=120, unique=True, verbose_name='URL категории', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            desired_size = (340, 220)
            img = ImageOps.fit(img, desired_size, Image.LANCZOS)
            img.save(self.image.path)


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField('Фамилия', max_length=50, blank=True)
    first_name = models.CharField('Имя', max_length=50, blank=True)
    patronymic = models.CharField('Отчество', max_length=50, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    city = models.CharField('Город проживания', max_length=100, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name='Фото пользователя')


    def __str__(self):
        return self.user.username


