import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

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



with open('cleaned_and_filled_daily_vector_2.json', 'w') as json_file:
    json.dump(daily_vectors, json_file, indent=4)

dates = list(daily_vectors.keys())
print(len(dates))
data_values = list(daily_vectors.values())

# Perform K-means clustering
n_clusters = 3  # Example: 4 clusters. Adjust this based on your requirements.
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data_values)
labels = kmeans.labels_

# Create a plot
plt.figure(figsize=(12, 8))  # Adjust size to your needs
plt.scatter(dates, labels, color='blue', s=5)  # Scatter plot of dates vs clusters


plt.ylabel('Cluster')
plt.title('Cluster Assignment by Date')


# Show the plot
plt.tight_layout()  # Adjust layout to make room for label rotation
plt.show()