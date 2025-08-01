from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .models import User
import requests
import os

class GoogleLoginView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Authorization code is required'}, status=status.HTTP_400_BAD_REQUEST)

        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
        redirect_uri = 'https://rebel-radiance-project.netlify.app/'

        if not client_id or not client_secret:
            return Response({'error': 'Google client credentials not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            token_response = requests.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'code': code,
                    'redirect_uri': redirect_uri,
                    'grant_type': 'authorization_code',
                },
                timeout=10
            )

            if token_response.status_code != 200:
                return Response({
                    'error': 'Failed to exchange code',
                    'details': token_response.json()
                }, status=status.HTTP_401_UNAUTHORIZED)

            token_data = token_response.json()
            access_token = token_data['access_token']

            user_info_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=10
            )
            user_info_response.raise_for_status()
            user_info = user_info_response.json()

        except requests.RequestException as e:
            return Response({
                'detail': 'Failed to validate Google token',
                'code': 'token_not_valid',
                'messages': [str(e)]
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'detail': 'Internal error during Google login',
                'code': 'google_login_failed',
                'messages': [str(e)]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        email = user_info.get('email')
        if not email:
            return Response({'error': 'Google did not return email'}, status=status.HTTP_400_BAD_REQUEST)

        username = email.split('@')[0]
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')

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
                password=None
            )

        login(request, user, backend='authentication.backends.EmailBackend')
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