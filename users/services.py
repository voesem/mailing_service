from django.conf import settings
from django.core.mail import send_mail


def send_verify_email_message(verification_url, recipient_email):
    send_mail(
        "Код подтверждения",
        f"Пройдите по ссылке, чтобы активировать адрес электронной почты: {verification_url}",
        settings.EMAIL_HOST_USER,
        [recipient_email],
        fail_silently=False,
    )
