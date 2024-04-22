import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from sklearn.cluster import KMeans

# Load the JSON data
with open('cleaned_and_filled_data_normalized_2.json', 'r') as file:
    dict_for_values = json.load(file)


daily_vectors = {}
for time_stamp in dict_for_values:
    
    date = time_stamp[:8]
    if date not in daily_vectors:
        daily_vectors[date] = []
    daily_vectors[date] = daily_vectors[date] + dict_for_values[time_stamp]


for time_stamp in [i for i in daily_vectors]:
    if len(daily_vectors[time_stamp]) != 8 * 8 :
        del daily_vectors[time_stamp]



with open('cleaned_and_filled_daily_vector.json', 'w') as json_file:
    json.dump(daily_vectors, json_file, indent=4)

dates = list(daily_vectors.keys())
print(len(dates))
data_values = list(daily_vectors.values())
dates = [datetime.strptime(date, "%Y%m%d") for date in dates]
# Perform K-means clustering
n_clusters = 2  # Example: 4 clusters. Adjust this based on your requirements.
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data_values)
labels = kmeans.labels_


plt.figure(figsize=(12, 4))
colors = ['red', 'blue']
for date, label in zip(dates, labels):
    plt.vlines(date, ymin=0, ymax=1, colors=colors[label], linewidth=3)

ax = plt.gca()  # Get the current Axes instance on the current figure
ax.xaxis.set_major_locator(mdates.MonthLocator())  # Set major locator to each month
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format date

plt.xticks(rotation=45)  # Rotate date labels for better readability
plt.ylabel('Cluster')
plt.title('Reclustered Data (After Excluding Smallest Cluster)')

plt.tight_layout()  # Adjust layout to make room for label rotation
plt.show()