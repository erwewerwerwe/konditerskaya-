from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    pickup_method = forms.ChoiceField(
        choices=Order.PICKUP_CHOICES,
        widget=forms.RadioSelect,
        label='Способ получения'
    )
    agree_terms = forms.BooleanField(label='Я согласен с условиями обработки персональных данных', required=True)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'patronymic', 'phone', 'email', 'address', 'pickup_method', 'delivery_date', 'delivery_time', 'comments']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'delivery_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
