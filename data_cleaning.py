import pandas as pd
import os
import json

folder_path = 'C:/Users/ahmed/Desktop/Project-Power_consumption_weather/p1-power-weather/weather'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
csv_files = csv_files [1::]
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    data = pd.read_csv(file_path, sep=';')
    data = data[data['numer_sta'] == 7149]
    columns_to_use = ["date", "pmer", "tend", "cod_tend", "dd", "ff", "t", "td", "u"]
    data = data[columns_to_use]
    dict_of_values = {}
    for index, row in data.iterrows():
        dict_of_values[row['date']] = row.tolist()[1::]
    json_filename = csv_file.replace('.csv', '.json')
    json_file_path = os.path.join(folder_path, json_filename)
    with open(json_file_path, 'w') as json_file:
        json.dump(dict_of_values, json_file)