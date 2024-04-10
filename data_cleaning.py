import pandas as pd
import os
import json

folder_path = './p1-power-weather/weather'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
csv_files = csv_files [1::]
dict_of_values = {}
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)


    data = pd.read_csv(file_path, sep=';')
    data = data[data['numer_sta'] == 7149]

    columns_to_use = ["date", "pmer", "tend", "cod_tend", "dd", "ff", "t", "td", "u"]

    data = data[columns_to_use]
    print(csv_file)
    
    for index, row in data.iterrows():
        dict_of_values[row['date']] = row.tolist()[1::]

print(len(dict_of_values))
compt = 0
catch=0
for i in dict_of_values:
    toadd = 0
    for j in dict_of_values[i] : 
        if j=="mq":
            compt += 1
            toadd=1
    catch += toadd
    if toadd == 1 :
        if catch >=2:
            print(i)
    else :
        catch =0

with open('example.json', 'w') as json_file:
    json.dump(dict_of_values, json_file, indent=4)



    