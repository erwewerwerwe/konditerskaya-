from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта', required=True)

    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'patronymic', 'birth_date', 'gender', 'city', 'image']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
        elif self.instance and hasattr(self.instance, 'user'):
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        email = self.cleaned_data.get('email')
        if email and user.email != email:
            user.email = email
            user.save()
        if commit:
            profile.save()
        return profile