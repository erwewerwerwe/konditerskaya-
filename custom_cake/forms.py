from django import forms
from .models import CustomCakeOrder

DECORATION_CHOICES = [
    ('cream', 'Крем'),
    ('sprinkles', 'Посыпка'),
    ('fruit', 'Фрукты'),
    ('nuts', 'Орехи'),
    ('other', 'Другое'),
]

class CustomCakeOrderForm(forms.ModelForm):
    biscuit = forms.CharField(label='Бисквит', max_length=100)
    cream = forms.CharField(label='Крем', max_length=100)
    filling = forms.CharField(label='Начинка', max_length=100)
    decoration = forms.CharField(label='Оформление', max_length=200, required=False)
    weight = forms.FloatField(label='Вес (кг)')

    class Meta:
        model = CustomCakeOrder
        fields = ['biscuit', 'cream', 'filling', 'decoration', 'weight', 'photo_example', 'comment']

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight <= 0:
            raise forms.ValidationError('Вес должен быть положительным числом.')
        return weight
