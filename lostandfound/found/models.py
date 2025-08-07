from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class FoundItem(models.Model):
   
    LOCATION_CHOICES = [
        ('Central Library', 'Central Library'),
        ('Bus', 'Bus'),
        ('Central Mosque', 'Central Mosque'),
        ('C building', 'C building'),
        ('Lab', 'Lab'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    finder_email =  models.EmailField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_found = models.DateField()
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



