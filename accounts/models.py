from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StaffUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=255)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)
    
    def __str__(self):
        return f"Card ending in {self.card_number[-4:]}"


