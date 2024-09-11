from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView


from .models import SubscriptionPlan
from .forms import SubscriptionForm


# Create your views here.

def index (request):
    current_plans = SubscriptionPlan.objects.all()
    return render(request, "main/index.html", {"current_plans": current_plans})

class MakePaymentView(DetailView):
    model = SubscriptionPlan
    template_name = "main/make_payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SubscriptionForm()
        context["form"] = form
        return context

def plan_payment_detail(request, slug):

    plan = SubscriptionPlan.objects.get(slug=slug)

    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            assert False
            #return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubscriptionForm()

    return render(request, "main/make_payment.html", {"form": form,
                                        "object": plan,
                                        })
