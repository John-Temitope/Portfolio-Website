import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

class Email:

    def __init__(self):
        self.MY_EMAIL = os.getenv("MY_EMAIL")
        self.PASSWORD = os.getenv("PASSWORD")
        self.SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
        self.RECIPIENT = os.getenv("RECIPIENT")


    def post_email(self, name, email, phone, message):
        with smtplib.SMTP_SSL(self.SMTP_ADDRESS, 465) as connection:
            connection.login(user=self.MY_EMAIL, password=self.PASSWORD)
            connection.sendmail(
                    from_addr=self.MY_EMAIL,
                    to_addrs=self.RECIPIENT,
                    msg=f"Subject: New Portfolio Connection!\n\n"
                        f"Name: {name} \nEmail: {email} \nPhone: {phone} \nMessage: {message}"
            )