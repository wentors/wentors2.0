from django.db import models

# Create your models here.

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    months = models.IntegerField()
    description = models.TextField()
