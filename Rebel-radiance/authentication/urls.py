from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AuthIndexView.as_view(), name='auth_index'), 
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'), 
    path('social/', include('social_django.urls', namespace='social')),  
    path('google/', views.GoogleLoginView.as_view(), name='google_login'),
]