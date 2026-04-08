from sklearn.cluster import KMeans
import numpy as np

def cluster_workloads(X, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)
    return labels, kmeans
