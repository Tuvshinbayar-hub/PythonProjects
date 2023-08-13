import requests

ENDPOINT_SHEETY = 'https://api.sheety.co/83df345384271044dfb6fababc306384/flightDeal/prices'


class DataManager:
    def __init__(self):
        self.data = None
        self.get_data()

    def get_data(self):
        response = requests.get(url=ENDPOINT_SHEETY)
        response.raise_for_status()
        self.data = response.json()

    def update_row_data(self, dic_row: dict, **kwargs):
        body = dic_row
        for key, value in kwargs.items():
            if value is not None:
                body[key] = kwargs.get(key)

        actual_body = {
            'price': body
        }

        response = requests.put(url=f"{ENDPOINT_SHEETY}/{dic_row['id']}", json=actual_body)
        response.raise_for_status()
        self.get_data()
