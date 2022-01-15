from importlib.resources import path
import json
import os
from datetime import datetime, timedelta


# NOTES:
# I didn't really understand parts 3,4 and 5.
# In part 3 I did not understand if i am supposed to compute average time difference per every specific
# item_id or compute average time difference between requests overall - what I did is computing average
# time difference for every item_id
#
# I had same interpretation problem in part 4
# I assume that I have to compute the number of requests per a single item_id

def yield_json(path):
    for file in os.listdir(path):
        path_to_file = os.path.join(path,file)
        with open(path_to_file) as f:
            yield json.load(f)

def parse_data(path):
    set_of_customers = set()
    set_of_requests = set()
    item_date_status_map = {}
    request_time_average = {}
    request_time_median = {}
    max_requests_per_item = {}
    for data in yield_json(path):
        # iterating through every user in our json
        for user_id in data:
            set_of_customers.add(user_id)  # add user_id into set of customers
            user_data = data[user_id]
            for val in user_data:
                if val == 'variant':
                    continue
                # assuming there are only 2 keys in user_data, so im sure that im processing the 'item_id'
                set_of_requests.add(val)  # add item_id into set of requests
                item_data_list = user_data[val][0]
                # parse data into structure where I store lists of [date,variant] for every 'item_id'
                try:
                    for i in item_data_list:
                        item_date_status_map[val].append(i)
                except KeyError:
                    item_date_status_map[val] = []
                    for i in item_data_list:
                        item_date_status_map[val].append(i)
    max_requests = 0
    max_id = 0
    # iterating through every 'item_id'
    for item in item_date_status_map:
        date_status_list = item_date_status_map[item]
        max_requests_per_item[item] = 0
        for status in date_status_list:
            if status[1] == 'similarInJsonList':
                max_requests_per_item[item] += 1
        if max_requests_per_item[item] > max_requests:
            max_requests = max_requests_per_item[item]
            max_id = item
        if len(date_status_list) < 2:
            continue
        # formulation of the task is incomplete (typo i guess) and there is not exactly specified what to
        # compute in case of only one timestamp. I assume that when there is only one timestamp I compute nothing.

        # calculating time diffs
        date_status_list.sort()
        diffs = []
        for i in range(0, len(date_status_list) - 1):
            before = datetime.fromisoformat(date_status_list[i][0])
            after = datetime.fromisoformat(date_status_list[i + 1][0])
            diffs.append(after - before)
        # calculating time average
        acc = timedelta(0)
        for t in diffs:
            acc += t
        request_time_average[item] = acc / len(diffs)

        # calculating time median
        diffs.sort()
        n = len(diffs)
        if n % 2 != 0:
            request_time_median[item] = diffs[n // 2]
        else:
            request_time_median[item] = (diffs[(n - 1) // 2] + diffs[n // 2]) / 2
    return len(set_of_customers),len(set_of_requests), request_time_average,request_time_median, max_id, max_requests

if __name__ == '__main__':
    
    path = os.path.join(os.getcwd(),'data')
    unique_customers, unique_reqs, avg_times, median_times, max_id, max_reqs = parse_data(path)
    
    print('Number of unique customers is {}'.format(unique_customers))
    print('Number of unique requests is {}'.format(unique_reqs))
    print('Maximum number of requests with the variant \'similarInJsonList\' returned is {} for request {}'
        .format(max_reqs, max_id))
    print('Avarage and median times are stored into files \'avg_times\' and \'median_times\'')

    with open('avg_times','w') as f:
        json.dump(avg_times,f,indent=4,sort_keys=True,default=str)
    with open('median_times','w') as f:
        json.dump(avg_times,f,indent=4,sort_keys=True,default=str)

