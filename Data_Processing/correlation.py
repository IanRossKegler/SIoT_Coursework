import pandas as pd
from sklearn.model_selection import train_test_split
import sklearn
from sklearn import neighbors
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


data = pd.read_csv('./data.csv')
data = data.drop('DateTime', axis=1)

to_drop = ['N', 'Bagger']
data = data[~data['UV'].isin(to_drop)]

mode = data['MentalHealthTweets'].mode()
data['MentalHealthTweets'].fillna(mode[0], inplace=True)

# data = pd.get_dummies(data)

train, test = train_test_split(data, test_size=0.3)

x_train = train.drop('MentalHealthTweets', axis=1)
y_train = train['MentalHealthTweets']

x_test = test.drop('MentalHealthTweets', axis=1)
y_test = test['MentalHealthTweets']

scaler = MinMaxScaler(feature_range=(0, 1))

x_train_scaled = scaler.fit_transform(x_train)
x_train = pd.DataFrame(x_train_scaled)

x_test_scaled = scaler.fit_transform(x_test)
x_test = pd.DataFrame(x_test_scaled)


rmse_val = []  # to store rmse values for different k
for K in range(20):
    K += 1
    model = neighbors.KNeighborsRegressor(n_neighbors=K)

    model.fit(x_train, y_train)  # fit the model
    pred = model.predict(x_test)  # make prediction on test set
    error = sqrt(mean_squared_error(y_test,pred))  # calculate rmse
    rmse_val.append(error)  # store rmse values

curve = pd.DataFrame(rmse_val)  # elbow curve


plt.figure(figsize=(20, 5))
plt.plot(curve[1:])
plt.title('Elbow Curve').set_fontsize(16)
plt.xlabel('K Value').set_fontsize(14)
plt.ylabel('Root Mean Squared Error').set_fontsize(14)
plt.show()



knn = neighbors.KNeighborsRegressor(n_neighbors=12)
mlp = MLPRegressor()
regr = RandomForestRegressor(max_depth=2, random_state=0, n_estimators=100)

knn.fit(x_train, y_train)
mlp.fit(x_train, y_train)
regr.fit(x_train, y_train)

knn_score = knn.score(x_test, y_test)
mlp_score = mlp.score(x_test, y_test)
regr_score = regr.score(x_test, y_test)

print([knn_score, mlp_score, regr_score])
