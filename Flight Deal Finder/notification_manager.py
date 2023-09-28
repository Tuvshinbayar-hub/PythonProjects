import smtplib
import os

my_email = os.environ.get('email')
password = 'vjvljjlgyfkibsba'


class NotificationManager:
    @staticmethod
    def send_email(message: str):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=os.environ.get('email'),
                msg=f'Subject:Low Price Alert!\n\n{message}'
            )
