from django.shortcuts import redirect


def guest_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')
        return view_func(request, *args, **kwargs)
    return wrap


def email_verification_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.email_verified_at:
            return redirect('users:unverified-email')
        return view_func(request, *args, **kwargs)
    return wrap


def email_unverified_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.email_verified_at:
            return redirect('users:profile')
        return view_func(request, *args, **kwargs)
    return wrap
