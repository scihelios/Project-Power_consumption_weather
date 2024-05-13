import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from sklearn.cluster import KMeans

# Load the JSON data
with open('matched_data_average_normalized.json', 'r') as file:
    dict_for_values = json.load(file)


daily_vectors = {}
for time_stamp in dict_for_values:
    date = time_stamp[:8]
    if date not in daily_vectors:
        daily_vectors[date] = []
    daily_vectors[date] = daily_vectors[date] + dict_for_values[time_stamp][1]


for time_stamp in [i for i in daily_vectors]:
    daily_vectors[time_stamp] = daily_vectors[time_stamp]
    if len(daily_vectors[time_stamp]) !=  7*8 :
        del daily_vectors[time_stamp]




with open('cleaned_and_filled_daily_vector_average_consumption.json', 'w') as json_file:
    json.dump(daily_vectors, json_file, indent=4)

dates = list(daily_vectors.keys())
data_values = list(daily_vectors.values())
dates = [datetime.strptime(date, "%Y%m%d") for date in dates]

n_clusters = 2 
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data_values)
labels = kmeans.labels_


date_to_cluster = {date.strftime("%Y%m%d"): label for date, label in zip(dates, labels)}

print(date_to_cluster)

dict_of_values = {}
with open('hourly_averaged_consumption.json', 'r') as json_file:
    dict_of_values = json.load(json_file)


average_values_per_hour = {str(i).zfill(2) + "0000": [0]*7 for i in range(24)}

entry_count_per_hour = {str(i).zfill(2) + "0000": [0]*7 for i in range(24)}

for time, values in dict_of_values.items():
    hour_string = time[-6:]  
    try:
        if date_to_cluster[time[0:8]]==1 :
            for i, value in enumerate(values):
                if value > 0:
                    average_values_per_hour[hour_string][i] += value
                    entry_count_per_hour[hour_string][i] += 1
    except:
        pass

for hour in average_values_per_hour:
    for i in range(7):
        if entry_count_per_hour[hour][i] > 0:
            average_values_per_hour[hour][i] /= entry_count_per_hour[hour][i]

variable_names = ["global_active_power", "global_reactive_power", "voltage", "global_intensity",
                  "sub_metering_1", "sub_metering_2", "sub_metering_3"]

fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(15, 7))
axes = axes.flatten()

for i in range(7):
    
    y_values = [average_values_per_hour[hour][i] for hour in sorted(average_values_per_hour)]
    x_values = list(range(24)) 
    axes[i].plot(x_values, y_values, marker='o',color='red')
    axes[i].set_title(variable_names[i])
    axes[i].set_xlabel('Hour of the day')
    axes[i].set_ylabel('Average Consumption')
    axes[i].set_xticks(x_values[::2])  
    axes[i].set_xticklabels([f"{int(hour[:2])}" for hour in sorted(average_values_per_hour)[::2]]) 

plt.tight_layout()





average_values_per_hour = {str(i).zfill(2) + "0000": [0]*7 for i in range(24)}

entry_count_per_hour = {str(i).zfill(2) + "0000": [0]*7 for i in range(24)}

for time, values in dict_of_values.items():
    hour_string = time[-6:]  
    try:
        if date_to_cluster[time[0:8]]==0 :
            for i, value in enumerate(values):
                if value > 0:  
                    average_values_per_hour[hour_string][i] += value
                    entry_count_per_hour[hour_string][i] += 1
    except:
        pass

for hour in average_values_per_hour:
    for i in range(7):
        if entry_count_per_hour[hour][i] > 0:
            average_values_per_hour[hour][i] /= entry_count_per_hour[hour][i]


for i in range(7):
  
    y_values = [average_values_per_hour[hour][i] for hour in sorted(average_values_per_hour)]
    x_values = list(range(24))  # Hours from 0 to 23
    axes[i].plot(x_values, y_values, marker='o',color='blue')


plt.tight_layout()
plt.show()
