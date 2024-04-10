import pandas as pd
import os
import json
import random
import matplotlib.pyplot as plt

with open('cleaned_and_filled_data.json', 'r') as json_file:
    dict_of_values = json.load(json_file)


time_stamps =  [i for i in dict_of_values]
time_stamps.sort()
for i , time in enumerate(time_stamps):
    for j , value in enumerate(dict_of_values[time] ): 

        if value =="mq":
            if j == 2 :
                dict_of_values[time][j] = float(random.choice([dict_of_values[time_stamps[i-1]][j],dict_of_values[time_stamps[i+1]][j]]))
                # pas de valeur bizarre comme 5.5 car il faut un int stricte car c'est un code de type de condition 
                # donc je vais choisir randomly entre les deux valeurs que j'ai avant et aprés le time stamp
                      
            else:
                try:
                    dict_of_values[time][j] = (float(dict_of_values[time_stamps[i-1]][j])+float(dict_of_values[time_stamps[i+1]][j]))/2
                    #je prend juste la moyenne des valeur du même indice dans les time stamp d'avant et aprés
                    pass
                except Exception as e:
   
                    print("An error occurred:", dict_of_values[time_stamps[i-1]][j] , dict_of_values[time_stamps[i+1]][j] , time , j)
        else:
            dict_of_values[time][j] = float(value)
        
        if j == 1:
            if value <= -500 or value >= 500 :
                del dict_of_values[time]

values_for_histogramme =[[] for i in range(8)] #car 8 variable en total
for i , time in enumerate(time_stamps):
    for j , value in enumerate(dict_of_values[time] ): 
        values_for_histogramme[j].append(value)


max_values_vector = [max(i) for i in values_for_histogramme]
min_values_vector = [min(i) for i in values_for_histogramme]

#now for the 0-1 normalization (cause it is much easier)
for i , time in enumerate(time_stamps):
    for j , value in enumerate(dict_of_values[time] ): 
        dict_of_values[time][j] = (value-min_values_vector[j])/max_values_vector[j]-min_values_vector[j]



variable_names = ["Pression au niveau mer","Variation de pression en 3 h","Type de tendance ba","Direction du vent(degré)",
                    "Vitesse du vent (m/s)", "Température (K)", "Point de rosée (K)","Humidité (%)"]


fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(10, 20))
axes = axes.flatten()

for i, ax in enumerate(axes):
    ax.hist(values_for_histogramme[i], bins='auto', alpha=0.75)
    ax.set_title(variable_names[i])
    ax.set_ylabel('Frequency')
plt.show()


with open('cleaned_and_filled_data_g.json', 'w') as json_file:
    json.dump(dict_of_values, json_file, indent=4)