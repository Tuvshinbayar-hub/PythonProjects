import smtplib

my_email = 'gtuvshin369@gmail.com'
password = 'vjvljjlgyfkibsba'


class NotificationManager:
    @staticmethod
    def send_email(message: str):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="gtuvshin369@gmail.com",
                msg=f'Subject:Low Price Alert!\n\n{message}'
            )
