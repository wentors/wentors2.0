from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView


from .models import SubscriptionPlan, Subscriber, Payment
from .forms import SubscriptionForm
import stripe
from django.conf import settings


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

        if form.is_valid():
            form_data = form.cleaned_data

            #assert False
            # call payment processing class and redirect to response url
            payment_processor = PaymentProcessor(form_data, plan)
            response_url = payment_processor.process_payment()
            return HttpResponseRedirect(response_url)
    else:
        form = SubscriptionForm()
    return render(request, "main/make_payment.html", {"form": form,
                                                    "object": plan,
                                                         })

def confirm_successful_stripe_payment(request):
    """
    Retrieves session_id from request.GET and processes successful payment.
    Display payment success page
    """

    if 'session_id' in request.GET:
        session_id = request.GET.get('session_id')
    else:
        return HttpResponseBadRequest()

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)

    payment_obj = get_object_or_404(Payment, stripe_payment_intent=session.payment_intent)
    payment_obj.is_confirmed = True
    payment_obj.save()

    # send confirmation email

    return render (request, "main/payment_success.html", {"payment": payment_obj})

def confirm_successful_paystack_payment(request):
    """
    Handles post-payment callback request from Paystack.

    * Calls paystack verification endpoint and handles response
    * Updates payment object and completes payment processing based on verification API response
    * Displays success/failure template based on response status
    """
    message = ""
    error_header = ""
    if 'reference' in request.GET:
        paystack_reference = request.GET.get('reference')
    else:
        # transaction reference not found
        return HttpResponseBadRequest('Can not confirm payment without "reference" in httprequest.\
                                         Please contact us if you have been charged!')

    # query paystack verify api
    url = 'https://api.paystack.co/transaction/verify/{}'.format(paystack_reference)
    paystack_auth = "Bearer {}".format(settings.PAYSTACK_SECRET_KEY)
    headers =  {"authorization": paystack_auth }
    response = requests.get(url, headers=headers)
    json_response = response.json()

    if not json_response["status"]  == True: # verification request failed
        error_header = "Verification Request Failed"
        message = "Paystack verification request unsuccessful"
    elif json_response['data']['status'] == "success": # successful payment
        payment_obj = get_object_or_404(Payment, paystack_unique_reference=paystack_reference)
        payment_obj.is_confirmed = True
        payment_obj.save()

        # send email
        return render (request, "main/payment_success.html", {"payment": payment_obj})
    elif not json_response['data']['status'] == "success": # unsuccessful payment
        error_header = "Payment Failed"
        message = "Paystack payment attempt was unsuccessful"
    else:
        error_header = "Verification Failure"
        message = "Could not verify paystack payment"

    return render (request, "main/paystack_failure.html", {"error":error_header, "message": message })

def payment_cancelled(request):
    """
    Handles payments cancelled by user. Displays correspond page
    """
    return render (request, "main/payment_cancelled.html")


class PaymentProcessor():
    def __init__(self, form_data, subscription_plan):
        self.form_data = form_data
        self.subscription_plan = subscription_plan

    def process_payment(self):
        subscriber_obj, _ = self.get_or_create_subcriber()

        if subscriber_obj: # here
            if self.form_data['paymentmethod'] == "stripe":
                checkout_url = self.process_stripe_payment(subscriber_obj)
                return checkout_url
            elif self.form_data['paymentmethod'] == "paystack":
                checkout_url = self.process_paystack_payment(subscriber_obj)
                return checkout_url


    def get_or_create_subcriber(self):
        """
        retrieve existing subscriber or create new
        """
        try:
            obj, created = Subscriber.objects.get_or_create(
                full_name=self.form_data['fullname'],
                email = self.form_data['email'],
                country= self.form_data["country"],
                phone_number=self.form_data["phonenumber"],
                country_code = self.form_data["countrycode"]
            )
            return obj, created
        except Exception as e:
            return None, False

    def process_stripe_payment(self, subscriber_obj):
        """
        process payment via stripe checkout api
        """
        # create stripe checkout session
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(

                customer_email = subscriber_obj.email,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': self.subscription_plan.name ,
                            'description': self.subscription_plan.description ,
                            },
                            'unit_amount': int(self.subscription_plan.price.amount * 100),
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('confirm_stripe_transaction')
                ) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri(reverse('payment_cancelled')),
            )

            # create payment object
            new_payment = self.initialize_payment_obj(subscriber_obj,
                                                        checkout_session['payment_intent'])

            return checkout_session.url

        except Exception as e:
            # logger.error(error)
            raise

    def process_paystack_payment(self, subscriber_obj):
        """
        process payment via paystack checkout api
        """
        try:
            charge_amount_NGN = self.subscription_plan.price.amount  * 1600.00 # replace with dynamic rate

            url = 'https://api.paystack.co/transaction/initialize'
            paystack_auth = "Bearer {}".format(settings.PAYSTACK_SECRET_KEY)
            headers =  {"authorization": paystack_auth }

            data={
                'email': subscriber_obj.email,
                'amount': int(charge_amount_NGN * 100 ),
                'currency': 'NGN',
                'callback_url': request.build_absolute_uri(reverse('confirm_paystack_transaction')),
                'metadata': {
                        "custom_fields":[
                            {
                              "display_name": "plan",
                              "variable_name": "plan",
                              "value": self.subscription_plan.name
                            },
                            {
                            "display_name":"description",
                            "variable_name":"description",
                            "value": self.subscription_plan.description
                            }
                            ],
                        "cancel_action": request.build_absolute_uri(reverse('payment_cancelled'))
                        }
            }

            json_data = json.dumps(data)
            r = requests.post(url, headers=headers, data=json_data)
            response = r.json()
            paystack_unique_reference = response["data"]["reference"]
            paystack_authorization_url = response["data"]["authorization_url"]

            if not response["status"] == True:
                raise Exception ("paystack initialization failed")

            self.initialize_payment_obj(subscriber_obj, paystack_unique_reference)
            return paystack_authorization_url

        except Exception as e:
            # logger.error(error)
            raise

    def initialize_payment_obj(self, subscriber_obj, payment_session_identifier):
        try:
            new_payment = Payment.objects.create(
                subscriber=subscriber_obj,
                plan=self.subscription_plan,
                payment_gateway= self.form_data["payment_method"]
            )
            if self.form_data["payment_method"] == "stripe" :
                new_payment.stripe_intent = payment_session_identifier
            elif self.form_data["payment_method"] == "paystack":
                new_payment.paystack_unique_reference = payment_session_identifier

            new_payment.full_clean() # custom validation check
            new_payment.save()
            return new_payment
        except Exception as e:
            raise Exception(e)