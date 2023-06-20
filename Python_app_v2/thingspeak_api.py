import thingspeak
import json
import datetime

# this funstion returns a list of data from a single data field in the format of [created_at, data]
# example usage: temperature = get_data_from_field(test_channel_id, 1)
def get_data_from_field(channel_id, field_num):
    ch = thingspeak.Channel(channel_id)
    all_data = ch.get()                                      # get all the data
    all_data_parsed = json.loads(all_data)
    last_entry = ch.get_field_last(1)                        # get last data json
    last_entry_parsed = json.loads(last_entry)
    last_entry_id = last_entry_parsed['entry_id']            # contains the last entry id
    first_entry_id = all_data_parsed['feeds'][0]['entry_id'] # contains thhe first entry id
    number_of_entries = last_entry_id - first_entry_id       # number of data entries

    data_list = []                                           # list of the output data
    which_field = 'field' + str(field_num)                   # which field to get data from
    for n in range(0, number_of_entries):
        temp_list = []
        temp_list.append(all_data_parsed['feeds'][n]['created_at'])
        temp_list.append(all_data_parsed['feeds'][n][which_field])
        data_list.append(temp_list)

    return data_list


# this function parses the date string to the datetime object format
def parse_date_string(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
