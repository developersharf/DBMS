# from django import forms
# from .models import FoundItem
# from django.utils import timezone

# LOCATION_CHOICES = [
#     ('Central Library', 'Central Library'),
#     ('Bus', 'Bus'),
#     ('Central Mosque', 'Central Mosque'),
#     ('C building', 'C building'),
#     ('Lab', 'Lab'),
# ]

# class FoundItemForm(forms.Form):
#     #   finder_email = forms.EmailField()
#     finder_email = forms.EmailField(
#         widget=forms.EmailInput(attrs={'readonly': 'readonly'}),
#         label='Your Email'
#     )
#     title = forms.CharField(max_length=255)
#     description = forms.CharField(widget=forms.Textarea)
#     date_found = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()})
#     )
#     location = forms.ChoiceField(choices=LOCATION_CHOICES)

#     def clean_date_found(self):
#         date = self.cleaned_data.get('date_found')
#         if date > timezone.now().date():
#             raise forms.ValidationError("Date cannot be in the future.")
#         return date


from django import forms
from .models import FoundItem
from django.utils import timezone

LOCATION_CHOICES = [
    ('Central Library', 'Central Library'),
    ('Bus', 'Bus'),
    ('Central Mosque', 'Central Mosque'),
    ('C building', 'C building'),
    ('Lab', 'Lab'),
]

class FoundItemForm(forms.ModelForm):
    finder_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'readonly': 'readonly'}),
        label='Your Email'
    )

    class Meta:
        model = FoundItem
        fields = ['finder_email', 'title', 'description', 'date_found', 'location']
        widgets = {
            'date_found': forms.DateInput(attrs={
                'type': 'date',
                'max': timezone.now().date()
            }),
            'description': forms.Textarea(),
        }

    def clean_date_found(self):
        date = self.cleaned_data.get('date_found')
        if date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future.")
        return date
