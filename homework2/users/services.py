from django.core.mail import send_mail
from config import settings


def send_verification_code(register_email, full_url):
    send_mail(
        'Подтверждение почты',
        f'Для подтверждения вашей почты введите код на странице подтверждения: {full_url}',
        settings.EMAIL_HOST_USER,
        [register_email]
    )