from sklearn import datasets
import pandas as pd
from sklearn.cluster import KMeans

iris_raw = datasets.load_iris()
iris = pd.DataFrame(
    iris_raw["data"],
    columns=iris_raw["feature_names"]
)


def cluster_data(data, x, y, n_clusters):
    data = data.loc[:, [x, y]]
    km = KMeans(n_clusters=max(n_clusters, 1))
    km.fit(data.values)
    data["cluster"] = km.labels_
    centers = km.cluster_centers_
    return data, centers

# cluster_data(iris, iris.columns[1], iris.columns[2], 3 )
