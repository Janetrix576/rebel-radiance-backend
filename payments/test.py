from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import MpesaTransaction
from unittest.mock import patch
import json

class MpesaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.phone = "+254712345678"
        self.amount = 1000

    @patch('payments.views.get_access_token')
    @patch('payments.views.requests.post')
    def test_successful_stk_push(self, mock_post, mock_get_token):
        mock_get_token.return_value = "test_token"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "ResponseCode": "0",
            "MerchantRequestID": "mockMerchant123",
            "CheckoutRequestID": "mockCheckout123"
        }

        response = self.client.post(
            reverse("stk_push"),
            data=json.dumps({
                "phone_number": self.phone,
                "amount": self.amount
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(MpesaTransaction.objects.filter(checkout_request_id="mockCheckout123").exists())

    def test_missing_phone_and_amount(self):
        response = self.client.post(
            reverse("stk_push"),
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Phone number and amount are required", response.json().get("error", ""))

    def test_payment_status_pending_if_transaction_not_found(self):
        response = self.client.get(reverse("payment_status", args=["nonexistent"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Pending")

    def test_mpesa_callback_updates_status_success(self):
        transaction = MpesaTransaction.objects.create(
            phone_number=self.phone,
            amount=self.amount,
            merchant_request_id="MR456",
            checkout_request_id="CR456"
        )

        callback_payload = {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": "MR456",
                    "CheckoutRequestID": "CR456",
                    "ResultCode": 0,
                    "ResultDesc": "Success"
                }
            }
        }

        response = self.client.post(
            reverse("mpesa_callback"),
            data=json.dumps(callback_payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        transaction.refresh_from_db()
        self.assertEqual(transaction.status, "Success")

    def test_mpesa_callback_with_failed_status(self):
        transaction = MpesaTransaction.objects.create(
            phone_number=self.phone,
            amount=self.amount,
            merchant_request_id="MR789",
            checkout_request_id="CR789"
        )

        callback_payload = {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": "MR789",
                    "CheckoutRequestID": "CR789",
                    "ResultCode": 1,
                    "ResultDesc": "Failed"
                }
            }
        }

        response = self.client.post(
            reverse("mpesa_callback"),
            data=json.dumps(callback_payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        transaction.refresh_from_db()
        self.assertEqual(transaction.status, "Failed")