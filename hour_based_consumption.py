
import json
import numpy as np
import matplotlib.pyplot as plt
dict_of_values ={} 

for j in ["07","08","09","10"]:
    with open('.\p1-power-weather\household_power_consumption\household_power_consumption_20'+j+'.csv', 'r') as file:
        # Read lines from the file
        lines = file.readlines()

    filtered_lines = {line.split(';')[0]+line.split(';')[1][0:2]:[] for line in lines if (line.split(';')[1].endswith("00:00") and line.split(';')[1][0:2] in [str(i).zfill(2) for i in range(24)])}
    
    for line in lines:
        if "" in line.split(';') or "?" in line.split(';'):
            pass
        else:
            key = line.split(';')[0]+str(int(line.split(';')[1][0:2])).zfill(2)
            line_info = line.split(';')
            line_info =line_info[2:len(line_info)-1:]  + [line_info[len(line_info)-1].replace("\n","")]
            filtered_lines[key].append([float(i) for i in line_info])
    
    for i in set(filtered_lines.keys()):
        if len(filtered_lines[i]) == 0:
            del filtered_lines[i] 
        else:
            sum = np.zeros(7)
            for j in filtered_lines[i]:
                sum += np.array(j)
            sum = sum / len(filtered_lines[i])
            filtered_lines[i] = sum

    for line in filtered_lines:
        date = line[0:len(line)-2]
        time_of_the_day = line[-2:]+"0000"
        day, month, year = date.split('/')
        time_stamp = year+month.zfill(2)+day.zfill(2)+time_of_the_day
        dict_of_values[time_stamp] = list( filtered_lines[line])

    print("done")

for i in dict_of_values:
    print(i , "     ",dict_of_values[i])


with open('hourly_averaged_consumption.json', 'w') as json_file:
    json.dump(dict_of_values, json_file, indent=4)



values_for_histogramme = {str(i).zfill(2)+"0000": [[] for j in range(7)] for i in range(24)}
print(values_for_histogramme)
time_stamps = [i for i in dict_of_values]

for i , time in enumerate(time_stamps):
    for j , value in enumerate(dict_of_values[time]): 
        if value >0:

            values_for_histogramme[time[-6::]][j].append(np.log(value))


variable_names = ["global_active_power","global_reactive_power","voltage","global_intensity",
                  "sub_metering_1","sub_metering_2","sub_metering_3"]




for j in values_for_histogramme:
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(10, 20))
    axes = axes.flatten()
    for i, ax in enumerate(axes):
        if i <7 :
            ax.hist(values_for_histogramme[j][i], bins=25, alpha=0.75)
            ax.set_title(variable_names[i])
            ax.set_ylabel('Frequency')

    plt.show()
    print(j)



mean_values_vector = [np.mean(np.array(i)) for i in values_for_histogramme]

variance_values_vector = [np.std(np.array(i)) for i in values_for_histogramme]


#now for the 0-1 normalization (cause it is much easier)
for i , time in enumerate(time_stamps):
    try:   
        for j , value in enumerate(dict_of_values[time][1] ): 
            dict_of_values[time][j] = (value-mean_values_vector[j])/variance_values_vector[j]
            if dict_of_values[time][j]>5:
                del dict_of_values[time]
    except:
        pass

values_for_histogramme =[[] for i in range(7)] #car 7 variable en total
for i , time in enumerate(dict_of_values.keys()):
    for j , value in enumerate(dict_of_values[time]): 
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



