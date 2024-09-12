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


class Subscriber(models.Model):
    full_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField( blank=False)
    country = models.CharField(max_length=50, blank=False )
    phone_number = models.CharField(max_length=20, blank=False )
    country_code = models.CharField(max_length=4, blank=False)

    def __repr__(self) -> str:
        return f'Subcriber({self.full_name}, {self.email}, {self.Country}, {self.phonenumber}, {self.country_code})'

    def __str__(self) -> str:
        return f'Subcriber({self.full_name}, {self.email})'

PAYMENT_METHODS = [
        ("stripe", "stripe"),
        ("paystack", "paystack")
    ]
class Payment(models.Model):
    subscriber =models.ForeignKey(Subscriber, on_delete=models.PROTECT)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    time_stamp = models.DateTimeField(auto_now=True)
    is_confirmed = models.BooleanField(default=False)
    amount = MoneyField(max_digits=19, decimal_places=2)
    payment_gateway = models.CharField(max_length=25, blank=False, choices=PAYMENT_METHODS )
    stripe_intent = models.CharField(max_length=200, blank=True, default="")
    paystack_unique_reference = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(default="")

    def clean(self):
        if self.stripe_intent == "" and self.paystack_unique_reference == "":
            raise ValidationError(_("'stripe intent' or 'paystack unique reference' must be provided;\
                                                                                 both cannot be blank!"))

        if self.payment_gateway == "stripe" and self.stripe_intent == "":
            raise ValidationError(_("'stripe intent' must be provided for stripe payments"))

        if self.payment_gateway == "paystack" and self.paystack_unique_reference == "":
            raise ValidationError(_("'paystack_unique_reference' must be provided for paystack payments"))
