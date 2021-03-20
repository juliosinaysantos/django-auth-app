import secrets

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from users.decorators import email_unverified_only
from users.utils import send_user_email_verification


@login_required
@email_unverified_only
def unverified_email(request):
    if request.method == 'POST':
        user = request.user
        send_user_email_verification(request, user)
        msg = f'We sent a verification email to {user.email}. Please follow the instructions in it.'
        messages.success(request, msg)
    return render(request, 'users/unverified_email.html')


@login_required
@email_unverified_only
def verify_email(request):
    user = request.user
    token = request.GET.get('token', None)
    user_email_verification_token = user.email_verification_token
    if not token or not secrets.compare_digest(token, user_email_verification_token):
        messages.error(request, 'There was an error verifying your email.')
        return redirect('users:unverified-email')
    user.email_verified_at = timezone.now()
    user.email_verification_token = ''
    user.save()
    messages.info(request, 'Your email was verified.')
    return redirect('users:profile')
