from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler

def perlman():
    return KNeighborsRegressor(n_neighbors=5, algorithm='brute', weights='uniform', metric='euclidean')

def hopper():
    return KNeighborsRegressor(n_neighbors=5, algorithm='brute', weights='uniform', metric='hamming')

def ron():
    return KNeighborsRegressor(n_neighbors=3, algorithm='brute', weights='distance', metric='euclidean')

def scaler():
    return MinMaxScaler()