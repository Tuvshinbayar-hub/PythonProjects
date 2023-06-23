import smtplib
import datetime as dt
import random

# Email section
my_email = 'gtuvshin369@gmail.com'
password = 'vjvljjlgyfkibsba'


def send_email(message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="gtuvshin369@gmail.com",
            msg=f'Subject:Motivational quote for you\n\n {message}'
        )


# Data section
def get_random_quote():
    with open('data/quotes.txt', 'r') as data:
        quotes = data.readlines()
        return random.choice(quotes)


# Time section
now = dt.datetime.now()

if now.weekday() == 4:
    print('sending email')
    send_email(get_random_quote())
    print('done')

