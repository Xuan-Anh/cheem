from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import pandas as pd

import lib.dailyforecast as daily_forecast
from lib.apiutil import request_headers

app = Flask(__name__)
api = Api(app)

lat, lon = 21.001533, 105.852815
day = 7


def handleFail(err):
    # API call failed...
    print('Status code: %d' % (err.status_code))


@app.route('/showdays', methods=['POST'])
def show_days():
    input = request.args.to_dict()
    if('day' in input):
        day = input['day']
    if('city' in input):
        city = requests.get(
            'https://nominatim.openstreetmap.org/search/{}?format=json'.format(input['city'])).json()
        global lat, lon
        lat = city[0]['lat']
        lon = city[0]['lon']
        print(lat, lon)

    url, params = daily_forecast.request_options(lat, lon)
    print(url, params)

    headers = request_headers()

    r = requests.get(url, params=params, headers=headers)
    if(r.status_code == 200):
        # df = pd.DataFrame(r.json())
        # print(r.json())
        daily_forecast.handle_response(r.json())
    else:
        handleFail(r)

    df = pd.read_csv('Thời tiết.csv')

    dict_df = df.to_dict('dict')
    print(dict_df)

    return jsonify(dict_df)


@app.route('/showdetails', methods=['GET'])
def show_details():
    input = request.args.to_dict()
    if('day' in input):
        day = input['day']
    if('city' in input):
        city = requests.get(
            'https://nominatim.openstreetmap.org/search/{}?format=json'.format(input['city'])).json()
        global lat, lon
        lat = city[0]['lat']
        lon = city[0]['lon']
        print(lat, lon)

    url, params = daily_forecast.request_options(lat, lon)
    print(url, params)

    headers = request_headers()

    r = requests.get(url, params=params, headers=headers)
    if(r.status_code == 200):
        # df = pd.DataFrame(r.json())
        # print(r.json())
        daily_forecast.handle_response(r.json())
    else:
        handleFail(r)

    df = pd.read_csv('Cụ thể theo ngày.csv')

    dict_df = df.to_dict('dict')
    print(dict_df)

    return jsonify(dict_df)


if __name__ == '__main__':
    app.run()
# khong set debug=true
