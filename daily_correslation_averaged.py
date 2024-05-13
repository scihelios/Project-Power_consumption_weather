import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np

with open('matched_data_non_normalized.json', 'r') as file:
    data = json.load(file)
test_vectors={}
daily_vectors = {}
for time_stamp in data:
    date = time_stamp[:8]
    if date[:4] !='2010':
        if date not in daily_vectors:
            daily_vectors[date] = [[], []]  
        daily_vectors[date][0].append(data[time_stamp][0])
        daily_vectors[date][1].append(data[time_stamp][1])
    else : 
        if date not in test_vectors:
            test_vectors[date] = [[], []]  
        test_vectors[date][0].append(data[time_stamp][0])
        test_vectors[date][1].append(data[time_stamp][1])



for time_stamp in [i for i in daily_vectors]:
    if len(daily_vectors[time_stamp][1]) != 8 or len(daily_vectors[time_stamp][0]) !=  8:
        del daily_vectors[time_stamp]


for date in list(daily_vectors.keys()):
    try:
        if len(daily_vectors[date][0]) > 0 and len(daily_vectors[date][1]) > 0:
            daily_vectors[date][0] = sum([np.array(f) for f in daily_vectors[date][0] if (len(f)==8)])/8
            daily_vectors[date][1] = sum([np.array(t) for t in daily_vectors[date][1] if (len(t)==7)])/8
    except:
        del daily_vectors[date]



for time_stamp in [i for i in test_vectors]:
    if len(test_vectors[time_stamp][1]) != 8 or len(test_vectors[time_stamp][0]) !=  8:
        del test_vectors[time_stamp]

for date in list(test_vectors.keys()):
    try:
        if len(test_vectors[date][0]) > 0 and len(test_vectors[date][1]) > 0:
            test_vectors[date][0] = sum([np.array(f) for f in test_vectors[date][0] if (len(f)==8)])/8
            test_vectors[date][1] = sum([np.array(t) for t in test_vectors[date][1] if (len(t)==7)])/8
    except:
        del test_vectors[date]


data = daily_vectors

X = []
Y = []
for key, value in data.items():
    X.append(value[0])  
    Y.append(value[1])  


X = pd.DataFrame(X, columns=["Pression au n.mer","Var de press en 3 h","Type de tendance ba","Direction du vent(degré)",
                    "Vitesse du vent (m/s)", "Température (K)", "Point de rosée (K)","Humidité (%)"])
Y = pd.DataFrame(Y, columns=["Global Active Power", "Global Reactive Power", "Voltage", "Global Intensity",
                             "Sub Metering 1", "Sub Metering 2", "Sub Metering 3"])


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.01, random_state=42)



model = LinearRegression()
model.fit(X_train, Y_train)

coefficients = model.coef_
print("Coefficient Matrix Shape:", coefficients.shape)
print("Coefficients:", coefficients)

Y_pred = model.predict(X_test)


mse = mean_squared_error(Y_test, Y_pred, multioutput='raw_values')
print("Mean Squared Error per Output Dimension:", mse)


fig, ax = plt.subplots(figsize=(12, 7))
img = ax.imshow(coefficients, cmap='coolwarm', interpolation='none')
ax.set_xticks(np.arange(len(X.columns)))
ax.set_yticks(np.arange(len(Y.columns)))
ax.set_title('Coefficient Matrix')
fig.colorbar(img, ax=ax)
ax.set_xticklabels(X.columns, rotation=90)
ax.set_yticklabels(Y.columns)
plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

dates = sorted(test_vectors.keys())
date_objs = [datetime.strptime(date, "%Y%m%d") for date in dates]  

predictions = model.predict(np.array([list(test_vectors[date][0]) for date in dates]))

fig, ax = plt.subplots()

ax.xaxis.set_major_locator(mdates.WeekdayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
for i in range(7):
    val = [test_vectors[date][1][i] for date in dates]
    pred = [prediction[i] for prediction in predictions]
    med = [(val[k-2] + val[k-1] + val[k] + val[k+1] + val[k+2]) / 5 for k in range(2, len(val)-2)]
    
    plt.plot(date_objs, val, label='Actual Values')
    plt.plot(date_objs, pred, label='Predictions')



    plt.xticks(rotation=45)
    plt.legend()
    plt.show()
