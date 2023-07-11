import requests
import pytz
import os
from datetime import datetime

API_ID = 'deab2a44'
API_KEY = 'a270eb1378389440fadb01ed374db84d'
END_POINT_EXERCISE = 'https://trackapi.nutritionix.com/v2/natural/exercise'

END_POINT_SHEETY = 'https://api.sheety.co/83df345384271044dfb6fababc306384/workoutPlan/sheet1'
TOKEN_SHEETY = 'Bearer e)js8jQ!ASw5'


def get_exercise_info(query: str):
    headers = {
        'x-app-id': API_ID,
        'x-app-key': API_KEY,
        'Content-Type': 'application/json'
    }

    body = {
        'query': query,
        'gender': 'male',
        'weight_kg': 86,
        'height_cm': 170,
        'age': 25
    }

    response = requests.post(url=END_POINT_EXERCISE, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def get_google_sheet():
    response = requests.get(url=END_POINT_SHEETY)
    response.raise_for_status()
    print(response.json())

# get_google_sheet()


def add_row_to_google_sheet():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': TOKEN_SHEETY
    }
    asia_ub = pytz.timezone('Asia/Ulaanbaatar')

    time_date = datetime.now(asia_ub).strftime('%d/%m/%Y')
    time_hour = datetime.now(asia_ub).strftime('%H:%M:%S')

    body = {
        'sheet1': {
            'date': time_date,
            'time': time_hour,
            'exercise': str.title(exercise_name),
            'duration': duration_min,
            'calories': nf_calories
        }
    }

    response = requests.post(url=END_POINT_SHEETY, json=body, headers=headers)
    response.raise_for_status()
    print(response.json())


user_input = input('What exercises did you do?: ')
exercises_list = get_exercise_info(user_input)['exercises']

if len(exercises_list) > 0:
    for exercise in exercises_list:
        duration_min = exercise['duration_min']
        nf_calories = exercise['nf_calories']
        exercise_name = exercise['name']

        # Google Sheets
        add_row_to_google_sheet()

