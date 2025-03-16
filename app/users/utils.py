import smtplib
from django.core.mail import send_mail
from django.conf import settings


def envoyer_email(email,message):
    subject = "Verification"
    body = message
    email='23010@supnum.mr'
    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER, 
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        return False