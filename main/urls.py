from django.urls import path, re_path

from .views import index, MakePaymentView


urlpatterns = [
    path('', index, name="root"),
    path('index/', index, name="index"),
    path('plans/', index, name="plans"),
    path('plans/<str:slug>/', MakePaymentView.as_view(),  name="make-plan-payment"),
]
