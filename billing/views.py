from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from .mpesa import initiate_stk_push


@api_view(["POST"])
def pay_hotspot(request):
    """
    Expected JSON:
    {
      "phone": "254708374149",
      "amount": 20
    }
    """
    phone = request.data.get("phone")
    amount = request.data.get("amount")

    if not phone or not amount:
        return Response(
            {"detail": "phone and amount are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        amount = int(amount)
    except (ValueError, TypeError):
        return Response(
            {"detail": "amount must be an integer"}, status=status.HTTP_400_BAD_REQUEST
        )

    # create local record first
    Payment.objects.create(phone_number=phone, amount=amount)

    # call Daraja
    try:
        mpesa_resp = initiate_stk_push(phone, amount)
    except Exception as exc:  # broad but OK for demo
        return Response(
            {"detail": "M‑Pesa request failed", "error": str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    return Response(
        {"message": "STK Push initiated", "mpesa_response": mpesa_resp},
        status=status.HTTP_202_ACCEPTED,
    )


