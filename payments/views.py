import base64
import datetime
import os
import requests
from dotenv import load_dotenv

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import MpesaTransaction

load_dotenv()  # Load .env variables

def get_access_token():
    consumer_key = os.getenv("MPESA_CONSUMER_KEY")
    consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    return response.json().get("access_token")


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])  # ✅ Allow external/frontend calls
def stk_push(request):
    access_token = get_access_token()
    if not access_token:
        return Response({"error": "Unable to authenticate with M-Pesa"}, status=500)

    phone = request.data.get("phone_number")
    amount = request.data.get("amount")
    if not phone or not amount:
        return Response({"error": "Phone number and amount are required."}, status=400)

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = os.getenv("MPESA_SHORTCODE")
    passkey = os.getenv("MPESA_PASSKEY")

    password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": os.getenv("MPESA_CALLBACK_URL"),
        "AccountReference": "RebelRadiance",
        "TransactionDesc": "Payment for order"
    }

    res = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
    data = res.json()

    if res.status_code == 200 and data.get("ResponseCode") == "0":
        MpesaTransaction.objects.create(
            phone_number=phone,
            amount=amount,
            merchant_request_id=data["MerchantRequestID"],
            checkout_request_id=data["CheckoutRequestID"]
        )
        return Response({"message": "STK push sent successfully. Check your phone 📲"})
    else:
        return Response({"error": data}, status=400)


@csrf_exempt  # ✅ Exempt from CSRF (callback from Safaricom backend)
@api_view(["POST"])
@permission_classes([AllowAny])  # ✅ Open for Safaricom servers
def mpesa_callback(request):
    data = request.data.get("Body", {}).get("stkCallback", {})
    checkout_id = data.get("CheckoutRequestID")
    result_code = data.get("ResultCode")

    try:
        transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_id)
        transaction.status = "Success" if result_code == 0 else "Failed"
        transaction.save()
    except MpesaTransaction.DoesNotExist:
        pass  # Optional: log warning

    return Response({"ResultCode": 0, "ResultDesc": "Callback received and processed"})
