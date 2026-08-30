import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def perform_clustering(df, n_clusters=3):
    df_copy = df.copy()
    X = df_copy[["Latitude", "Longitude", "Severity_Score"]].copy()
    weights = np.sqrt(df_copy["Severity_Score"] + 1)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_copy["Cluster"] = kmeans.fit_predict(X, sample_weight=weights)
    cluster_means = df_copy.groupby("Cluster")["Severity_Score"].mean().sort_values()
    risk_mapping = {
        cluster_means.index[0]: "Low",
        cluster_means.index[1]: "Medium",
        cluster_means.index[2]: "High"
    }
    df_copy["Risk_Level"] = df_copy["Cluster"].map(risk_mapping)
    return df_copy
