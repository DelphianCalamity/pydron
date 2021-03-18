# import ray
import pydron
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

# ray.init()

def get_data():
    df = pd.read_csv('./KNN_Project_Data')
    df.head()
    scaler = StandardScaler()
    scaler.fit(df.drop('TARGET CLASS',axis=1))
    scaled_features = scaler.transform(df.drop('TARGET CLASS',axis=1))
    df_feat = pd.DataFrame(scaled_features,columns=df.columns[:-1])
    df_feat.head()

    X_train, X_test, y_train, y_test = train_test_split(scaled_features,df['TARGET CLASS'],test_size=0.30)
    return X_train, X_test, y_train, y_test


# @ray.remote
@pydron.functional
def get_n_val(i, X_train, X_test, y_train, y_test):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    return np.mean(pred_i != y_test)


def run_non_parallelized(neighbor_num, X_train, X_test, y_train, y_test):
    # non-parallelized loop
    start = time.time()
    error_rate = []

    for i in range(1, neighbor_num):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(X_train, y_train)
        pred_i = knn.predict(X_test)
        error_rate.append(np.mean(pred_i != y_test))

    end = time.time()
    return end - start


@pydron.schedule
def run_parallelized(neighbor_num, X_train, X_test, y_train, y_test):
    # parallelized loop
    start = time.time()
    error_rate = []

    for i in range(1, neighbor_num):
        err = get_n_val(i, X_train, X_test, y_train, y_test)
        error_rate = error_rate + [err]  # error_rate.append(err)

    end = time.time()
    return end - start


if __name__ == '__main__':
    experiment_num = 5
    neighbor_num = 500
    X_train, X_test, y_train, y_test = get_data()

    n_times = []
    p_times = []
    for _ in range(experiment_num):
        time1 = run_non_parallelized(neighbor_num, X_train, X_test, y_train, y_test)
        time2 = run_parallelized(neighbor_num, X_train, X_test, y_train, y_test)
        n_times.append(time1)
        p_times.append(time2)

    print(n_times)
    print(p_times)
