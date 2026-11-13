from unittest.mock import patch

from django.test import SimpleTestCase

from users.tasks import send_welcome_email


class WelcomeEmailTaskTests(SimpleTestCase):
    @patch("users.tasks.send_email")
    def test_task_sends_all_email_fields(self, mock_send_email):
        send_welcome_email.run("New User", "new@example.com", "Welcome", "Hello!")

        mock_send_email.assert_called_once_with(
            to_name="New User",
            to_email="new@example.com",
            subject="Welcome",
            text="Hello!",
        )

    @patch("users.tasks.send_email", side_effect=RuntimeError("Mail service unavailable"))
    def test_delivery_failure_propagates_to_worker(self, mock_send_email):
        with self.assertRaisesMessage(RuntimeError, "Mail service unavailable"):
            send_welcome_email.run("New User", "new@example.com", "Welcome", "Hello!")
