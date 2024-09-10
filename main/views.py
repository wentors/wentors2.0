from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView


from .models import SubscriptionPlan


# Create your views here.

def index (request):
    current_plans = SubscriptionPlan.objects.all()
    return render(request, "main/index.html", {"current_plans": current_plans})

class MakePaymentView(DetailView):
    model = SubscriptionPlan
    template_name = "main/make_payment.html"
