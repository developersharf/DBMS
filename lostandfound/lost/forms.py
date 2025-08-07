# from django import forms
# from .models import LostItem
# from django.utils import timezone

# LOCATION_CHOICES = [
#     ('Central Library', 'Central Library'),
#     ('Bus', 'Bus'),
#     ('Central Mosque', 'Central Mosque'),
#     ('C building', 'C building'),
#     ('Lab', 'Lab'),
# ]

# class LostItemForm(forms.Form):
    
#     user_email = forms.EmailField(
#         widget=forms.EmailInput(attrs={'readonly': 'readonly'}),
#         label='Your Email'
#     )
#     title = forms.CharField(max_length=255)
#     description = forms.CharField(widget=forms.Textarea)
#     date_lost = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()})
#     )
#     location = forms.ChoiceField(choices=LOCATION_CHOICES)

#     def clean_date_lost(self):
#         date = self.cleaned_data.get('date_lost')
#         if date > timezone.now().date():
#             raise forms.ValidationError("Date cannot be in the future.")
#         return date


from django import forms
from .models import LostItem
from django.utils import timezone

class LostItemForm(forms.ModelForm):
    user_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'readonly': 'readonly'}),
        label='Your Email'
    )

    class Meta:
        model = LostItem
        fields = ['user_email', 'title', 'description', 'date_lost', 'location']
        widgets = {
            'date_lost': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()}),
            'description': forms.Textarea(),
        }

    def clean_date_lost(self):
        date = self.cleaned_data.get('date_lost')
        if date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future.")
        return date
