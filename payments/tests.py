from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from payments.models import MpesaTransaction

class MpesaPaymentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.stk_push_url = reverse('stk_push')
        self.callback_url = reverse('mpesa_callback')
        self.checkout_id = "ws_CO_123456789"

        self.transaction = MpesaTransaction.objects.create(
            phone_number="254712345678",
            amount=100,
            merchant_request_id="123456",
            checkout_request_id=self.checkout_id,
            status="Pending"
        )

    def test_stk_push_requires_fields(self):
        res = self.client.post(self.stk_push_url, data={})
        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.data)

    def test_payment_status_returns_pending(self):
        res = self.client.get(reverse('payment_status', args=[self.checkout_id]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["status"], "Pending")

    def test_callback_sets_success_status(self):
        callback_data = {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": "123456",
                    "CheckoutRequestID": self.checkout_id,
                    "ResultCode": 0
                }
            }
        }

        res = self.client.post(self.callback_url, data=callback_data, format='json')
        self.assertEqual(res.status_code, 200)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.status, "Success")

    def test_callback_sets_failed_status(self):
        callback_data = {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": "123456",
                    "CheckoutRequestID": self.checkout_id,
                    "ResultCode": 1032
                }
            }
        }

        res = self.client.post(self.callback_url, data=callback_data, format='json')
        self.assertEqual(res.status_code, 200)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.status, "Failed")

    def test_callback_missing_checkout_id(self):
        callback_data = {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": "123456",
                    "ResultCode": 0
                }
            }
        }

        res = self.client.post(self.callback_url, data=callback_data, format='json')
        self.assertEqual(res.status_code, 400)

    def test_callback_transaction_not_found(self):
        callback_data = {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": "wrong_id",
                    "CheckoutRequestID": "nonexistent123",
                    "ResultCode": 0
                }
            }
        }

        res = self.client.post(self.callback_url, data=callback_data, format='json')
        self.assertEqual(res.status_code, 404)

    def test_status_nonexistent_transaction(self):
        res = self.client.get(reverse('payment_status', args=["does_not_exist"]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["status"], "Pending")

    def test_transaction_str_representation(self):
        self.assertEqual(
            str(self.transaction),
            "254712345678 - 100.00 - Pending"
        )