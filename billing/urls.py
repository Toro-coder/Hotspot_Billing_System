# billing/urls.py
from django.urls import path
from .views import pay_hotspot

urlpatterns = [
    path("pay/", pay_hotspot, name="pay-hotspot"),
]
