import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the JSON data
with open('cleaned_and_filled_data.json', 'r') as file:
    dict_for_values = json.load(file)


daily_vectors = {}
for time_stamp in dict_for_values:
    
    date = time_stamp[:8]
    if date not in daily_vectors:
        daily_vectors[date] = []
    daily_vectors[date] = daily_vectors[date] + dict_for_values[time_stamp]


for time_stamp in daily_vectors:
    if len(daily_vectors[time_stamp]) != 7 * 8 :
        del daily_vectors[time_stamp]



# Cluster the dict_for_values
n_clusters = 4  # Example: 4 clusters. Adjust based on your analysis.
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(normalized_data)

# Print the cluster labels for each day
cluster_labels = kmeans.labels_
for i, date in enumerate(daily_vectors.keys()):
    print(f"Date: {date}, Cluster: {cluster_labels[i]}")