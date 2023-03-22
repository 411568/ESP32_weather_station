import thingspeak
import json
import matplotlib.pyplot as plt
import time
import thingspeak_api
import datetime
import matplotlib.dates as mdates

# channel id
test_channel_id = 2071282

# getting the data
temperature = thingspeak_api.get_data_from_field(test_channel_id, 4) # temperature
# altitude = thingspeak_api.get_data_from_field(test_channel_id, 4)    # atlitude

# list of dates
date_list = []
for n in range(0, len(temperature)):
    date_list.append(thingspeak_api.parse_date_string(temperature[n][0]))

# list of temperature data
temperature_list = []
for n in range(0, len(temperature)):
    temperature_list.append(float(temperature[n][1]))


# plotting
plt.plot(date_list, temperature_list)
plt.show()