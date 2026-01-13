import os
import resend


resend.api_key = os.getenv("RESEND_API_KEY")

class Email:

    def __init__(self):
        self.SENDER = os.getenv("SENDER")
        self.RECIPIENT = os.getenv("RECIPIENT")

        if not all([self.SENDER, self.RECIPIENT, resend.api_key]):
            raise RuntimeError("Email environment variables not set")


    def post_email(self, name, email, phone, message):
        """Using resend API to send an email """

        try:
            # Suppress PyCharm TypedDict type-checking warning for Resend params using noinspection
            # noinspection PyTypeChecker
            params: resend.Emails.SendParams = {
                "from": f"Portfolio <{self.SENDER}>",
                "to": [self.RECIPIENT],
                "subject": "New Portfolio Connection!",
                "html": f"""
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Phone:</strong> {phone}</p>
                    <p><strong>Message:</strong> {message}</p>
                """
            }

            # Send the email
            response = resend.Emails.send(params)
            return response

        except Exception as e:
            raise RuntimeError(f"Resend email failed: {e}")

