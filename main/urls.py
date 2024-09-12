from django.urls import path, re_path

from .views import index, MakePaymentView, plan_payment_detail, confirm_successful_stripe_payment, confirm_successful_paystack_payment


urlpatterns = [
    path('', index, name="root"),
    path('index/', index, name="index"),
    path('plans/', index, name="plans"),
    path('plans/<str:slug>/', plan_payment_detail,  name="make-plan-payment"),
    path('stripe_payment_successful/', confirm_successful_stripe_payment, name="confirm_stripe_transaction"),
    path('paystack_payment_successful/', confirm_successful_paystack_payment , name="confirm_paystack_transaction"),
]
