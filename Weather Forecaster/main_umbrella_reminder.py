import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

LAT = 47.921230
LNG = 106.918556

API_KEY = 'b18e792815c141649d965148233006'
load_dotenv('.env')
# b18e792815c141649d965148233006

params = {
    'days': 2,
    'aqi': 'no',
    'alerts': 'no',
    'q': 'Ulaanbaatar',
    'key': API_KEY
}

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

account_sid = 'AC6b9cf55cb2c5532da92d9641f0666044'
auth_token = '653c5e602e30c2b0243fd7a195f4eafe'

# here http_client must be added due to functions with free tier of twilio
client = Client(account_sid, auth_token, http_client=proxy_client)

response = requests.get(url=f'https://api.weatherapi.com/v1/forecast.json', params=params)
response.raise_for_status()
weather_data = response.json()

will_rain = False

for hour in range(7, 19):
    if weather_data['forecast']['forecastday'][0]['hour'][hour]['will_it_rain'] == 1:
        will_rain = True

print(os.getenv('API_KEY'))

# if will_rain:
#     message = client.messages.create(
#         to='+97699369096',
#         body='Bring an umbrella',
#         from_='+12058518156'
#     )
#     print(message.sid)
