from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
import json

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        """Set up the test client and a test user."""
        self.client = APIClient()
        self.register_data = {
            "email": "testuser2@example.com",
            "password": "TestPass123!",
            "username": "testuser2",
            "first_name": "Test",
            "last_name": "User"
        }
        self.login_data = {
            "email": "testuser2@example.com",
            "password": "TestPass123!"
        }

    def test_register_user(self):
        """Test user registration endpoint."""
        response = self.client.post(
            '/api/auth/register/',
            data=json.dumps(self.register_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user']['email'], self.register_data['email'])

        # Verify user exists in database
        user = User.objects.get(email=self.register_data['email'])
        self.assertTrue(user.check_password(self.register_data['password']))

    def test_login_user(self):
        """Test user login endpoint after registration."""
        # First register the user
        self.client.post(
            '/api/auth/register/',
            data=json.dumps(self.register_data),
            content_type='application/json'
        )

        # Then attempt login
        response = self.client.post(
            '/api/auth/login/',
            data=json.dumps(self.login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user']['email'], self.login_data['email'])

    def test_get_register_info(self):
        """Test GET method on register endpoint."""
        response = self.client.get('/api/auth/register/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Use POST to register with email, password, and username.')

    def test_duplicate_email_registration(self):
        """Test registration with duplicate email."""
        # Register once
        self.client.post(
            '/api/auth/register/',
            data=json.dumps(self.register_data),
            content_type='application/json'
        )
        # Try to register again with the same email
        response = self.client.post(
            '/api/auth/register/',
            data=json.dumps(self.register_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], 'user with this email already exists.')

    # Note: Full Google login test is limited due to OAuth
    def test_social_login_redirect(self):
        """Test initial redirect for social login (simplified)."""
        response = self.client.get('/api/auth/social/google-oauth2/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Expect a redirect
        # Full OAuth flow requires a test server and Google credentials, which is complex here
        # This is a basic check; for full testing, use a mock or frontend