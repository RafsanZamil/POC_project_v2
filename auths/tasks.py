from django.core.mail import get_connection, EmailMessage
from POC_project_v2 import settings
from celery import shared_task


@shared_task(bind=True)
def send_notification_mail(self, otp, recipient_list):
    with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = "Email Verification for Blog Application"
        email_from = settings.EMAIL_HOST_USER
        message = "your one time otp key for account verification: {}".format(otp)
        fail_silently = False
        EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
    return "Done"
