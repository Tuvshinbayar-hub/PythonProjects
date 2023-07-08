from typing import Callable

import requests
from datetime import datetime

API_ENDPOINT_PIXELA = 'https://pixe.la/v1/users'
TOKEN = 'e)js8jQ!ASw5'
USERNAME = 'tuvshuu'
GRAPH_ID_01 = 'graph1'


def create_user():
    user_config = {
        'token': TOKEN,
        'username': USERNAME,
        'agreeTermsOfService': 'yes',
        'notMinor': 'yes',
    }

    respond = requests.post(url=API_ENDPOINT_PIXELA, json=user_config)
    print(respond.json())


def create_graph():
    headers = {
        'X-USER-TOKEN': TOKEN
    }

    graph_config = {
        'id': GRAPH_ID_01,
        'name': 'Reading Graph',
        'unit': 'minute',
        'type': 'int',
        'color': 'shibafu',
        'timezone': 'Asia/Ulaanbaatar'
    }

    response = requests.post(url=f'{API_ENDPOINT_PIXELA}/{USERNAME}/graphs', json=graph_config, headers=headers)
    print(response.text)


def try_post_pixel(quantity: int, date: str = ''):
    headers = {
        'X-USER-TOKEN': TOKEN
    }

    today = datetime.today().strftime('%Y%m%d')

    if date == '':
        date = today

    pixel_config = {
        'date': date,
        'quantity': str(quantity),
    }

    response = requests.post(url=f'{API_ENDPOINT_PIXELA}/{USERNAME}/graphs/{GRAPH_ID_01}',
                             json=pixel_config,
                             headers=headers)
    return response.json()


def try_update_pixel(quantity: int, date: str = ''):
    headers = {
        'X-USER-TOKEN': TOKEN
    }

    today = datetime.today().strftime('%Y%m%d')

    if date == '':
        date = today

    pixel_config = {
        'quantity': str(quantity),
    }

    response = requests.put(url=f'{API_ENDPOINT_PIXELA}/{USERNAME}/graphs/{GRAPH_ID_01}/{date}', json=pixel_config,
                            headers=headers)
    return response.json()


def try_delete_pixel(date: str = ''):
    headers = {
        'X-USER-TOKEN': TOKEN
    }

    today = datetime.today().strftime('%Y%m%d')

    if date == '':
        date = today

    response = requests.delete(url=f'{API_ENDPOINT_PIXELA}/{USERNAME}/graphs/{GRAPH_ID_01}/{date}', headers=headers)

    return response.json()


# This function ensures successful updates with a 25% chance due to payment.
def execute_function(function_with_chance: Callable, date: str = '', **kwargs):
    response_sms = function_with_chance(kwargs.get('quantity'), date)

    while response_sms['message'] != 'Success.':
        response_sms = function_with_chance(kwargs.get('quantity'), date)
        print(response_sms)


execute_function(try_post_pixel, '20230706', quantity=25)
