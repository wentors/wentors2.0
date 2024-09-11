from django.urls import path, re_path

from .views import index, MakePaymentView, plan_payment_detail


urlpatterns = [
    path('', index, name="root"),
    path('index/', index, name="index"),
    path('plans/', index, name="plans"),
    path('plans/<str:slug>/', plan_payment_detail,  name="make-plan-payment"),
    # path('process-payment/', process_payment),
]
