from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import pandas as pd
import numpy as np

import lib.dailyforecast as daily_forecast
from lib.apiutil import request_headers
from water_plant_need import water_coeff, plant_progress, climate

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
        global day
        day = input['day']
    if('city' in input):
        city = requests.get(
            'https://nominatim.openstreetmap.org/search/{}?format=json'.format(input['city'])).json()
        global lat, lon
        lat = city[0]['lat']
        lon = city[0]['lon']
        print(lat, lon)

    url, params = daily_forecast.request_options(lat, lon, day)
    print(url, params)

    headers = request_headers()

    r = requests.get(url, params=params, headers=headers)
    if(r.status_code == 200):
        # df = pd.DataFrame(r.json())
        # print(r.json())
        daily_forecast.handle_response(r.json())
    else:
        handleFail(r)

    df_days = pd.read_csv('Thời tiết.csv')

    dict_df = df_days.to_dict('dict')
    # print(dict_df)

    return jsonify(dict_df)


@app.route('/showdetails', methods=['POST'])
def show_details():
    input = request.args.to_dict()
    global day
    if('day' in input):
        day = input['day']
    if('city' in input):
        city = requests.get(
            'https://nominatim.openstreetmap.org/search/{}?format=json'.format(input['city'])).json()
        global lat, lon
        lat = city[0]['lat']
        lon = city[0]['lon']
        print(lat, lon)

    url, params = daily_forecast.request_options(lat, lon, day)
    print(url, params)

    headers = request_headers()

    r = requests.get(url, params=params, headers=headers)
    if(r.status_code == 200):
        # df = pd.DataFrame(r.json())
        # print(r.json())
        daily_forecast.handle_response(r.json())
    else:
        handleFail(r)

    df_details = pd.read_csv('Cụ thể theo ngày.csv')

    print(df_details[['Ngày cụ thể', 'Nhiệt độ',
                      'Phần trăm độ ẩm', 'Khả năng có mưa', 'Lượng mưa']])

    dict_df = df_details.to_dict('dict')

    return jsonify(dict_df)


@app.route('/waterIrrigate', methods=['POST'])
def water_irrigate():
    input = request.args.to_dict()
    if('tree' in input):
        tree = input['tree']
    else:
        tree = 'Lúa mạch'
    global day
    if('day' in input):
        day = input['day']
    if('city' in input):
        city = requests.get(
            'https://nominatim.openstreetmap.org/search/{}?format=json'.format(input['city'])).json()
        global lat, lon
        lat = city[0]['lat']
        lon = city[0]['lon']
        print(lat, lon)

    url, params = daily_forecast.request_options(lat, lon, day)
    print(url, params)

    headers = request_headers()
    r = requests.get(url, params=params, headers=headers)
    if(r.status_code == 200):
        # df = pd.DataFrame(r.json())
        # print(r.json())
        daily_forecast.handle_response(r.json())
    else:
        handleFail(r)
    df_details = pd.read_csv('Cụ thể theo ngày.csv')
    df_details = df_details[1:]
    df_details.reset_index(inplace=True)
    water_coef = water_coeff()
    plant_progres = plant_progress()
    climates = climate()
    # print(df_details.fillna(0))

    df_details['Nước cỏ'] = df_details['Nhiệt độ'].apply(lambda x:
                                                         climates[(climates['Nhiệt độ trung bình hằng ngày'] == 'Thấp (dưới 15 ° C)') & (
                                                             climates['Vùng khí hậu'] == 'Ẩm ướt')]['Lượng nước']
                                                         if x < 15 else
                                                         climates[(climates['Nhiệt độ trung bình hằng ngày'] == 'Cao (hơn 25 ° C)') & (
                                                             climates['Vùng khí hậu'] == 'Ẩm ướt')]['Lượng nước']
                                                         if x > 25 else
                                                         climates[(climates['Nhiệt độ trung bình hằng ngày'] == 'Trung bình (15-25 ° C)')
                                                                  & (climates['Vùng khí hậu'] == 'Ẩm ướt')]['Lượng nước']
                                                         )

    water_coef_tree_np = water_coef[water_coef['Mùa vụ'].str.contains(
        tree)].to_numpy()
    water_coef_tree_np = water_coef_tree_np[:, 1:].astype(float)
    nuoc_co_np = df_details['Nước cỏ'].to_numpy()
    nuoc_co_np = nuoc_co_np.reshape((-1, 1)).astype(float)

    water_need = np.matmul(nuoc_co_np, water_coef_tree_np)

    #water_need = pd.DataFrame(water_need,columns=[['Giai đoạn đầu','Giai đoạn phát triển cây trồng','Giai đoạn giữa mùa','Giai đoạn cuối mùa']])

    rain_fall = df_details['Lượng mưa']
    absorbing_plant = rain_fall.apply(lambda x: (
        x*0.8 - 25) if x > 75 else 0 if(x*0.6 < 10) else (x*0.6 - 10)).astype(float)

    first_stage = water_need[:, 0] + absorbing_plant
    grow_stage = water_need[:, 1] + absorbing_plant
    mid_stage = water_need[:, 2] + absorbing_plant
    final_stage = water_need[:, 3] + absorbing_plant

    water_need_irrigate = pd.DataFrame(zip(first_stage, grow_stage, mid_stage, final_stage), columns=[
                                       'Giai đoạn đầu', 'Giai đoạn phát triển cây trồng', 'Giai đoạn giữa mùa', 'Giai đoạn cuối mùa'])

    print(water_need_irrigate)
    water_need_irrigate = water_need_irrigate.to_dict('dict')

    return jsonify(water_need_irrigate)


if __name__ == '__main__':
    app.run(debug=True)
