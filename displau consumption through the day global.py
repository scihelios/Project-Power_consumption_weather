import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


dict_of_values = {}
with open('hourly_averaged_consumption.json', 'r') as json_file:
    dict_of_values = json.load(json_file)


average_values_per_hour = {str(i).zfill(2) + "0000": [0]*7 for i in range(24)}


entry_count_per_hour = {str(i).zfill(2) + "0000": [0]*7 for i in range(24)}


for time, values in dict_of_values.items():
    hour_string = time[-6:] 
    for i, value in enumerate(values):
        if value > 0:  
            average_values_per_hour[hour_string][i] += value
            entry_count_per_hour[hour_string][i] += 1


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
    x_values = list(range(24))  # Hours from 0 to 23
    axes[i].plot(x_values, y_values, marker='o')
    axes[i].set_title(variable_names[i])
    axes[i].set_xlabel('Hour of the day')
    axes[i].set_ylabel('Average Consumption')
    axes[i].set_xticks(x_values[::2])  
    axes[i].set_xticklabels([f"{int(hour[:2])}" for hour in sorted(average_values_per_hour)[::2]]) 

plt.tight_layout()
plt.show()

