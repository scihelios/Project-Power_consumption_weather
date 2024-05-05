
import json
import numpy as np

with open('cleaned_and_filled_data_normalized_2.json', 'r') as json_file:
    dict_of_values = json.load(json_file)

for j in ['07','08','09','10']:
    with open('.\p1-power-weather\household_power_consumption\household_power_consumption_20'+j+'.csv', 'r') as file:
        # Read lines from the file
        lines = file.readlines()

    filtered_lines = {line.split(';')[0]+line.split(';')[1][0:2]:[] for line in lines if (line.split(';')[1].endswith("00:00") and line.split(';')[1][0:2] in ["00","03","06","09","12","15","18","21"])}
    for line in lines:
        if "" in line.split(';') or "?" in line.split(';'):
            pass
        else:
            key = line.split(';')[0]+str((int(line.split(';')[1][0:2])//3)*3).zfill(2)
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
        if time_stamp in dict_of_values :
            dict_of_values[time_stamp] = [dict_of_values[time_stamp],list( filtered_lines[line])]

    print("done")

new_dict ={}

for i in dict_of_values:
    if len(dict_of_values[i]) ==2:
        new_dict[i] = dict_of_values[i]

with open('matched_data_average.json', 'w') as json_file:
    json.dump(new_dict, json_file, indent=4)

#to take out excess data in the weather side so i only take those that have two elments i e the two lists


