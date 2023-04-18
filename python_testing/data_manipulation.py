import datetime

import thingspeak_api as tsp_api
from dateutil.relativedelta import relativedelta
import math

# channel id
test_channel_id = 2071282

# getting the data
temperature = []
humidity = []
pressure = []
illumination = []
rain = []
wind_speed = []
battery_level = []


# lists of data
date_list = []
temperature_list = []
humidity_list = []
pressure_list = []
illumination_list = []
rain_list = []
wind_speed_list = []
#battery_level_value = 0

# get new data from thingspeak api
def update_data_from_api():
    # getting the data again
    temperature = tsp_api.get_data_from_field(test_channel_id, 1)  # temperature
    humidity = tsp_api.get_data_from_field(test_channel_id, 2)  # humidity
    pressure = tsp_api.get_data_from_field(test_channel_id, 3)  # pressure
    illumination = tsp_api.get_data_from_field(test_channel_id, 5)  # illimination
    rain = tsp_api.get_data_from_field(test_channel_id, 6)  # rain
    wind_speed = tsp_api.get_data_from_field(test_channel_id, 7)  # wind speed
    battery_level = tsp_api.get_data_from_field(test_channel_id, 8) # battery level

    temperature_list.clear()
    humidity_list.clear()
    pressure_list.clear()
    illumination_list.clear()
    rain_list.clear()
    wind_speed_list.clear()

    # list of dates
    date_list.clear()
    for n in range(0, len(temperature)):
        date_list.append(tsp_api.parse_date_string(temperature[n][0]))

    # convert values
    for n in range(0, len(date_list)):
        temperature_list.append(float(temperature[n][1]))
        humidity_list.append(float(humidity[n][1]))
        pressure_list.append(float(pressure[n][1]))
        illumination_list.append(float(illumination[n][1]))
        rain_list.append(float(rain[n][1]))
        wind_speed_list.append(float(wind_speed[n][1]))

    # get the last battery level reading
    global battery_level_value
    battery_level_value = battery_level[len(date_list) - 1][1]

    return temperature, humidity, pressure, illumination, wind_speed, rain


# change data range, (date_range parameter tells us what date range we want)
def change_date_range(date_range, temperature, humidity, pressure, illumination, wind_speed, rain):
    # clear all the data lists (we still keep the data in the "temperature", "humidity", etc lists for future use)
    date_list.clear()
    temperature_list.clear()
    humidity_list.clear()
    pressure_list.clear()
    illumination_list.clear()
    rain_list.clear()
    wind_speed_list.clear()


    num_of_days = 10000

    # one day
    if date_range == 0:
        num_of_days = 1
    # one week
    if date_range == 1:
        num_of_days = 7
    # one month
    if date_range == 2:
        num_of_days = 30

    start_date = datetime.datetime.now() - relativedelta(days = num_of_days)

    # list of dates
    for n in range(0, len(temperature)):
        if tsp_api.parse_date_string(temperature[n][0]) > start_date:
            date_list.append(tsp_api.parse_date_string(temperature[n][0]))
            temperature_list.append(float(temperature[n][1]))
            humidity_list.append(float(humidity[n][1]))
            pressure_list.append(float(pressure[n][1]))
            illumination_list.append(float(illumination[n][1]))
            rain_list.append(float(rain[n][1]))
            wind_speed_list.append(float(wind_speed[n][1]))