from django.urls import path, include
from .views import RegisterView, LoginView, social_login

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('social/<backend>/', social_login, name='social_login'),
    path('social/', include('social_django.urls', namespace='social')),
]