import requests
import datetime
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

STOCK = 'TSLA'
COMPANY_NAME = 'Tesla Inc'
API_KEY_ALPHAVANTAGE = 'NINHBCLNZIKWKS15'
API_KEY_NEWSAPI = 'eef53b5bc0b544fcb67eb1b5e823acad'

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

today_date = datetime.datetime.today()
yesterday_date = str((today_date - datetime.timedelta(days=1)).date())
two_days_before_date = str((today_date - datetime.timedelta(days=2)).date())


def get_price_diff_percent():
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': 'EURUSD',
        'apikey': API_KEY_ALPHAVANTAGE,
    }

    response = requests.get(url='https://www.alphavantage.co/query?', params=params)
    response.raise_for_status()

    yesterday_price = float(response.json()['Time Series (Daily)'][yesterday_date]['4. close'])
    two_days_before_price = float(response.json()['Time Series (Daily)'][two_days_before_date]['4. close'])

    price_diff_percent = (two_days_before_price - yesterday_price)/two_days_before_price * 100

    if price_diff_percent > 0:
        return '↑ ' + str(abs(round(price_diff_percent, 2)))
    else:
        return '↓ ' + str(abs(round(price_diff_percent, 2)))

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


def get_news():
    params = {
        'q': 'forex',
        'apiKey': API_KEY_NEWSAPI,
        'category': 'business',
    }
    respond = requests.get(url='https://newsapi.org/v2/top-headlines?', params=params)
    respond.raise_for_status()

    if len(respond.json()['articles']) > 0:
        return respond.json()['articles'][0]['description']
    else:
        return None

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


def send_sms(sms_content: str, price_diff_percent: str):
    # proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    account_sid = 'AC6b9cf55cb2c5532da92d9641f0666044'
    auth_token = '653c5e602e30c2b0243fd7a195f4eafe'
    client = Client(account_sid, auth_token)
    # client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages.create(
        to='+97699369096',
        body=f'EURUSD: {price_diff_percent}\nBrief: {sms_content}',
        from_='+12058518156'
    )
    print(message.sid)


news = get_news()
price_diff = get_price_diff_percent()

if news is not None:
    send_sms(news, price_diff)

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


