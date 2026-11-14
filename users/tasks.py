from celery import shared_task

from common.mail_services import send_email


@shared_task(ignore_result=True)
def send_welcome_email(name, email, subject, text):
    send_email(
        to_name=name,
        to_email=email,
        subject=subject,
        text=text,
    )
