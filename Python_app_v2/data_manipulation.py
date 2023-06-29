import datetime
from PyQt5.QtWidgets import *

import thingspeak_api as tsp_api
from dateutil.relativedelta import relativedelta
import math
import pandas as pd
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima.arima import auto_arima

# channel id
test_channel_id =  2071282   #2208447  #

# all the data from server
temperature = []
humidity = []
pressure = []
illumination = []
rain = []
wind_speed = []
battery_level = []

# sarima models
arima_model_temperature = None
arima_model_pressure = None
arima_model_humidity = None
arima_model_ill = None
arima_model_wind = None
arima_model_rain = None

# lists of data
date_list = []
temperature_list = []
humidity_list = []
pressure_list = []
illumination_list = []
rain_list = []
wind_speed_list = []
battery_level_value = 0


# get new data from thingspeak api
def update_data_from_api():
    global temperature
    global humidity
    global pressure
    global illumination
    global rain
    global wind_speed
    temperature = tsp_api.get_data_from_field(test_channel_id, 1)
    humidity = tsp_api.get_data_from_field(test_channel_id, 2)
    pressure = tsp_api.get_data_from_field(test_channel_id, 3)
    illumination = tsp_api.get_data_from_field(test_channel_id, 5)
    rain = tsp_api.get_data_from_field(test_channel_id, 6)
    wind_speed = tsp_api.get_data_from_field(test_channel_id, 7)
    battery_level = tsp_api.get_data_from_field(test_channel_id, 8)

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
def change_date_range(date_range, predictions):
    global temperature_list
    global humidity_list
    global pressure_list
    global date_list
    global illumination_list
    global rain_list
    global wind_speed_list

    # clear all the data lists
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

    # check if the list is empty
    if len(date_list) < 5:
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("No data to show in the selected date range!")
        msgBox.setWindowTitle("Warning!")
        msgBox.exec()
        change_date_range(3, predictions) # show all the data



    # TO DO
    if((predictions == True) and (len(date_list) > 0)):
        # add predicted data
        for n in range(0, 10):
            date_list.append(date_list[len(date_list) - 1] + relativedelta(minutes=2*n)) # if getting data every 20 minutes

        global arima_model_temperature
        global arima_model_humidity
        global arima_model_pressure
        global arima_model_ill
        global arima_model_wind
        global arima_model_rain

        if arima_model_temperature is None:
            arima_model_temperature = auto_arima(temperature_list[-20:], start_p=0, test="adf", start_q=0, max_d=5,
                                                 max_q=5, start_P=0, D=1,
                                                 startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True,
                                                 supress_warnings=True,
                                                 stepwise=True, random_state=20, n_fits=40)
            print("I am here")
            arima_model_humidity = auto_arima(humidity_list[-20:], start_p=0, test="adf", start_q=0, max_d=5, max_q=5,
                                              start_P=0, D=1,
                                              startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True, supress_warnings=True,
                                              stepwise=True, random_state=20, n_fits=40)
            print("I am here")
            arima_model_pressure = auto_arima(pressure_list[-20:], start_p=0, test="adf", start_q=0, max_d=5, max_q=5,
                                              start_P=0, D=1,
                                              startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True, supress_warnings=True,
                                              stepwise=True, random_state=20, n_fits=40)
            print("I am here")
            arima_model_ill = auto_arima(illumination_list[-20:], start_p=0, test="adf", start_q=0, max_d=5, max_q=5,
                                         start_P=0, D=1,
                                         startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True, supress_warnings=True,
                                         stepwise=True, random_state=20, n_fits=40)
            print("I am here")
            arima_model_wind = auto_arima(wind_speed_list[-20:], start_p=0, test="adf", start_q=0, max_d=5, max_q=5,
                                          start_P=0, D=1,
                                          startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True, supress_warnings=True,
                                          stepwise=True, random_state=20, n_fits=40)
            print("I am here")
            arima_model_rain = auto_arima(rain_list[-20:], start_p=0, test="adf", start_q=0, max_d=5, max_q=5,
                                          start_P=0, D=1,
                                          startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True, supress_warnings=True,
                                          stepwise=True, random_state=20, n_fits=40)
        # temperature prediction
        prediction = arima_model_temperature.predict(n_periods=10)
        temperature_list.extend(prediction)

        # humidity prediction
        prediction = arima_model_humidity.predict(n_periods=10)
        humidity_list.extend(prediction)

        # pressure prediction
        prediction = arima_model_pressure.predict(n_periods=10)
        pressure_list.extend(prediction)

        # illumination prediction
        prediction = arima_model_ill.predict(n_periods=10)
        illumination_list.extend(prediction)

        # wind speed prediction
        prediction = arima_model_wind.predict(n_periods=10)
        wind_speed_list.extend(prediction)

        # rain prediction
        prediction = arima_model_rain.predict(n_periods=10)
        rain_list.extend(prediction)
