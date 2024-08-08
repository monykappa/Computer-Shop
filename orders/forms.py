from shared_imports import *

class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'placeholder': 'Leave a comment (optional)', 'class': 'form-control'}),
        }
