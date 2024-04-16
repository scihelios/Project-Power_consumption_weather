import pandas as pd
import os
import json
import random
import matplotlib.pyplot as plt
import numpy as np

with open('cleaned_and_filled_data.json', 'r') as json_file:
    dict_of_values = json.load(json_file)

print(len(dict_of_values))
time_stamps =  [i for i in dict_of_values]
time_stamps.sort()
print(len(time_stamps))
new_dict_of_values = dict_of_values
for i , time in enumerate(time_stamps):
    for j , value in enumerate(dict_of_values[time] ): 

        if value =="mq":
            if j == 2 :
                new_dict_of_values[time][j] = float(random.choice([new_dict_of_values[time_stamps[i-1]][j],new_dict_of_values[time_stamps[i+1]][j]]))
                # pas de valeur bizarre comme 5.5 car il faut un int stricte car c'est un code de type de condition 
                # donc je vais choisir randomly entre les deux valeurs que j'ai avant et aprés le time stamp
                      
            else:
                try:
                    new_dict_of_values[time][j] = (float(new_dict_of_values[time_stamps[i-1]][j])+float(new_dict_of_values[time_stamps[i+1]][j]))/2
                    #je prend juste la moyenne des valeur du même indice dans les time stamp d'avant et aprés
                    pass
                except Exception as e:
   
                    print("An error occurred:", new_dict_of_values[time_stamps[i-1]][j] , new_dict_of_values[time_stamps[i+1]][j] , time , j)
        else:
            try:
                new_dict_of_values[time][j] = float(value)
                pass
            except:
                pass
        


        if j == 1:
            if value <= -500 or value >= 500 :
                del new_dict_of_values[time]

time_stamps =  [i for i in new_dict_of_values]
time_stamps.sort()

values_for_histogramme =[[] for i in range(8)] #car 8 variable en total
for i , time in enumerate(time_stamps):
    for j , value in enumerate(new_dict_of_values[time] ): 
        values_for_histogramme[j].append(value)


mean_values_vector = [np.mean(np.array([j for j in i if j!=0])) for i in values_for_histogramme]
variance =[np.std(np.array([j for j in i if j!=0])) for i in values_for_histogramme]


#now for the 0-1 normalization (cause it is much easier)
for i , time in enumerate(time_stamps):
    for j , value in enumerate(new_dict_of_values[time] ): 
        new_dict_of_values[time][j] = (value-mean_values_vector[j])/variance[j]

values_for_histogramme =[[] for i in range(8)] #car 8 variable en total
for i , time in enumerate(time_stamps):
    for j , value in enumerate(new_dict_of_values[time] ): 
        values_for_histogramme[j].append(value)



variable_names = ["Pression au niveau mer","Variation de pression en 3 h","Type de tendance ba","Direction du vent(degré)",
                    "Vitesse du vent (m/s)", "Température (K)", "Point de rosée (K)","Humidité (%)"]


fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(10, 20))
axes = axes.flatten()

for i, ax in enumerate(axes):
    if i <8 :
        ax.hist(values_for_histogramme[i], bins=10, alpha=0.75)
        ax.set_title(variable_names[i])
        ax.set_ylabel('Frequency')
plt.show()

with open('cleaned_and_filled_data_normalized_2.json', 'w') as json_file:
    json.dump(new_dict_of_values, json_file, indent=4)