import random
import smtplib
import datetime as dt
import pandas as pd
import os

# This is code for sending email to list of people from csv, using smtplib

# Email section
my_email = 'username@email.com'
password = 'vjvljjlgyfkibsba'


def send_email(to_address, msg):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=to_address,
            msg=msg
        )


# Letters section
def get_letter(receiver_name):
    path = 'letter_templates'
    with os.scandir(path) as entries:
        entry_list = list(entries)
        random_entry = random.choice(entry_list)
        with open(random_entry) as letter:
            return letter.read().replace('[NAME]', receiver_name)


# Date section
now = dt.datetime.now()
birthdays = pd.read_csv('birthdays.csv')
birthdays_list = birthdays.to_dict(orient='records')
for birthday in birthdays_list:
    if birthday['month'] == now.month and birthday['day'] == now.day:
        print('sending')
        send_email(birthday['email'], msg=f"Subject:Happy birthday!\n\n{get_letter(birthday['name'])}")
        print('sent!')
