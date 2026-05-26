from html import escape

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError

from .mail_services import send_email


@method_decorator(csrf_exempt, name="dispatch")
class TestEmailView(View):
    def get(self, request):
        return HttpResponse(self._render_form())

    def post(self, request):
        to_name = request.POST.get("to_name", "").strip()
        to_email = request.POST.get("to_email", "").strip()
        subject = request.POST.get("subject", "").strip()
        text = request.POST.get("text", "").strip()

        if not to_name or not to_email or not subject or not text:
            return HttpResponse(
                self._render_form("Please fill in all fields.", is_error=True),
                status=400,
            )

        try:
            result = send_email(to_name, to_email, subject, text)
        except ValidationError as exc:
            return HttpResponse(
                self._render_form(f"Mailjet error: {exc.detail}", is_error=True),
                status=400,
            )

        return HttpResponse(
            self._render_form(f"Email sent. Mailjet status: {result.status_code}")
        )

    def _render_form(self, message=None, is_error=False):
        message_html = ""

        if message:
            color = "crimson" if is_error else "green"
            message_html = f'<p style="color: {color};">{escape(message)}</p>'

        return f"""
        <!doctype html>
        <html>
            <head>
                <title>Test Email</title>
            </head>
            <body>
                <h1>Test Mailjet Email</h1>
                {message_html}
                <form method="post">
                    <p>
                        <label>Name</label><br>
                        <input name="to_name" required>
                    </p>
                    <p>
                        <label>Email</label><br>
                        <input name="to_email" type="email" required>
                    </p>
                    <p>
                        <label>Subject</label><br>
                        <input name="subject" required>
                    </p>
                    <p>
                        <label>Message</label><br>
                        <textarea name="text" rows="6" cols="50" required></textarea>
                    </p>
                    <button type="submit">Send test email</button>
                </form>
            </body>
        </html>
        """
