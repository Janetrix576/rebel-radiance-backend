from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, authenticate
from .models import User
import requests
from .serializers import UserSerializer, LoginSerializer
from requests_oauthlib import OAuth2Session
import os

class AuthIndexView(APIView):
    def get(self, request):
        return Response({
            'message': 'Authentication API',
            'endpoints': {
                'register': 'api/auth/register/',
                'login': 'api/auth/login/',
                'google': 'api/auth/google/',
                'social': 'api/auth/social/',
            }
        }, status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"message": "Use POST to register with email, password, and username."}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user is None:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(APIView):
    def post(self, request):
        code = request.data.get('code')  # Expecting authorization code from frontend
        if not code:
            return Response({'error': 'Authorization code is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Google OAuth2 configuration
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
        redirect_uri = 'http://localhost:5173'  # Match your frontend URL

        if not client_id or not client_secret:
            return Response({'error': 'Google client credentials not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Initialize OAuth2 session
            google = OAuth2Session(client_id, redirect_uri=redirect_uri)
            # Exchange code for access token
            token = google.fetch_token(
                'https://oauth2.googleapis.com/token',
                code=code,
                client_secret=client_secret,
                include_client_id=True
            )
            access_token = token['access_token']

            # Validate the access token and get user info
            user_info_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            user_info_response.raise_for_status()
            user_info = user_info_response.json()
        except requests.RequestException as e:
            return Response({
                'detail': 'Failed to validate token',
                'code': 'token_not_valid',
                'messages': [str(e)]
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'detail': 'Failed to exchange authorization code',
                'code': 'token_exchange_failed',
                'messages': [str(e)]
            }, status=status.HTTP_401_UNAUTHORIZED)

        email = user_info.get('email')
        username = user_info.get('email').split('@')[0]
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')

        # Check if user already exists
        try:
            user = User.objects.get(email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password='social_' + access_token[:10]
            )
            user.save()

        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)