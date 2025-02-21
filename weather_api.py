"""
GET https://api.data.gov.my/weather/forecast
GET https://api.data.gov.my/weather/warning
GET https://api.data.gov.my/weather/warning/earthquake

Documentation: https://developer.data.gov.my/realtime-api/weather#weather-api-endpoint

Forecasts are 7 days in advance

State:
Penang = St003, Georgetown = Tn013, Butterworth = Tn014
Pahang = St007, Cameron Highlands = Rc008, Genting Highlands = Rc016
Perak = St004, Ipoh = Tn041
Johor = St013, Johor Bahru = Ds090, Senai = Tn136
Kuala Lumpuer = Ds058
"""

import requests

FORECAST_URL = 'https://api.data.gov.my/weather/forecast/'
WARNING_URL = 'https://api.data.gov.my/weather/warning/'
EARTHQUAKE = 'https://api.data.gov.my/weather/warning/earthquake/'

places_list = ["Tn013", "Tn014",
               "Rc008", #"Rc016",
               "Tn041",
               "Ds090", "Tn136", "Ds058"]

def forecasting(places):
    r"""Prints out table of summary forecast

    :param: target places (type list)
    :return: location, Table containing date, and summary forecast of that day
    """

    try:
        print(f'|{"Date":-^15}|{"Summary Forecast":-^29}|')

        for place in places:
            myurl = FORECAST_URL + f'?contains={place}@location__location_id&limit=7'
            response = (requests.get(myurl, timeout=15)).json()
            # Add timeout toprevent it from getting stuck on unresponsive servers

            # Print the location in center
            print(f'\n|{response[0]["location"]["location_name"]:-^45}|')

            for i in range(7):      # Repeat for 7 days
                # Print the date and summary forecast
                print(f'|{response[i]["date"]:^15}|{response[i]["summary_when"]:^29}|')
                print(f'|{response[i]["summary_forecast"]:>40}     |')
                print(f'|Min Temp:{response[i]["min_temp"]:^13}|Max Temp:{response[i]["max_temp"]:^13}|')

    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('Error:', e)
        # return None

def warning(url, limit: int):
    r"""Prints output for warning from MET Malaysia

    :param: url and output limit
    :return: response.json
    """
    try:
        url += f'?limit={limit}'
        response = requests.get(url, timeout=15)
        # Add timeout toprevent it from getting stuck on unresponsive servers
        result = response.json()
        print('\n!!! Weather Warning !!!')

        for i in range(limit):
            print(f'Date issued: {result[i]["warning_issue"]["issued"][:10]}')
            print(f'Title: {result[i]["warning_issue"]["title_en"]}')
            print(f'Detail: {result[i]["text_en"]}')
        return result

    except requests.exceptions.Timeout:
        print("Request timed out.")
        return None

    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return None


def earfquake(url, limit: int):
    r"""Prints out earthquake warning

    :param: url and output limit
    :return: response.json
    """
    try:
        url += f'?limit={limit}'
        response = requests.get(url, timeout=15)
        # Add timeout toprevent it from getting stuck on unresponsive servers
        result = response.json()
        print('\n!!! Earthquake warning !!!')

        for i in range(limit):
            print(f'Date issued: {result[i]["localdatetime"][:10]}')
            print(f'Location: {result[i]["location_original"]}')
            print(f'Magnitue: {result[i]["magdefault"]} {result[i]["magtypedefault"]}')
            print(f'Status: {result[i]["status"]}')
        return result

    except requests.exceptions.Timeout:
        print("Request timed out.")
        return None

    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return None


if __name__ == '__main__':
    forecasting(places_list)
    warning(WARNING_URL, limit=2)
    earfquake(EARTHQUAKE, limit=2)
