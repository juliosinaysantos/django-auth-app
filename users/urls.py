from django.urls import path

from users.views import (
    login,
    register,
    logout,
    profile,
    unverified_email,
    verify_email,
    password_reset,
    new_password,
    settings
)

app_name = 'users'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('unverified-email/', unverified_email, name='unverified-email'),
    path('verify-email/', verify_email, name='verify-email'),
    path('password-reset/', password_reset, name='password-reset'),
    path('password-reset/<str:token>/', new_password, name='new-password'),
    path('settings/', settings, name='account-settings')
]
