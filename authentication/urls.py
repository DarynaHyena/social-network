from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import PublicProfileView, RegisterView, ProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('profile/', ProfileUpdateView.as_view(), name='profile'),

    path('profile/<str:username>/', PublicProfileView.as_view(), name='public_profile'),
]