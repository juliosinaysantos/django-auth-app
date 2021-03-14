from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.utils.http import is_safe_url
from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages

from users.forms import LoginForm
from users.decorators import guest_only


@guest_only
def register_view(request):
    return render(request, 'users/register.html')


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
