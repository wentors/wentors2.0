from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your models here.

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    months = models.IntegerField()
    description = models.TextField()

class CohortSchedule(models.Model):
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(blank=True)

    def save(self, *args, **kwargs):
        if not self.end_date: # calculate the end_date based on start_date -> add six months
            self.end_date = self.start_date + relativedelta(months=+6)
        super(CohortSchedule, self).save(*args, **kwargs)

    @property
    def description(self):
        return f'cohort scheduled to begin on {self.start_date}'
