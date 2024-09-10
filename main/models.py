from django.db import models
from datetime import date
from django.utils.text import slugify
from django.urls import reverse



from djmoney.models.fields import MoneyField
from dateutil.relativedelta import relativedelta

# Create your models here.

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=20)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    months = models.IntegerField()
    description = models.TextField()
    slug = models.SlugField(max_length=300, unique=True)


    # def __repr__(self) -> str:
    #     return f"{self.name}: {self.price}"

    def __str__(self) -> str:
        return f"{self.name}: {self.price}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubscriptionPlan, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse ("make-plan-payment", kwargs={"slug": self.slug})



# class PlanFeatures(models.Model):
#     title = models.TextField(blank=False)
#     description = models.TextField(blank=False)

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

    def __str__(self) -> str:
        return self.description
