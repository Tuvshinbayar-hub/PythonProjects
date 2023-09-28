import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

API_KEY_FLIGHT = os.environ.get('api_key_flight')
END_POINT_SEARCH = 'https://api.tequila.kiwi.com/v2/search'
END_POINT_LOCATION = 'https://api.tequila.kiwi.com/locations/query'


def search_iata(query_city_name):
    headers = {
        'apikey': API_KEY_FLIGHT,
    }

    params = {
        'term': query_city_name,
        'locale': 'en-US'
    }

    response = requests.get(url=END_POINT_LOCATION, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


class FlightSearch:
    def __init__(self, fly_to: str):
        self.result = None
        self.iata = None
        self.search(fly_to)

    def search(self, fly_to: str):
        headers = {
            'apikey': API_KEY_FLIGHT,
        }

        time_now = datetime.now().strftime('%d/%m/%Y')
        time_six_month_after = (datetime.today() + relativedelta(months=+6)).strftime('%d/%m/%Y')

        params = {
            'fly_from': 'UBN',
            'fly_to': fly_to,
            'date_from': time_now,
            'date_to': time_six_month_after,
            'limit': 10,
            'curr': 'USD',
        }
        response = requests.get(url=END_POINT_SEARCH, params=params,  headers=headers)
        response.raise_for_status()
        self.result = response.json()
