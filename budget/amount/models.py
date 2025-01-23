from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.date}"
