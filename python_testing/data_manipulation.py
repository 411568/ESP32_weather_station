import datetime

import thingspeak_api as tsp_api
from dateutil.relativedelta import relativedelta
import math
import pandas as pd
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX

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
def change_date_range(date_range, predictions, temperature, humidity, pressure, illumination, wind_speed, rain):
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

    if((predictions == True) and (len(date_list) > 0)):
        # add predicted data
        for n in range(0, 10):
            date_list.append(date_list[len(date_list) - 1] + relativedelta(days=n))
            temperature_list.append(0.0)
            humidity_list.append(0.0)
            pressure_list.append(0.0)
            illumination_list.append(0.0)
            wind_speed_list.append(0.0)
            rain_list.append(0.0)

        #auto arima models
        model_temp = SARIMAX(temperature_list, order=(0, 1, 2), seasonal_order=(0,1,2,4)).fit(dis=-1)
        print(model_temp.summary())
      #  predicted_temp = pd.Series(model_temp.predict(n_perdiods = len(temperature_list)))
      #  temperature_list.extend(predicted_temp)
