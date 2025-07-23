from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
import json

User = get_user_model()

class AuthenticationTests(APITestCase):
    def setUp(self):
        """Set up the test client and test data."""
        self.client = self.client
        self.register_url = reverse('register')  # Maps to /api/auth/register/
        self.login_url = reverse('login')       # Maps to /api/auth/login/
        self.social_url = '/api/auth/social/google-oauth2/'  # Direct path for social login
        self.register_data = {
            "email": "testuser4@example.com",
            "password": "TestPass123!",
            "username": "testuser4",
            "first_name": "Test",
            "last_name": "User"
        }
        self.login_data = {
            "email": "testuser4@example.com",
            "password": "TestPass123!"
        }

    def test_register_user(self):
        """Test user registration endpoint (POST)."""
        response = self.client.post(
            self.register_url,
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
        """Test user login endpoint (POST) after registration."""
        # Register the user first
        self.client.post(
            self.register_url,
            data=json.dumps(self.register_data),
            content_type='application/json'
        )

        # Attempt login
        response = self.client.post(
            self.login_url,
            data=json.dumps(self.login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user']['email'], self.login_data['email'])

    def test_get_register_info(self):
        """Test GET method on register endpoint."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Use POST to register with email, password, and username.')

    def test_duplicate_email_registration(self):
        """Test registration with duplicate email."""
        # Register once
        self.client.post(
            self.register_url,
            data=json.dumps(self.register_data),
            content_type='application/json'
        )
        # Try to register again with the same email
        response = self.client.post(
            self.register_url,
            data=json.dumps(self.register_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], 'user with this email already exists.')

    def test_social_login_redirect(self):
        """Test initial redirect for social login (simplified)."""
        response = self.client.get(self.social_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Expect a redirect
        # Full OAuth flow requires mocking or frontend testing; this is a basic check

    def test_invalid_login(self):
        """Test login with invalid credentials."""
        # Register the user
        self.client.post(
            self.register_url,
            data=json.dumps(self.register_data),
            content_type='application/json'
        )
        # Try login with wrong password
        invalid_login_data = {
            "email": "testuser4@example.com",
            "password": "WrongPass123!"
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(invalid_login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid credentials')
