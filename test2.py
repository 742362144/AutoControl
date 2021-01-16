import json
import math

from statsmodels.tsa.stattools import adfuller
import pandas as pd
import matplotlib.pyplot as plt

# data = pd.read_csv('Tractor-Sales.csv')

data = []
with open('test.txt', 'r') as f:
    data = json.load(f)

data = pd.Series(data)


first_rows = data.head(5) # 返回前n条数据,默认返回5条

# cols = data.columns # 返回全部列名

# dimensison = data.shape # 返回数据的格式，数组，（行数，列数）
# print(dimensison)
#
# data.values # 返回底层的numpy数据

# b = data.values[:, 1]

# b = pd.Series()
b = data

# plot(data, xlab='Years', ylab='Tractor Sales')

# b = [10930, 10318, 10595, 10972, 7706, 6756, 9092, 10551, 9722, 10913, 11151, 8186, 6422,
#      6337, 11649, 11652, 10310, 12043, 7937, 6476, 9662, 9570, 9981, 9331]
# b = pd.Series(b)

print("Results of Dicky-Fuller Test:")
dftest = adfuller(b, autolag='AIC')

dfoutput = pd.Series(dftest[0:4], index=['ADF Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
for key, value in dftest[4].items():
    dfoutput['Critical Value (%s)' % key] = value

print(dfoutput)

from pmdarima.arima import auto_arima

train = b[:9950]
test = b[9950:]

res = []
for i in range(len(test)):
    train = b[i:i+100]
    model = auto_arima(train, start_p=1, start_q=1,
                       max_p=10, max_q=10, m=1,
                       seasonal=False,
                       d=0, trace=True,
                       error_action='warn',
                       suppress_warnings=True,
                       stepwise=True)
    print(model.aic())

    model.fit(train)
    print('predict: %f' % model.predict(n_periods=1)[0])
    res.append(model.predict(n_periods=1)[0])
print(json.dumps(res))
print(json.dumps(test.values.tolist()))

# plt.plot(test)
# plt.plot(res)
# plt.legend()
# plt.show()

# mse = 0.0
# for i in range(min(len(res), len(test))):
#     mse += (res[i] - test[i]) * (res[i] - test[i])
#
# print(mse)


# prediction1 = model.predict(n_periods=20)
# prediction2 = model.predict(n_periods=20)
#
# print(type(train))
# print(type(test))
# print(type(prediction1))
# print(type(prediction2))
#
# print(prediction1)
# print(prediction2)
#
# # plot the predictions for validation set
# plt.plot(train.values, label='train')
# plt.plot(test.values, label='test')
# plt.plot(prediction1, label='prediction1')
# plt.plot(prediction2, label='prediction2')
# plt.legend()
# plt.show()
