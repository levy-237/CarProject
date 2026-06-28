from html import escape

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .mail_services import send_email_safely


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
                self._render_form("Bitte fülle alle Felder aus.", is_error=True),
                status=400,
            )

        result = send_email_safely(to_name, to_email, subject, text)
        if not result:
            return HttpResponse(
                self._render_form("Die E-Mail konnte nicht gesendet werden.", is_error=True),
                status=400,
            )

        return HttpResponse(
            self._render_form(f"E-Mail gesendet. Mailjet-Status: {result.status_code}")
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
                <title>Test-E-Mail</title>
            </head>
            <body>
                <h1>Mailjet-Test-E-Mail</h1>
                {message_html}
                <form method="post">
                    <p>
                        <label>Name</label><br>
                        <input name="to_name" required>
                    </p>
                    <p>
                        <label>E-Mail</label><br>
                        <input name="to_email" type="email" required>
                    </p>
                    <p>
                        <label>Betreff</label><br>
                        <input name="subject" required>
                    </p>
                    <p>
                        <label>Nachricht</label><br>
                        <textarea name="text" rows="6" cols="50" required></textarea>
                    </p>
                    <button type="submit">Test-E-Mail senden</button>
                </form>
            </body>
        </html>
        """
