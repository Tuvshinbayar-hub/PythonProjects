# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_search import search_iata
from notification_manager import NotificationManager

notification_manager = NotificationManager()
data_manager = DataManager()
my_locations = data_manager.data['prices']

flight_search = FlightSearch('PAR')


def update_iata_codes():
    for location in my_locations:
        data_manager.update_row_data(location, iataCode=search_iata(location['city'])['locations'][0]['code'])


def update_info():
    for location in my_locations:
        current_price = int(location['lowestPrice'])
        # current_price_id = location['id']

        flight_search_temp = FlightSearch(location['iataCode'])
        data = flight_search_temp.result['data']
        new_price = int(data[0]['price'])

        if new_price < current_price:
            from_date = data[0]['route'][0]['local_departure'].split('T')[0]
            to_date = data[0]['route'][-1]['local_arrival'].split('T')[0]
            data_manager.update_row_data(location, lowestPrice=new_price, fromDate=from_date, toDate=to_date)

            print('sending email...')
            notification_manager.send_email(f'Low price alert! Only ${new_price} '
                                            f'to fly from {data[0]["cityFrom"]}-{data[0]["flyFrom"]}'
                                            f' to {data[0]["cityTo"]}-{data[0]["flyTo"]}, from {from_date} to {to_date}')
            print('sent!')


# update_iata_codes()
update_info()
