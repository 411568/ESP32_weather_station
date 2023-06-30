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
test_channel_id = 2071282  # 2208447 #     #2208447  #

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
            date_list.append(date_list[len(date_list) - 1] + relativedelta(days = 1))   # minutes=2*n if getting data every 20 minutes

        global arima_model_temperature
        global arima_model_humidity
        global arima_model_pressure
        global arima_model_ill
        global arima_model_wind
        global arima_model_rain

        daily_temp = []
        daily_humidity = []
        daily_pressure = []
        daily_ill = []
        daily_wind = []
        daily_rain = []

        # calculate the sarima models if not done yet
        if arima_model_temperature is None:
            # calculate the average parameters for every day
            for i in range(0, len(temperature_list) - 1):
                current_day = date_list[i].day
                current_month = date_list[i].month
                current_year = date_list[i].year

                if date_list[len(temperature_list) - 1].day == current_day and date_list[
                    len(temperature_list) - 1].month == current_month and date_list[
                    len(temperature_list) - 1].year == current_year:
                    break

                avg_temp = 0.0
                avg_hum = 0.0
                avg_press = 0.0
                avg_ill = 0.0
                avg_wind = 0.0
                avg_rain = 0.0

                counter = 0

                for j in range(0, len(temperature_list) - i - 1):
                    if date_list[i + j].day == current_day and date_list[i].month == current_month and date_list[
                        i].year == current_year:
                        counter = counter + 1
                        avg_temp += temperature_list[i + j]
                        avg_hum += humidity_list[i + j]
                        avg_press += pressure_list[i + j]
                        avg_ill += illumination_list[i + j]
                        avg_wind += wind_speed_list[i + j]
                        avg_rain += rain_list[i + j]
                    else:
                        break

                daily_temp.append(avg_temp / counter)
                daily_humidity.append(avg_hum / counter)
                daily_pressure.append(avg_press / counter)
                daily_ill.append(avg_ill / counter)
                daily_rain.append(avg_rain / counter)
                daily_wind.append(avg_wind / counter)

                i = i + counter

            # find the models
            arima_model_temperature = auto_arima(daily_temp, start_p=0, test="adf", start_q=0, max_d=5,
                                                 max_q=5, start_P=0, D=1,
                                                 startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True,
                                                 supress_warnings=True,
                                                 stepwise=True, random_state=20, n_fits=40) # temperature_list[-20:]
            arima_model_humidity = auto_arima(daily_humidity, start_p=0, test="adf", start_q=0, max_d=5, max_q=5,
                                              start_P=0, D=1,
                                              startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True, supress_warnings=True,
                                              stepwise=True, random_state=20, n_fits=40) #humidity_list[-20:]
            arima_model_pressure = auto_arima(daily_pressure, start_p=0, test="adf", start_q=0, max_d=5, max_q=5,
                                              start_P=0, D=1,
                                              startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True, supress_warnings=True,
                                              stepwise=True, random_state=20, n_fits=40) # pressure_list[-20:]
            arima_model_ill = auto_arima(daily_ill, start_p=0, test="adf", start_q=0, max_d=5, max_q=5,
                                         start_P=0, D=1,
                                         startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True, supress_warnings=True,
                                         stepwise=True, random_state=20, n_fits=40) #illumination_list[-20:]
            arima_model_wind = auto_arima(daily_wind, start_p=0, test="adf", start_q=0, max_d=5, max_q=5,
                                          start_P=0, D=1,
                                          startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True, supress_warnings=True,
                                          stepwise=True, random_state=20, n_fits=40) #wind_speed_list[-20:]
            arima_model_rain = auto_arima(daily_rain, start_p=0, test="adf", start_q=0, max_d=5, max_q=5,
                                          start_P=0, D=1,
                                          startQ=5, max_P=5, max_D=5, max_Q=5, seasonal=True, supress_warnings=True,
                                          stepwise=True, random_state=20, n_fits=40) #

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
