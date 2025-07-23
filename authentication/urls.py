from django.urls import path, include
from .views import RegisterView, LoginView
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='register/', permanent=False)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('social/', include('social_django.urls', namespace='social')),
]