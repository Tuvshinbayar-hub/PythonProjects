import requests
from datetime import datetime
from pytz import timezone


params = {
    'lat': 47.9184676,
    'lng': 106.9177016,
    'formatted': 0
}

response = requests.get(url='https://api.sunrise-sunset.org/json', params=params)
response.raise_for_status()
data = response.json()

sunrise_utc = datetime.fromisoformat(data['results']['sunrise'])
sunset_utc = datetime.fromisoformat(data['results']['sunset'])

time_zone = timezone('Asia/Ulaanbaatar')
sunrise_local = sunrise_utc.astimezone(time_zone)
sunset_local = sunset_utc.astimezone(time_zone)

print(sunset_local)
print(sunrise_local)
