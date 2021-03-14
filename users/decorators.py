from django.shortcuts import redirect


def guest_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')
        return view_func(request, *args, **kwargs)
    return wrap
