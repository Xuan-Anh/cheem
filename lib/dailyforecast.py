# Daily Forecast
#
# - https://weather.com/swagger-docs/ui/sun/v1/sunV1DailyForecast.json
#
# The daily forecast API returns the geocode weather forecasts for the current day
# up to the days duration in the API endpoint. The daily forecast product can contain
# multiple days of daily forecasts for each location. Each day of a forecast can
# contain up to (3) “temporal segments” meaning three separate forecasts. For any
# given forecast day we offer day, night, and a 24-hour forecast (daily summary).
#
# Base URL: api.weather.com/v1
# Endpoint: /geocode/{latitude}/{longitude}/forecast/daily/{days}day.json
import pandas 

__name__ = 'dailyforecast'

from lib.apiutil import host, default_params

def request_options (lat, lon, days = 3, units = 'm'):
  d = days if days in [3, 5, 7, 10, 15] else 3
  u = units if units in ['e', 'm', 'h', 's'] else 'm'

  url = host + '/v3/wx/forecast/daily/{}day'.format(days)
  
  params = default_params()
  params['geocode'] = '{lat},{lon}'.format(lat=lat, lon=lon)
  params['format'] = 'json'
  params['units'] = u
  params['language'] = 'en-US'

  return url, params

def handle_response (res):
#   if res and res['forecasts']:
#     forecasts = res['forecasts']
#     print('daily-forecast: returned {}-day forecast'.format(len(forecasts)))

#     # each entry in the forecasts array corresponds to a daily forecast
#     for index, daily in enumerate(forecasts):
#       print('daily-forecast: day {} - High of {}, Low of {}'.format(index, daily['max_temp'], daily['min_temp']))
#       print('daily-forecast: day {} - {}'.format(index, daily['narrative']))

#     # additional entries include (but not limited to):
#     # lunar_phase, sunrise, day['uv_index'], night['wdir'], etc
#   else:
#     print('daily-forecast: no daily forecast returned')
	if (res['calendarDayTemperatureMax'] and res['calendarDayTemperatureMin']):
		temp_max = res['calendarDayTemperatureMax']
		temp_min = res['calendarDayTemperatureMin']
		daysweek = res['dayOfWeek']
		moonphase = res['moonPhase']
		moonrise = res['moonriseTimeLocal']
		moonset = res['moonsetTimeLocal']
		narrative = res['narrative']
		qdf = res['qpf']
		sunrise = res['sunriseTimeLocal']
		sunset = res['sunsetTimeLocal']
		df = pandas.DataFrame({
			'Nhiệt độ cao nhất': temp_max,
			'Nhiệt độ thấp nhất' : temp_min,
			'Ngày trong tuần' : daysweek,
			'Chu kỳ mặt trăng' : moonphase,
			'Trăng lên giờ địa phương' : moonrise,
			'Trăng xuống giờ địa phương' : moonset,
			'Tường thuật' : narrative,
			'Lượng mưa' : qdf,
			'Mặt trời lên' : sunrise,
			'Mặt trời xuống' : sunset
		})
		df.to_csv('Thời tiết.csv',index=False)
		
		print('Cụ thể theo ngày: ')
		day_or_night = res['daypart'][0]['dayOrNight']
		day_part_name = res['daypart'][0]['daypartName']
		cloud_cover = res['daypart'][0]['cloudCover']
		narrative = res['daypart'][0]['narrative']
		precip_chance = res['daypart'][0]['precipChance']
		qpf = res['daypart'][0]['qpf']
		qualifier_phrase = res['daypart'][0]['qualifierPhrase']
		relative_humidity = res['daypart'][0]['relativeHumidity']
		temperature = res['daypart'][0]['temperature']
		feel_like = res['daypart'][0]['temperatureHeatIndex']
		thunder = res['daypart'][0]['thunderIndex']
		uv = res['daypart'][0]['uvDescription']
		wind_phrase = res['daypart'][0]['windPhrase']
		detail = res['daypart'][0]['wxPhraseLong']
		df2 = pandas.DataFrame({
			'Day or Night' : day_or_night,
			'Ngày cụ thể' : day_part_name,
			'Độ che phủ theo ngày' : cloud_cover,
			'Cụ thể' : narrative,
			'Khả năng có mưa' : precip_chance,
			'Lượng mưa' : qpf,
			'Cảnh báo thời tiết' : qualifier_phrase,
			'Phần trăm độ ẩm' : relative_humidity,
			'Nhiệt độ' : temperature,
			'Cảm thấy như' : feel_like,
			'Mức độ giông bão' : thunder,
			'Chỉ số UV' : uv,
			'Hướng gió' : wind_phrase,
			'Mô tả': detail
		})
		df2.to_csv('Cụ thể theo ngày.csv',index=False)

# API = /v3/wx/forecast/daily/{days}day
# API = '/v3/wx/forecast/daily/10day'
# API = '/v3/wx/forecast/daily/7day'
# API = '/v3/wx/forecast/daily/5day'
# API = '/v3/wx/forecast/daily/3day'

# def handleResponse(res):
#   if res and res['dayOfWeek']:
#     days = res['dayOfWeek']
#     print('daily-forecast: returned %d-day forecast' % (len(days)))

#     # each entry in the response object is an array with
#     # entries in the array applying to the day of the week
#     # (i.e., res['dayOfWeek']) matched by the index
#     for index, day in enumerate(days):
#       maxtemp = str(res['temperatureMax'][index]) if res['temperatureMax'][index] else 'n/a'
#       mintemp = str(res['temperatureMin'][index]) if res['temperatureMin'][index] else 'n/a'
#       print ('daily-forecast: %s - High of %s, Low of %s' % (day, maxtemp, mintemp) )
#       print ('daily-forecast: %s - %s' % (day, res['narrative'][index]) )

#     # additional entries include (but not limited to):
#     # moonPhase, sunriseTimeLocal, daypart['precipChance'], daypart['windDirection'], etc
#   else:
#     print('daily-forecast: daily forecast returned')


# def callDailyForecast(lat, lon, units = 'm'):
#   url = HOST + lib.dailyforecast.API
#   options = defaultParams
#   options['qs']['geocode'] = ( '%f,%f' % (lat, lon) )
#   options['qs']['units'] = units

#   r = requests.get( url, params=options['qs'], headers=options['headers'] )
#   if r.status_code == 200:
#     lib.dailyforecast.handleResponse( r.json() )
#   else:
#     handleFail(r)

