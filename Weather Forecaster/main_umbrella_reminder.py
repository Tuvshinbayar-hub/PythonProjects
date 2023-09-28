import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

LAT = 47.921230
LNG = 106.918556

API_KEY = os.environ.get('api_key')
load_dotenv('.env')

params = {
    'days': 2,
    'aqi': 'no',
    'alerts': 'no',
    'q': 'Ulaanbaatar',
    'key': API_KEY
}

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('auth_token')

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

if will_rain:
    message = client.messages.create(
        to='phone number',
        body='Bring an umbrella',
        from_='+12058518156'
    )
    print(message.sid)
