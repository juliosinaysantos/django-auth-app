import jwt

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.utils import timezone
from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from django.conf import settings

from users.models import User
from users.forms import LoginForm, RegisterForm, PasswordResetForm, ChangePasswordForm
from users.decorators import guest_only
from users.utils import send_user_email_verification


@guest_only
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            send_user_email_verification(request, user)

            messages.success(request, 'Your account has been created!')
            return redirect('users:login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@guest_only
def login_view(request):
    redirect_to = request.GET.get('next', None)
    if not is_safe_url(url=redirect_to, allowed_hosts=None):
        redirect_to = resolve_url('users:profile')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_data = form.cleaned_data['login']
            password_data = form.cleaned_data['password']
            user = authenticate(username=login_data, password=password_data)
            if user:
                login(request, user)
                return redirect(redirect_to)
            else:
                messages.error(request, 'Login or password invalid')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@guest_only
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user:
                expires = timezone.now() + timezone.timedelta(minutes=5)
                token = jwt.encode({'username': user.username, 'exp': expires}, settings.SECRET_KEY, algorithm='HS256')
                url = request.build_absolute_uri(reverse_lazy('users:new-password', args=(token,)))

                subject = '[Auth App] Please reset your password.'
                from_mail = 'no-reply@authteam.com'
                to_mail = user.email
                text_content = 'content'
                html_content = render_to_string('emails/password_reset.html', {'url': url})

                send_mail(subject, text_content, from_mail, [to_mail], html_message=html_content)

            messages.success(
                request, (
                    'Check your email for a link to reset your password. '
                    'If it does not appear within a few minutes, check your spam folder.'
                )
            )
            return redirect('users:password-reset')
    else:
        form = PasswordResetForm()
    return render(request, 'users/reset_password.html', {'form': form})


def new_password(request, token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                user = User.objects.get(username=payload['username'])
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password has been changed successfully!')
                return redirect('users:login')
        else:
            form = ChangePasswordForm()
        return render(request, 'users/new_password.html', {'username': payload['username'], 'form': form})
    except jwt.ExpiredSignatureError:
        messages.error(request, 'Your password reset token has been expired.')
    except jwt.InvalidTokenError:
        messages.error(request, 'Your password reset token is invalid.')
    return redirect('users:password-reset')
