import smtplib

import requests
import time
from datetime import datetime
from pytz import timezone

MY_LAT = 47.921230
MY_LONG = 106.918556

MY_EMAIL = 'username@gmail.com'
MY_PASSWORD = 'vjvljjlgyfkibsba'


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()


# Time converting section
sunrise_utc = datetime.fromisoformat(data['results']['sunrise'])
sunset_utc = datetime.fromisoformat(data['results']['sunset'])

time_zone = timezone('Asia/Ulaanbaatar')
sunrise_local = sunrise_utc.astimezone(time_zone)
sunset_local = sunset_utc.astimezone(time_zone)

sunrise_hour = int(str(sunrise_local.time()).split(':')[0])
sunrise_minute = int(str(sunrise_local.time()).split(':')[1])

sunset_hour = int(str(sunset_local.time()).split(':')[0])
sunset_minute = int(str(sunset_local.time()).split(':')[1])

# print(sunrise_hour, sunrise_minute)
# print(sunset_hour, sunset_minute)
time_now = datetime.now()


def is_iss_overhead():
    if abs(iss_latitude - MY_LAT) <= 5 and abs(iss_longitude - MY_LONG):
        return True
    else:
        return False


def is_dark():
    temp_time = time_now.time()

    if temp_time.hour - sunset_hour >= 1:
        return True
    elif temp_time.hour - sunset_hour == 0 and temp_time.minute - sunset_minute >= 0:
        return True
    if sunrise_hour - temp_time.hour <= 1:
        return True
    elif sunrise_hour - temp_time.hour == 0 and sunrise_minute - temp_time.minute <= 0:
        return True
    else:
        return False


def send_email():
    with smtplib.SMTP('smtp.gmail.com') as smtp:
        smtp.starttls()
        smtp.login(user=MY_EMAIL, password=MY_PASSWORD)
        smtp.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:ISS is over your head\n\nLook up it's over you!"
        )


def program():
    if is_iss_overhead() and is_dark():
        send_email()


while True:
    program()
    time.sleep(60)




