import base64
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# === DARAJA SANDBOX CREDENTIALS ===
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

BUSINESS_SHORTCODE = "174379"
PASSKEY = os.getenv("PASS_KEY")

# Use a valid https callback, even if dummy — Safaricom requires HTTPS
CALLBACK_URL = "https://mydomain.com/callback"


def _access_token() -> str:
    token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(token_url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    response.raise_for_status()
    return response.json()["access_token"]


def initiate_stk_push(phone_number: str, amount: int) -> dict:
    # Format phone number correctly (e.g. 254708374149)
    if not phone_number.startswith("254") or len(phone_number) != 12:
        raise ValueError("Phone number must be in format 2547XXXXXXXX")

    access_token = _access_token()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{BUSINESS_SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "HOTSPOT",
        "TransactionDesc": "Hotspot Access"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        # Return more details in case of 500
        return {
            "detail": "STK Push failed",
            "status_code": response.status_code,
            "reason": str(err),
            "response": response.text
        }

    return response.json()
