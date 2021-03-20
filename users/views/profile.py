from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import email_verification_required


@login_required
@email_verification_required
def profile(request):
    return render(request, 'users/profile.html')
