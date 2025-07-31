from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .models import User
import requests
from requests_oauthlib import OAuth2Session
import os

class GoogleLoginView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response(
                {'error': 'Authorization code is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        client_id = os.environ.get('GOOGLE_CLIENT_ID') or getattr(settings, 'GOOGLE_CLIENT_ID', None)
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET') or getattr(settings, 'GOOGLE_CLIENT_SECRET', None)
        redirect_uri = 'http://localhost:5173'  

        if not client_id or not client_secret:
            return Response(
                {'error': 'Server configuration error: missing Google credentials'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            token_url = 'https://oauth2.googleapis.com/token'
            google = OAuth2Session(client_id, redirect_uri=redirect_uri)

            token = google.fetch_token(
                token_url,
                code=code,
                client_secret=client_secret,
                include_client_id=True
            )
            access_token = token['access_token']

            user_info = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            user_info.raise_for_status()
            user_data = user_info.json()

        except requests.HTTPError as e:
            return Response(
                {'error': 'Failed to fetch user info from Google', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Authentication failed', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = user_data.get('email')
        if not email:
            return Response({'error': 'Google account has no email'}, status=status.HTTP_400_BAD_REQUEST)

        username = email.split('@')[0]
        first_name = user_data.get('given_name', '')
        last_name = user_data.get('family_name', '')

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
            }
        )

        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        login(request, user)

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)