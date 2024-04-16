
import json
with open('cleaned_and_filled_data_normalized_2.json', 'r') as json_file:
    dict_of_values = json.load(json_file)

for j in ['07','08','09','10']:
    with open('.\p1-power-weather\household_power_consumption\household_power_consumption_20'+j+'.csv', 'r') as file:
        # Read lines from the file
        lines = file.readlines()




    filtered_lines = [line for line in lines if (line.split(';')[1].endswith("00:00") and line.split(';')[1][0:2] in ["00","03","06","09","12","15","18","21"])]

    for i in filtered_lines:
        line = i.split(";")
        date = line[0]
        time_of_the_day = line[1]
        day, month, year = date.split('/')
        hour, minute, second = time_of_the_day.split(':')
        time_stamp = f"{year}{month.zfill(2)}{day.zfill(2)}{hour}{minute}{second}"

        line_info = line[2:len(line)-1:]  +  [line[len(line)-1].replace("\n","")]


        
        if time_stamp in dict_of_values:
            dict_of_values[time_stamp] = [dict_of_values[time_stamp], line_info]

    print("done")

new_dict ={}

for i in dict_of_values:
    if len(dict_of_values[i]) ==2:
        new_dict[i] = dict_of_values[i]
#to take out excess data in the weather side so i only take those that have two elments i e the two lists

with open('matched_data.json', 'w') as json_file:
    json.dump(new_dict, json_file, indent=4)
