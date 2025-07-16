from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
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
        amount = float(amount)
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


@api_view(["POST"])
def payment_callback(request):
    """
    Handle M-Pesa callback notifications.

    """
    # This endpoint is called by Safaricom when the payment status changes
    # The Request is validated, the payment status is checked, and the records are updated accordingly.

    # Ensure the request is from a trusted IP
    # allowed_ips = ["196.201.214.200",
    #                "196.201.214.206",
    #                "196.201.213.114",
    #                "196.201.214.207",
    #                "196.201.214.208",
    #                "196. 201.213.44",
    #                "196.201.212.127",
    #                "196.201.212.138",
    #                "196.201.212.129",
    #                "196.201.212.136",
    #                "196.201.212.74",
    #                "196.201.212.69",
    #                "c49ded4d78d4.ngrok-free.app"]
    # if request.META.get("REMOTE_ADDR") not in allowed_ips:
    #     return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
    
    # Safaricom sends a POST request with the callback data
    # The data structure is documented in the M-Pesa API documentation
    print("Received M-Pesa callback:", request.data)
    callback_data = request.data
    result_code = callback_data['Body']['stkCallback']['ResultCode']
    if result_code != 0:
        # If the result code is not 0, there was an error
        error_message = callback_data['Body']['stkCallback']['ResultDesc']
        response_data = {'ResultCode': result_code,
                         'ResultDesc': error_message}
        payment = Payment.objects.filter().last()
        if payment:
            payment.status = 'failed'
            payment.save()
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

     # If the result code is 0, the transaction was completed
    callback_metadata = callback_data['Body']['stkCallback']['CallbackMetadata']
    for item in callback_metadata['Item']:
        if item['Name'] == 'Amount':
            amount = item['Value']
        elif item['Name'] == 'PhoneNumber':
            phone_number = item['Value']
        elif item['Name'] == 'MpesaReceiptNumber':
            mpesa_receipt_number = item['Value']
        elif item['Name'] == 'TransactionDate':
            transaction_date = item['Value']
    payment = Payment.objects.filter(
        phone_number=phone_number, amount=amount).last()
    if payment:
        payment.status = 'completed'
        payment.mpesa_receipt_number = mpesa_receipt_number
        payment.transaction_date = transaction_date
        payment.save()
    else:
        # Handle the case where the payment record is not found
        return Response(
            {"detail": "Payment record not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    print("Received M-Pesa callback:", request.data)

    return Response({"detail": "Callback received"}, status=status.HTTP_200_OK)
@csrf_exempt
@api_view(["GET"])
def index(request):
    """
    Simple index view to test if the server is running.
    """
    return Response({"message": "Welcome to the Hotspot Billing System!"})