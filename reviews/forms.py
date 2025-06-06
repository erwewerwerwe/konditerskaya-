from django import forms
from .models import Review
from .models import ReviewFeedback


class ReviewForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0, max_value=5, widget=forms.NumberInput(attrs={'step': '0.1'}))

    class Meta:
        model = Review
        fields = ['rating', 'comment']

class ReviewFeedbackForm(forms.ModelForm):
    class Meta:
        model = ReviewFeedback
        fields = ['was_helpful', 'comment']
        widgets = {
            'was_helpful': forms.RadioSelect(choices=[(True, 'Да'), (False, 'Нет')]),
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ваш комментарий'}),
        }
