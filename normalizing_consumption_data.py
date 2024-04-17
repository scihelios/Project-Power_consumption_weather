import pandas as pd
import os
import json
import random
import matplotlib.pyplot as plt
import numpy as np

with open('matched_data_average.json', 'r') as json_file:
    dict_of_values = json.load(json_file)

print(len(dict_of_values))
time_stamps =  [i for i in dict_of_values]
time_stamps.sort()
print(len(time_stamps))
new_dict_of_values = dict_of_values

time_stamps =  [i for i in new_dict_of_values]
time_stamps.sort()
print(new_dict_of_values)

with open('testing.json', 'w') as json_file:
    json.dump(new_dict_of_values, json_file, indent=4)

values_for_histogramme =[[] for i in range(7)] #car 7 variable en total
for i , time in enumerate(time_stamps):
    for j , value in enumerate(new_dict_of_values[time][1]): 
        values_for_histogramme[j].append(value)



mean_values_vector = [np.mean(np.array(i)) for i in values_for_histogramme]

variance_values_vector = [np.std(np.array(i)) for i in values_for_histogramme]


#now for the 0-1 normalization (cause it is much easier)
for i , time in enumerate(time_stamps):
    try:   
        for j , value in enumerate(new_dict_of_values[time][1] ): 
            new_dict_of_values[time][1][j] = (value-mean_values_vector[j])/variance_values_vector[j]
            if new_dict_of_values[time][1][j]>5:
                del new_dict_of_values[time]
    except:
        pass

values_for_histogramme =[[] for i in range(7)] #car 7 variable en total
for i , time in enumerate(new_dict_of_values.keys()):
    for j , value in enumerate(new_dict_of_values[time][1]): 
        values_for_histogramme[j].append(value)

variable_names = ["global_active_power","global_reactive_power","voltage","global_intensity",
                  "sub_metering_1","sub_metering_2","sub_metering_3"]


fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(10, 20))
axes = axes.flatten()

for i, ax in enumerate(axes):
    if i <7 :
        ax.hist(values_for_histogramme[i], bins=10, alpha=0.75)
        ax.set_title(variable_names[i])
        ax.set_ylabel('Frequency')
plt.show()


with open('matched_data_average_normalized.json', 'w') as json_file:
    json.dump(new_dict_of_values, json_file, indent=4)