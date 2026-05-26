from django.conf import settings
from mailjet_rest import Client
from rest_framework.exceptions import ValidationError


def get_mailjet_client():
    api_key = settings.MAILJET_API_KEY
    api_secret = settings.MAILJET_API_SECRET

    if not api_key or not api_secret:
        raise ValidationError({"mailjet": "Mailjet API keys are not configured."})

    return Client(auth=(api_key, api_secret), version="v3.1")


def send_email(to_name, to_email, subject, text):
    if not settings.MAILJET_SENDER_EMAIL:
        raise ValidationError({"mailjet": "Mailjet sender email is not configured."})

    data = {
        "Messages": [
            {
                "From": {
                    "Email": settings.MAILJET_SENDER_EMAIL,
                    "Name": settings.MAILJET_SENDER_NAME,
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": to_name,
                    }
                ],
                "Subject": subject,
                "TextPart": text,
            }
        ]
    }

    result = get_mailjet_client().send.create(data=data)
    print(result)

    if result.status_code >= 400:
        raise ValidationError({"mailjet": result.json()})

    return result