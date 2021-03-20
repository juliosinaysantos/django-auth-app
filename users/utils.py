from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy


def send_user_email_verification(request, user):
    url = request.build_absolute_uri(reverse_lazy('users:verify-email'))
    token = user.email_verification_token
    full_url = f'{url}?token={token}'

    subject = '[Auth App] Please verify your email address.'
    from_mail = 'no-reply@authteam.com'
    to_mail = user.email
    text_content = 'content'
    html_content = render_to_string('emails/email_verification.html', {'user': user, 'url': full_url})

    send_mail(subject, text_content, from_mail, [to_mail], html_message=html_content)
