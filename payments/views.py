import base64
import datetime
import os
import requests
from dotenv import load_dotenv

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from .models import MpesaTransaction

load_dotenv()  # Load environment variables from .env


# 🔐 Get access token from Safaricom API
def get_access_token():
    consumer_key = os.getenv("MPESA_CONSUMER_KEY")
    consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    print("🧪 Testing MPESA Credentials:")
    print("Consumer Key:", consumer_key)
    print("Consumer Secret:", consumer_secret)

    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))

    print("AUTH STATUS CODE:", response.status_code)
    print("AUTH RAW TEXT:", response.text)

    try:
        return response.json().get("access_token")
    except Exception as e:
        print("❌ JSON decode error:", str(e))
        return None


# 📲 Initiate STK Push
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
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
    callback_url = os.getenv("MPESA_CALLBACK_URL")

    print("----- M-PESA ENV DEBUG -----")
    print("Shortcode:", shortcode)
    print("Passkey:", passkey[:10] + "...")
    print("Timestamp:", timestamp)
    print("Callback URL:", callback_url)
    print("Access Token:", access_token[:10] + "...")
    print("----------------------------")

    password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": "RebelRadiance",
        "TransactionDesc": "Payment for order"
    }

    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )

    try:
        data = res.json()
    except Exception as e:
        print("❌ M-Pesa JSON Decode Error:", str(e))
        print("Raw Response:", res.text)
        return Response({"error": "Failed to decode Safaricom response."}, status=500)

    print("📡 M-PESA Raw Response:", data)

    if res.status_code == 200 and data.get("ResponseCode") == "0":
        MpesaTransaction.objects.create(
            phone_number=phone,
            amount=amount,
            merchant_request_id=data["MerchantRequestID"],
            checkout_request_id=data["CheckoutRequestID"]
        )
        return Response({
            "message": "STK push sent successfully. Check your phone 📲",
            "checkout_request_id": data["CheckoutRequestID"]
        })
    else:
        return Response({"error": data}, status=400)


# 📥 M-PESA Callback URL
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def mpesa_callback(request):
    try:
        print("📩 Raw Callback Body:", request.body.decode())
        callback_data = request.data or {}

        if not callback_data:
            import json
            callback_data = json.loads(request.body.decode())

        data = callback_data.get("Body", {}).get("stkCallback", {})
        print("📦 Parsed Callback Data:", data)

        checkout_id = data.get("CheckoutRequestID")
        result_code = data.get("ResultCode")

        if not checkout_id:
            print("❌ Missing CheckoutRequestID in callback")
            return Response({"error": "Missing checkout ID"}, status=400)

        try:
            transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_id)
            transaction.status = "Success" if result_code == 0 else "Failed"
            transaction.save()
            print("✅ Transaction updated:", transaction)
        except MpesaTransaction.DoesNotExist:
            print(f"❌ Transaction not found for CheckoutRequestID: {checkout_id}")
            return Response({"error": "Transaction not found"}, status=404)

        return Response({"ResultCode": 0, "ResultDesc": "Callback received and processed"})

    except Exception as e:
        print("❌ Callback error:", str(e))
        return Response({"error": "Invalid callback format"}, status=500)


# 🧾 Check Payment Status
@csrf_exempt
@api_view(["GET"])
@permission_classes([AllowAny])
def payment_status(request, checkout_request_id):
    try:
        transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
        return Response({
            "status": transaction.status,
            "phone_number": transaction.phone_number,
            "amount": transaction.amount
        })
    except MpesaTransaction.DoesNotExist:
        return Response({"status": "Pending"})
