from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'patronymic', 'birth_date', 'gender', 'city', 'image']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }