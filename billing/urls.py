# billing/urls.py
from django.urls import path
from .views import pay_hotspot,payment_callback,index

urlpatterns = [
    path("pay/", pay_hotspot, name="pay-hotspot"),
    path("callback/", payment_callback, name="payment-callback"),
    path("", index, name="index"),  # Add this line to include the index view
]
