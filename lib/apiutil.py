import os

__name__ = 'dailyforecast'

host = 'https://api.weather.com'


def default_params():
    return{
        'apiKey': '2b6ed19f3d474152aed19f3d4791527d',
        'language': 'en-US'
    }


def request_headers():
    return {
        'User-Agent': 'Request-Promise',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip'
    }
