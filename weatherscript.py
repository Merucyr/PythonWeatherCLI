import requests
import socket
from datetime import datetime

# Your API Key for IPStack
ipstack_key = 'YOURAPIKEYHERE'

# Gets your IP Address using ipify api, creates the request string for location from ip
computer_ip             = requests.get('https://api.ipify.org?format=json')
computer_ip_json        = computer_ip.json()
location_request_string = 'http://api.ipstack.com/' + computer_ip_json['ip'] + '?access_key=' + ipstack_key

# Gets your latitude/longitude from ipstack api
lr_headers        = {
    'User-Agent': 'Merucyr Weather Script 1.0'
}
location_req      = requests.get(location_request_string, headers=lr_headers)
location_req_json = location_req.json()

latitude  = str(location_req_json['latitude'])
longitude = str(location_req_json['longitude'])

# Uses lat/lon to get your actual 7-Day and Hourly forecasts, both contained in weather's point request api
weather_point_request_string = 'https://api.weather.gov/points/' + latitude + ',' + longitude

weather_req      = requests.get(weather_point_request_string)
weather_req_json = weather_req.json()

seven_day_forecast_string = weather_req_json['properties']['forecast']
hourly_forecast_string    = weather_req_json['properties']['forecastHourly']

seven_day_req      = requests.get(seven_day_forecast_string)
seven_day_req_json = seven_day_req.json()

hourly_req      = requests.get(hourly_forecast_string)
hourly_req_json = hourly_req.json()

# Periods are tables with numbered tables inside of them, period 0 being the current hour
seven_day_periods  = seven_day_req_json['properties']['periods']
hourly_req_periods = hourly_req_json['properties']['periods']

current_hour        = hourly_req_periods[0]
current_datetime    = datetime.fromisoformat(current_hour['startTime'])
current_datetime_hr = current_datetime.strftime("%H:%M")
current_temperature = str(current_hour['temperature'])
print('The current temperature is approx: ' + current_temperature + ', as of: ' + current_datetime_hr)